from __future__ import annotations

from typing import Any
import importlib.resources
import fs
import os.path
import json

from . import base
from . import conan_generator
from .data import conan_profiles


def to_rapid_os(os_name: str) -> str | None:
    if os_name == "Windows":
        return "windows"
    return None


def to_rapid_toolchain(conan_compiler: str, version: str) -> str | None:
    if conan_compiler == "Visual Studio":
        if version == "16":
            return base.TOOLCHAIN_MSVC16
    if conan_compiler == "clang":
        if version == "13":
            return base.TOOLCHAIN_LLVM13
    return None


def _generate_toolchain_msvc_from_conan_vc_vars(vc_vars):
    toolchain = {}

    generate_sdk_paths = False
    if generate_sdk_paths:
        windows_sdk_dir = base.sanitize_path(vc_vars["WindowsSdkDir"])
        windows_sdk_version = vc_vars["WindowsSDKVersion"]

        toolchain["windows_sdk_include_path"] = os.path.join(f"{windows_sdk_dir}Include", f"{windows_sdk_version}")
        toolchain["windows_sdk_lib_path"] = os.path.join(f"{windows_sdk_dir}Lib", f"{windows_sdk_version}")

    vc_tools_install_dir = base.sanitize_path(vc_vars["VCToolsInstallDir"])
    vc_host_arch = vc_vars["VSCMD_ARG_HOST_ARCH"]
    vc_target_arch = vc_vars["VSCMD_ARG_TGT_ARCH"]

    vc_bin_path = os.path.join(f"{vc_tools_install_dir}", "bin", f"Host{vc_host_arch}", f"{vc_target_arch}")
    # vc_lib_path = os.path.join(f"{vc_tools_install_dir}", "lib", f"{vc_target_arch}")
    # vc_include_path = base.sanitize_path(vc_tools_install_dir)

    toolchain["bin_path"] = vc_bin_path
    toolchain["compiler_path"] = os.path.join(vc_bin_path, "cl.exe")
    toolchain["compiler_family"] = "msvc"
    toolchain["linker_path"] = os.path.join(vc_bin_path, "link.exe")
    toolchain["librarian_path"] = os.path.join(vc_bin_path, "lib.exe")

    msvc_extra_files = [
        'c1.dll',
        'c1xx.dll',
        'c2.dll',
        'atlprov.dll',  # Only needed if using ATL
        'msobj140.dll',
        'mspdb140.dll',
        'mspdbcore.dll',
        'mspdbsrv.exe',
        'mspft140.dll',
        'msvcp140.dll',
        'tbbmalloc.dll',  # Required as of 16.2(14.22 .27905)
        'vcruntime140.dll',
        os.path.join('1033', 'clui.dll'),
        os.path.join('1033', 'mspft140ui.dll'),  # Localized messages for static analysis
    ]

    msvc_extra_files = [os.path.join(vc_bin_path, p) for p in msvc_extra_files if len(p) != 0]

    toolchain["compiler_extra_files"] = base.sanitize_paths(msvc_extra_files)
    toolchain["toolchain_include_dirs"] = base.sanitize_paths(vc_vars["INCLUDE"])
    toolchain["toolchain_lib_dirs"] = base.sanitize_paths(vc_vars["LIB"])
    return toolchain


def _generate_toolchain_llvm_from_conan_vc_vars(vc_vars):
    use_vs_embedded_llvm = False
    if use_vs_embedded_llvm:
        llvm_bin_path = os.path.join(base.sanitize_path(vc_vars["VSINSTALLDIR"]), "VC", "Tools", "Llvm", "x64", "bin")
    else:
        llvm_bin_path = os.path.join("C:\\", "Program Files", "LLVM", "bin")

    toolchain = {
        "compiler_path": os.path.join(llvm_bin_path, "clang++.exe"),
        "compiler_family": "clang",
        "linker_path": os.path.join(llvm_bin_path, "lld-link.exe"),
        "librarian_path": os.path.join(llvm_bin_path, "llvm-ar.exe"),
        "compiler_extra_files": [],
        "toolchain_include_dirs": base.sanitize_paths(vc_vars["INCLUDE"]),
        "toolchain_lib_dirs": base.sanitize_paths(vc_vars["LIB"]),
    }
    return toolchain


def get_toolchain_manifest_filename():
    return "toolchain_gen.json"


def generate_toolchain_manifest_from_conan_vc_vars(toolchain_name, vc_vars):
    if toolchain_name == base.TOOLCHAIN_MSVC16:
        toolchain = _generate_toolchain_msvc_from_conan_vc_vars(vc_vars)
    elif toolchain_name == base.TOOLCHAIN_LLVM13:
        toolchain = _generate_toolchain_llvm_from_conan_vc_vars(vc_vars)
    else:
        raise NotImplementedError("Toolchain '{}' is not implemented.".format(toolchain_name))

    toolchain_manifest = {
        toolchain_name: toolchain
    }

    return json.dumps(toolchain_manifest, indent=4)


def get_third_party_manifest_filename():
    return "third_party_gen.json"


def generate_third_party_manifest_from_conan_deps_info(deps_cpp_info):
    targets_interfaces = {}
    for dep in deps_cpp_info.deps:
        dep_cpp_info = deps_cpp_info[dep]

        dep_interface = {
            "kind": base.TargetKind.STATIC_LIB.to_string(),  # TODO: determine if lib static or dynamic
            "include_dirs": base.sanitize_paths(dep_cpp_info.include_paths),
            "definitions": {p: None for p in dep_cpp_info.defines},  # TODO: parse defines
            "link_libs": [],
            "link_libs_external": base.sanitize_paths(dep_cpp_info.libs),
            "link_libs_external_dirs": base.sanitize_paths(dep_cpp_info.lib_paths),
            "runtime_libs": [],
            "_sharedlinkflags": dep_cpp_info.sharedlinkflags,
            "_exelinkflags": dep_cpp_info.exelinkflags,
            "_system_libs": dep_cpp_info.system_libs,
            "_cxxflags": dep_cpp_info.cxxflags,
        }
        targets_interfaces[dep] = dep_interface
    return json.dumps(targets_interfaces, indent=4)


class SystemConfigManifestProviderConan(base.SystemConfigManifestProvider):
    def __init__(self, *, logger, process_runner, conanfile_path, execute_conan, base_to_conan_build_type):
        self.logger = logger
        self.process_runner = process_runner
        self.conanfile_path = conanfile_path
        self.execute_conan = execute_conan
        self.base_to_conan_build_type = base_to_conan_build_type

        self.third_party_manifest: dict[str, Any] = {}
        self.toolchains_manifest: dict[str, Any] = {}

    @staticmethod
    def install_combination_to_install_dir_name(profile_name: str, build_type: str) -> str:
        return f"{profile_name}-{build_type}"

    def run(self, working_dir_abs_path):
        supported_conan_build_types = [
            "Debug",
            "Release"
        ]

        for conan_build_type in self.base_to_conan_build_type.values():
            if conan_build_type not in supported_conan_build_types:
                raise RuntimeError(f"Unsupported conan build type '{conan_build_type}'")

        conan_export_invocation = []
        conan_export_resource = ""

        for resource in importlib.resources.contents(conan_generator):
            if resource == "conanfile.py":
                with importlib.resources.path(conan_generator, resource) as conan_generator_path:
                    conan_export_resource = resource
                    conan_export_invocation = ["conan", "export", f"{conan_generator_path}"]
                break

        if conan_export_resource == "":
            raise RuntimeError("Internal error: unable to find Conan generator resource.")

        conan_install_invocations = []
        conan_install_invocations_resources = []
        conan_install_combinations = []

        for resource in importlib.resources.contents(conan_profiles):
            profile_name, ext = fs.path.splitext(resource)
            if ext == ".txt":
                for build_type, conan_build_type in self.base_to_conan_build_type.items():

                    install_dir_name = self.install_combination_to_install_dir_name(profile_name, build_type)
                    install_dir_abs_path = fs.path.join(working_dir_abs_path, install_dir_name)

                    with importlib.resources.path(conan_profiles, resource) as profle_path:
                        argv = [
                            "conan", "install",
                            f"--profile={profle_path}",
                            "-s", f"build_type={conan_build_type}",
                            f"--install-folder={install_dir_abs_path}",
                            "--build=missing",
                            f"{self.conanfile_path}"
                        ]

                    conan_install_invocations.append(argv)
                    conan_install_invocations_resources.append(resource)
                    conan_install_combinations.append((profile_name, build_type))

        if self.execute_conan:
            abs_conan_home_path = fs.path.join(working_dir_abs_path, "conan_home")

            env = os.environ.copy()
            env["CONAN_USER_HOME"] = abs_conan_home_path

            with importlib.resources.path(conan_generator, conan_export_resource) as conan_generator_path:
                self.logger.log_info("Invoking: {}".format(" ".join(conan_export_invocation)))
                self.process_runner.run(conan_export_invocation, env=env, check=True)

            for args, resource in zip(conan_install_invocations, conan_install_invocations_resources):
                self.logger.log_info("Invoking: {}".format(" ".join(argv)))
                with importlib.resources.path(conan_profiles, resource) as _:
                    self.process_runner.run(args, env=env, check=True)

        with fs.open_fs(working_dir_abs_path) as work_fs:
            for profile_name, build_type in conan_install_combinations:
                install_dir_name = self.install_combination_to_install_dir_name(profile_name, build_type)

                path = fs.path.join(install_dir_name, get_toolchain_manifest_filename())
                if not work_fs.exists(path):
                    raise RuntimeError(f"Expected file '{path}' does not exist.")

                path = fs.path.join(install_dir_name, get_third_party_manifest_filename())
                if not work_fs.exists(path):
                    raise RuntimeError(f"Expected file '{path}' does not exist.")

            for profile_name, build_type in conan_install_combinations:
                install_dir_name = self.install_combination_to_install_dir_name(profile_name, build_type)

                toolchains_manifest_path = fs.path.join(install_dir_name, get_toolchain_manifest_filename())
                with work_fs.open(toolchains_manifest_path, "r") as f:
                    manifest = json.load(f)

                for k, v in manifest.items():
                    if k not in self.toolchains_manifest.keys():
                        self.toolchains_manifest[k] = v

                third_party_manifest_path = fs.path.join(install_dir_name, get_third_party_manifest_filename())
                with work_fs.open(third_party_manifest_path, "r") as f:
                    manifest = json.load(f)

                toolchain_name = profile_name.split("-")[-1]  # TODO

                for k, v in manifest.items():
                    iface_key = base.build_target_key(k, toolchain_name, build_type)
                    assert (iface_key not in self.third_party_manifest.keys())
                    self.third_party_manifest[iface_key] = v

    def get_toolchains_manifest(self):
        return self.toolchains_manifest

    def get_third_party_manifest(self):
        return self.third_party_manifest
