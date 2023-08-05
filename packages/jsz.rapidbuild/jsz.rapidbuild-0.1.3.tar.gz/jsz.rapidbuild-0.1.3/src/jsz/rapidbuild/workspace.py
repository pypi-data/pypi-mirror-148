#!/usr/bin/env
from dataclasses import dataclass
from typing import Any, Union
import yaml
import os.path
import fs.path
from fs.base import FS
from fs.osfs import OSFS
import fs.errors

from . import base
from .conan import SystemConfigManifestProviderConan
from .fastbuild import BuildScriptEmitterFastbuild
from .toolchain import ToolchainSettingsProviderDefault


class WorkspaceInvalidFormatError(Exception):
    pass


@dataclass
class TargetScopedProperties:
    definitions: dict[Any, Any]
    dependencies: list[str]
    externals: list[str]

    @staticmethod
    def from_dict(d: dict):
        if not isinstance(d, dict):
            raise WorkspaceInvalidFormatError
        if not set(d.keys()).issubset({"definitions", "dependencies", "externals"}):
            raise WorkspaceInvalidFormatError
        definitions = d.get("definitions", {})
        if not isinstance(definitions, dict):
            raise WorkspaceInvalidFormatError
        dependencies = d.get("dependencies", [])
        if not isinstance(dependencies, list):
            raise WorkspaceInvalidFormatError
        externals = d.get("externals", [])
        if not isinstance(externals, list):
            raise WorkspaceInvalidFormatError
        return TargetScopedProperties(definitions=definitions, dependencies=dependencies, externals=externals)


@dataclass
class TargetDefinition:
    name: str
    kind: base.TargetKind
    private_props: TargetScopedProperties
    public_props: TargetScopedProperties

    @staticmethod
    def from_dict(name: str, d: dict):
        if not isinstance(d, dict):
            raise WorkspaceInvalidFormatError
        if not set(d.keys()).issubset({"kind", "public", "private"}):
            raise WorkspaceInvalidFormatError
        if "kind" not in d.keys():
            raise WorkspaceInvalidFormatError
        try:
            kind = base.TargetKind.from_string(d["kind"])
        except KeyError:
            raise WorkspaceInvalidFormatError
        public_props = TargetScopedProperties.from_dict(d.get("public", {}))
        private_props = TargetScopedProperties.from_dict(d.get("private", {}))
        return TargetDefinition(name=name, kind=kind, private_props=private_props, public_props=public_props)


@dataclass
class WorkspaceDefinition:
    targets: list[TargetDefinition]

    @staticmethod
    def from_dict(d):
        if not isinstance(d, dict):
            raise WorkspaceInvalidFormatError
        if len(d) == 0:
            raise WorkspaceInvalidFormatError
        targets = [TargetDefinition.from_dict(name, v) for name, v in d.items()]
        return WorkspaceDefinition(targets=targets)


def append_unique(list_: list[Any], item: any):
    if item not in list_:
        list_.append(item)


def _validate_third_party_manifest(manifest):
    if not isinstance(manifest, dict):
        return False
    return True


def _validate_toolchains_manifest(manifest):
    if not isinstance(manifest, dict):
        return False
    if len(manifest.keys()) == 0:
        return False
    return True


def _create_targets_interfaces_and_implementations(source_dir_abs_path, toolchains_manifest, build_types,
                                                   third_party_manifest, workspace_def: WorkspaceDefinition):
    assert(len(source_dir_abs_path) != 0)
    assert(len(build_types) != 0)
    assert(_validate_toolchains_manifest(toolchains_manifest))
    assert(_validate_third_party_manifest(third_party_manifest))

    targets_interfaces = dict(third_party_manifest)
    targets_impls = {}

    for toolchain_name in toolchains_manifest.keys():
        for build_type in build_types:
            for target_def in workspace_def.targets:
                iface = {
                    "kind": "",
                    "definitions": {},
                    "include_dirs": [],
                    "link_libs": [],
                    "link_libs_external": [],
                    "link_libs_external_dirs": [],
                    "runtime_libs": []
                }

                impl = {
                    "kind": "",
                    "definitions": {},
                    "source_dir": "",
                    "include_dirs": [],
                    "link_libs": [],
                    "link_libs_external": [],
                    "link_libs_external_dirs": [],
                    "runtime_libs": []
                }

                target_public_include_dir_name = "include"
                target_private_include_dir_name = "src"
                target_source_dir_name = "src"

                target_public_include_path = fs.path.join(source_dir_abs_path, target_def.name,
                                                          target_public_include_dir_name)
                target_private_include_path = fs.path.join(source_dir_abs_path, target_def.name,
                                                           target_private_include_dir_name)
                target_source_dir_path = fs.path.join(source_dir_abs_path, target_def.name,
                                                      target_source_dir_name)

                iface["kind"] = target_def.kind
                impl["kind"] = target_def.kind

                iface["include_dirs"].append(target_public_include_path)
                impl["include_dirs"].append(target_public_include_path)
                impl["include_dirs"].append(target_private_include_path)
                impl["source_dir"] = target_source_dir_path

                iface["link_libs"].append(target_def.name)

                # process public section

                # Own public definitions -> interface definitions + impl definitions
                for name, value in target_def.public_props.definitions.items():
                    # TODO: resolve conflicts (A=3, A=4)
                    if name not in iface["definitions"]:
                        iface["definitions"][name] = value
                    if name not in impl["definitions"]:
                        impl["definitions"][name] = value

                for dependency in target_def.public_props.dependencies:
                    dep_iface = targets_interfaces[base.build_target_key(dependency, toolchain_name, build_type)]

                    if dep_iface["kind"] == base.TargetKind.EXECUTABLE:
                        raise RuntimeError("Cannot declare dep on an exe.")

                    for link_lib in dep_iface["link_libs"]:
                        append_unique(iface["link_libs"], link_lib)
                        append_unique(impl["link_libs"], link_lib)

                    for link_lib in dep_iface["link_libs_external"]:
                        append_unique(iface["link_libs_external"], link_lib)
                        append_unique(impl["link_libs_external"], link_lib)

                    for link_lib in dep_iface["link_libs_external_dirs"]:
                        append_unique(iface["link_libs_external_dirs"], link_lib)
                        append_unique(impl["link_libs_external_dirs"], link_lib)

                for dependency in target_def.public_props.externals:
                    dep_iface = targets_interfaces[
                        base.build_target_key(dependency, toolchain_name, build_type)]

                    for link_lib in dep_iface["link_libs_external"]:
                        append_unique(iface["link_libs_external"], link_lib)
                        append_unique(impl["link_libs_external"], link_lib)

                    for link_lib in dep_iface["link_libs_external_dirs"]:
                        append_unique(iface["link_libs_external_dirs"], link_lib)
                        append_unique(impl["link_libs_external_dirs"], link_lib)

                deps = target_def.public_props.dependencies + target_def.public_props.externals

                for dependency in deps:
                    dep_iface = targets_interfaces[base.build_target_key(dependency, toolchain_name, build_type)]

                    for name, value in dep_iface["definitions"].items():
                        # TODO: resolve conflicts (A=3, A=4)
                        if name not in iface["definitions"]:
                            iface["definitions"][name] = value
                        if name not in impl["definitions"]:
                            impl["definitions"][name] = value

                    for d in dep_iface["include_dirs"]:
                        append_unique(iface["include_dirs"], d)
                        append_unique(impl["include_dirs"], d)

                    for d in dep_iface["runtime_libs"]:
                        append_unique(iface["runtime_libs"], d)
                        # TODO: Is that a typo?
                        append_unique(impl["runtime_libs"], d)

                    if dep_iface["kind"] == base.TargetKind.DYNAMIC_LIB:
                        append_unique(iface["runtime_libs"], dependency)
                        append_unique(impl["runtime_libs"], dependency)

                # process private section

                for name, value in target_def.private_props.definitions.items():
                    # TODO: resolve conflicts (A=3, A=4)
                    if name not in impl["definitions"]:
                        impl["definitions"][name] = value

                for dependency in target_def.private_props.dependencies:
                    dep_iface = targets_interfaces[base.build_target_key(dependency, toolchain_name, build_type)]

                    if dep_iface["kind"] == base.TargetKind.EXECUTABLE:
                        raise RuntimeError("Cannot declare dep on an exe.")

                    for link_lib in dep_iface["link_libs"]:
                        append_unique(iface["link_libs"], link_lib)
                        append_unique(impl["link_libs"], link_lib)

                    for link_lib in dep_iface["link_libs_external"]:
                        append_unique(iface["link_libs_external"], link_lib)
                        append_unique(impl["link_libs_external"], link_lib)

                    for link_lib in dep_iface["link_libs_external_dirs"]:
                        append_unique(iface["link_libs_external_dirs"], link_lib)
                        append_unique(impl["link_libs_external_dirs"], link_lib)

                for dependency in target_def.private_props.externals:
                    dep_iface = targets_interfaces[base.build_target_key(dependency, toolchain_name, build_type)]

                    for link_lib in dep_iface["link_libs_external"]:
                        append_unique(iface["link_libs_external"], link_lib)
                        append_unique(impl["link_libs_external"], link_lib)

                    for link_lib in dep_iface["link_libs_external_dirs"]:
                        append_unique(iface["link_libs_external_dirs"], link_lib)
                        append_unique(impl["link_libs_external_dirs"], link_lib)

                deps = target_def.private_props.dependencies + target_def.private_props.externals

                for dependency in deps:
                    dep_iface = targets_interfaces[
                        base.build_target_key(dependency, toolchain_name, build_type)]

                    # print(json.dumps(dep_iface, indent=4))

                    for name, value in dep_iface["definitions"].items():
                        # TODO: resolve conflicts (A=3, A=4)
                        if name not in impl["definitions"]:
                            impl["definitions"][name] = value

                    for d in dep_iface["include_dirs"]:
                        append_unique(impl["include_dirs"], d)

                    for d in dep_iface["runtime_libs"]:
                        append_unique(iface["runtime_libs"], d)
                        append_unique(impl["runtime_libs"], d)

                    if dep_iface["kind"] == base.TargetKind.DYNAMIC_LIB:
                        append_unique(iface["runtime_libs"], dependency)
                        append_unique(impl["runtime_libs"], dependency)

                # save result
                target_key = base.build_target_key(target_def.name, toolchain_name, build_type)

                # Executables don't need an interface
                if target_def.kind != base.TargetKind.EXECUTABLE:
                    targets_interfaces[target_key] = iface
                targets_impls[target_key] = impl

    return targets_interfaces, targets_impls


class Workspace:
    def __init__(self, *,
                 wks_fs: FS,
                 logger: base.Logger,
                 system_config_provider: base.SystemConfigManifestProvider,
                 toolchain_settings_provider: base.ToolchainSettingsProvider,
                 build_script_emitter: base.BuildScriptEmitter
                 ):

        self.fs = wks_fs

        self.configure_dir_name = "configure"
        self.source_dir_name = "src"
        self.build_dir_name = "build"

        self.workspace_def: Union[WorkspaceDefinition, None] = None
        self.third_party_manifest: dict[str, Any] = {}
        self.toolchains_manifest: dict[str, Any] = {}

        self.build_types = [base.BUILD_TYPE_DEBUG, base.BUILD_TYPE_RELEASE]

        self.logger = logger
        self.system_config_provider = system_config_provider
        self.toolchain_settings_provider = toolchain_settings_provider
        self.build_script_emitter = build_script_emitter

    def __del__(self):
        self.fs.close()
        pass

    def _get_source_dir_path(self):
        return self.source_dir_name

    def _get_source_dir_abs_path(self):
        if self.fs.hassyspath(self.source_dir_name):
            return self.fs.getsyspath(self.source_dir_name)
        return f"wks://{self.source_dir_name}"

    def _get_configure_dir_abs_path(self):
        if self.fs.hassyspath(self.configure_dir_name):
            return self.fs.getsyspath(self.configure_dir_name)
        return f"wks://{self.configure_dir_name}"

    def _get_build_dir_abs_path(self):
        if self.fs.hassyspath(self.build_dir_name):
            return self.fs.getsyspath(self.build_dir_name)
        return f"wks://{self.build_dir_name}"

    def configure(self, *, quick_mode: bool) -> bool:

        #
        # Load workspace target definitions
        #
        targets_file_path = fs.path.join(self.source_dir_name, "rapid_targets.yml")
        self.logger.log_info(f"Reading target definitions '{targets_file_path}'...")

        try:
            with self.fs.open(targets_file_path, 'r') as f:
                targets_defs = yaml.load(f, yaml.Loader)
        except fs.errors.ResourceNotFound:
            self.logger.log_error(f"File '{targets_file_path}' does not exist.")
            return False

        try:
            self.workspace_def = WorkspaceDefinition.from_dict(targets_defs)
        except WorkspaceInvalidFormatError:
            self.logger.log_error(f"File '{targets_file_path}' is not a valid targets definition file.")
            return False

        self.logger.log_info("Workspace definition loaded.")

        # print(json.dumps(target_defs, indent=2))

        #
        # Prepare configuration directory, provide manifests
        #
        self.fs.makedir(self.configure_dir_name, recreate=True)

        self.system_config_provider.run(self._get_configure_dir_abs_path())

        self.third_party_manifest = self.system_config_provider.get_third_party_manifest()

        if not _validate_third_party_manifest(self.third_party_manifest):
            self.logger.log_error("Provided third party manifest is invalid.")
            return False

        self.toolchains_manifest = self.system_config_provider.get_toolchains_manifest()

        if not _validate_toolchains_manifest(self.toolchains_manifest):
            self.logger.log_error("Provided toolchains manifest is invalid.")
            return False

        #
        # Build targets implementations
        #
        targets_interfaces, targets_impls = _create_targets_interfaces_and_implementations(
            self._get_source_dir_abs_path(),
            self.toolchains_manifest,
            self.build_types,
            self.third_party_manifest,
            self.workspace_def
        )

        assert(isinstance(targets_interfaces, dict))
        assert(isinstance(targets_impls, dict) and len(targets_impls.keys()) != 0)

        #
        # Generate build script for targets based on implementations
        #

        build_script_filename = self.build_script_emitter.filename()
        build_script_contents = self.build_script_emitter.contents(
            self._get_build_dir_abs_path(),
            self.toolchains_manifest,
            self.toolchain_settings_provider.get_toolchain_settings(),
            self.build_types,
            [d.name for d in self.workspace_def.targets],
            targets_impls
        )

        build_script_path = fs.path.join(self.configure_dir_name, build_script_filename)

        self.logger.log_info(f"Writing build script '{build_script_path}'...")
        with self.fs.open(build_script_path, 'w') as f:
            f.write(build_script_contents)

        self.logger.log_info("Configuring done.")
        return True


def open_workspace(wks_dir: str) -> Workspace:

    wks_fs = OSFS(os.path.abspath(wks_dir))

    logger = base.LoggerDefault()

    system_config_provider = SystemConfigManifestProviderConan(
        logger=logger,
        process_runner=base.ProcessRunnerDefault(),
        conanfile_path=wks_fs.getsyspath("conanfile.py"),
        execute_conan=True,
        base_to_conan_build_type={
            base.BUILD_TYPE_DEBUG: "Debug",
            base.BUILD_TYPE_RELEASE: "Release"
        }
    )

    wks = Workspace(
        wks_fs=wks_fs,
        logger=logger,
        system_config_provider=system_config_provider,
        toolchain_settings_provider=ToolchainSettingsProviderDefault(),
        build_script_emitter=BuildScriptEmitterFastbuild()
    )
    return wks
