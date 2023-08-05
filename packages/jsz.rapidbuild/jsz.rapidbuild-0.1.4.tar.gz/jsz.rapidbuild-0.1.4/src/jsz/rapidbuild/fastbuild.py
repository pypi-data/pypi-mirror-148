from contextlib import contextmanager
from typing import Any
import fs

from . import base


class BFFEmitter:
    GENERATED_FILE_HEADER = [
        "/////////////////////////////////////////////////////////////",
        "// This is a generated file, all manual changes will be lost!",
        "/////////////////////////////////////////////////////////////",
    ]
    INDENT_SIZE = 4

    def __init__(self):
        self._lines = []
        self._indent_level = 0

        for line in self.GENERATED_FILE_HEADER:
            self._emit_line(line)

    def _indent(self):
        self._indent_level += 1

    def _dedent(self):
        assert self._indent_level > 0
        self._indent_level -= 1

    def _emit_line(self, content: str):
        if len(content) != 0:
            self._lines.append("{}{}".format(' ' * self._indent_level * self.INDENT_SIZE, content))
        else:
            self._lines.append("")

    def _emit_array(self, name: str, values: list):
        self._emit_line(".{} = ".format(name))
        self._emit_line("{")
        self._indent()
        for v in values:
            self._emit_line("{},".format(self._format_value(v, can_split_str=False)))
        self._dedent()
        self._emit_line("}")

    def _emit_struct(self, name: str, dictionary: dict):
        self._emit_line(".{} = ".format(name))
        self._emit_line("[")
        self._indent()
        for key, value in dictionary.items():
            self.emit_var_assignment(key, value)
        self._dedent()
        self._emit_line("]")

    def _begin_function(self, fn_name: str, args: str):
        self._emit_line("{}('{}')".format(fn_name, args))
        self._emit_line("{")
        self._indent()

    def _end_function(self):
        self._dedent()
        self._emit_line("}")
        self._emit_line("")

    def once(self):
        self._emit_line("#once")

    def include(self, path: str):
        self._emit_line("#include \"{}\"".format(path))

    def line_break(self):
        self._emit_line("")

    def emit_var_assignment(self, name: str, value, *, should_split_str=False):
        if type(value) == list:
            self._emit_array(name, value)
        elif type(value) == dict:
            self._emit_struct(name, value)
        else:
            self._emit_line(".{} = {}".format(name, self._format_value(value, can_split_str=should_split_str)))

    @contextmanager
    def library(self, name: str):
        self._begin_function("Library", name)
        yield
        self._end_function()

    @contextmanager
    def object_list(self, name: str):
        self._begin_function("ObjectList", name)
        yield
        self._end_function()

    @contextmanager
    def dll(self, name: str):
        self._begin_function("DLL", name)
        yield
        self._end_function()

    @contextmanager
    def exe(self, name: str):
        self._begin_function("Executable", name)
        yield
        self._end_function()

    @contextmanager
    def alias(self, name: str):
        self._begin_function("Alias", name)
        yield
        self._end_function()

    @contextmanager
    def copy_dir(self, name: str):
        self._begin_function("CopyDir", name)
        yield
        self._end_function()

    @contextmanager
    def compiler(self, name: str):
        self._begin_function("Compiler", name)
        yield
        self._end_function()

    def build(self):
        return "\n".join(self._lines)

    def _format_value(self, value, *, can_split_str):

        def format_default(v):
            return "{}".format(v)

        def str_smart_split(s: str):
            splits = []
            inside_quoted = False
            delim = " "
            curr = ""
            for c in s:
                if not inside_quoted:
                    if c == "\"":
                        inside_quoted = True
                        curr += c
                    elif c == delim:
                        splits.append(curr)
                        curr = delim
                    else:
                        curr += c
                else:
                    if c == "\"":
                        inside_quoted = False
                        curr += c
                    else:
                        curr += c
            if len(curr) != 0:
                splits.append(curr)
            return splits

        def format_string(s: str):
            if len(s) == 0:
                return "''"

            if not can_split_str:
                return f"'{s}'"

            lines = []
            col_limit = 80

            if len(s) > col_limit:
                lines = str_smart_split(s)
            else:
                lines.append(s)

            result = ""
            result += "'{}'".format(lines[0])
            if len(lines) > 1:
                for line in lines[1:]:
                    result += f"\n{' ' * (self._indent_level + 1) * self.INDENT_SIZE}+ '{line}'"
            return result

        def format_bool(b: bool):
            return "true" if b else "false"

        formatters = {
            str: format_string,
            bool: format_bool,
        }

        f = formatters.get(type(value), format_default)
        return f(value)


def format_compiler_node_name(toolchain_name: str) -> str:
    return f"compiler-{toolchain_name}"


def format_target_node_name(target_name: str, toolchain_name: str, build_type_name: str) -> str:
    return f"{target_name}-{toolchain_name}-{build_type_name}"


def format_definition_compiler_arg_msvc(name: str, value: Any) -> str:
    if value is not None:
        return f"/D\"{name}={value}\""
    else:
        return f"/D\"{name}\""


def format_include_dir_compiler_arg_msvc(include_dir: str) -> str:
    return f"/I\"{include_dir}\""


def format_definition_compiler_arg_llvm(name: str, value: Any) -> str:
    if value is not None:
        return f"-D\"{name}={value}\""
    else:
        return f"-D\"{name}\""


def format_include_dir_compiler_arg_llvm(include_dir: str) -> str:
    return f"-I\"{include_dir}\""


def format_lib_dir_linker_arg_msvc(include_dir: str) -> str:
    return f"/libpath:\"{include_dir}\""


def format_lib_dir_linker_arg_llvm(include_dir: str) -> str:
    return f"/libpath:\"{include_dir}\""


class BuildScriptEmitterFastbuild(base.BuildScriptEmitter):
    ALL_TARGETS_TARGET_NAME = "rapid_all"

    def filename(self):
        return "fbuild.bff"

    def contents(self, build_dir_abs_path, toolchains_manifest, toolchains_settings, build_types, targets_names,
                 targets_impls) -> str:

        intermediate_dir_abs_path = fs.path.join(build_dir_abs_path, "intermediate")
        deploy_dir_abs_path = fs.path.join(build_dir_abs_path, "bin")

        out_bff = BFFEmitter()
        out_bff.once()

        for toolchain_name, toolchain_def in toolchains_manifest.items():
            with out_bff.compiler(format_compiler_node_name(toolchain_name)):
                out_bff.emit_var_assignment("Executable", toolchain_def["compiler_path"])
                out_bff.emit_var_assignment("CompilerFamily", toolchain_def["compiler_family"])
                out_bff.emit_var_assignment("ExtraFiles", toolchain_def["compiler_extra_files"])

        include_dir_compiler_arg_formatters = {
            base.TOOLCHAIN_MSVC16: format_include_dir_compiler_arg_msvc,
            base.TOOLCHAIN_LLVM13: format_include_dir_compiler_arg_llvm,
        }

        preprocessor_definition_compiler_arg_formatters = {
            base.TOOLCHAIN_MSVC16: format_definition_compiler_arg_msvc,
            base.TOOLCHAIN_LLVM13: format_definition_compiler_arg_llvm,
        }

        lib_dir_linker_arg_formatters = {
            base.TOOLCHAIN_MSVC16: format_lib_dir_linker_arg_msvc,
            base.TOOLCHAIN_LLVM13: format_lib_dir_linker_arg_llvm,
        }

        all_deploy_nodes: list[str] = []
        per_toolchain_deploy_nodes: dict[str, list[str]] = {toolchain_name: [] for toolchain_name in
                                                            toolchains_manifest.keys()}
        per_build_type_deploy_nodes: dict[str, list[str]] = {build_type: [] for build_type in build_types}

        for toolchain_name, toolchain_def in toolchains_manifest.items():

            format_definition_compiler_arg = preprocessor_definition_compiler_arg_formatters[toolchain_name]
            format_include_dir_compiler_arg = include_dir_compiler_arg_formatters[toolchain_name]
            format_lib_dir_linker_arg = lib_dir_linker_arg_formatters[toolchain_name]

            toolchain_include_dirs = toolchain_def["toolchain_include_dirs"]
            toolchain_lib_dirs = toolchain_def["toolchain_lib_dirs"]

            current_toolchain_settings = toolchains_settings[toolchain_name]
            toolchain_definitions = current_toolchain_settings["definitions"]
            toolchain_compiler_args = current_toolchain_settings["compiler_args"]
            toolchain_linker_args = current_toolchain_settings["linker_args"]
            toolchain_link_libs = current_toolchain_settings["link_libs"]

            for build_type in build_types:

                toolchain_build_type_definitions = toolchain_definitions["all"] | toolchain_definitions[build_type]
                toolchain_build_type_compiler_args = toolchain_compiler_args["all"] + toolchain_compiler_args[
                    build_type]
                toolchain_build_type_linker_args = toolchain_linker_args["all"] + toolchain_linker_args[build_type]
                toolchain_build_type_link_libs = toolchain_link_libs["all"] + toolchain_link_libs[build_type]

                for target_name in targets_names:

                    target_impl = targets_impls[base.build_target_key(target_name, toolchain_name, build_type)]
                    target_node_name = format_target_node_name(target_name, toolchain_name, build_type)

                    target_kind = target_impl["kind"]

                    target_source_dir_path = target_impl["source_dir"]
                    target_source_dir_glob_pattern = ["*.c", "*.cpp", "*.cxx"]
                    target_output_dir_path = fs.path.join(intermediate_dir_abs_path, target_node_name)

                    def build_compiler_options():
                        compiler_options = []

                        if toolchain_name == base.TOOLCHAIN_MSVC16:
                            intermediate_pdb_path = fs.path.join(target_output_dir_path, f"{target_node_name}-lib.pdb")
                            compiler_options += ["/nologo", "/c", "\"%1\"", "/Fo\"%2\"",
                                                 f"/Fd\"{intermediate_pdb_path}\""]
                        elif toolchain_name == base.TOOLCHAIN_LLVM13:
                            compiler_options += ["-c", "%1", "-o", "%2"]
                        else:
                            raise RuntimeError("unsupported toolchain")

                        compiler_options += toolchain_build_type_compiler_args
                        compiler_options += [format_include_dir_compiler_arg(include_dir)
                                             for include_dir in toolchain_include_dirs]
                        compiler_options += [format_definition_compiler_arg(name, value)
                                             for name, value in toolchain_build_type_definitions.items()]

                        compiler_options += [format_include_dir_compiler_arg(include_dir)
                                             for include_dir in target_impl["include_dirs"]]
                        compiler_options += [format_definition_compiler_arg(name, value)
                                             for name, value in target_impl["definitions"].items()]
                        return compiler_options

                    def build_linker_options(*, dll=False):
                        linker_options = []

                        output_pdb_path = fs.path.join(target_output_dir_path, f"{target_node_name}.pdb")

                        if toolchain_name == base.TOOLCHAIN_MSVC16:
                            linker_options += ["/nologo", "\"%1\"", "/out:\"%2\"", f"/pdb:\"{output_pdb_path}\""]
                            if dll:
                                linker_options += ["/dll"]
                        elif toolchain_name == base.TOOLCHAIN_LLVM13:
                            linker_options += ["/nologo", "\"%1\"", "/out:\"%2\"", f"/pdb:\"{output_pdb_path}\""]
                            if dll:
                                linker_options += ["/dll"]
                        else:
                            raise RuntimeError("unsupported toolchain")

                        linker_options += toolchain_build_type_linker_args

                        linker_options += toolchain_build_type_link_libs
                        linker_options += [format_lib_dir_linker_arg(lib_dir)
                                           for lib_dir in toolchain_lib_dirs]

                        # External libs are added manully, not through "Libraries" variable.
                        # If the extension is skipped, fastbuild tries to use "obj"
                        linker_options += [f"{lib}.lib"
                                           for lib in target_impl["link_libs_external"]]
                        linker_options += [format_lib_dir_linker_arg(lib_dir)
                                           for lib_dir in target_impl["link_libs_external_dirs"]]

                        return linker_options

                    def build_librarian_options():
                        librarian_options = []

                        if toolchain_name == base.TOOLCHAIN_MSVC16:
                            librarian_options += ["/NOLOGO", "/MACHINE:X64", "/WX", "\"%1\"", "/OUT:\"%2\""]
                        elif toolchain_name == base.TOOLCHAIN_LLVM13:
                            librarian_options += ["rc", "%2", "%1"]
                        else:
                            raise RuntimeError("unsupported toolchain")

                        return librarian_options

                    if target_kind == base.TargetKind.STATIC_LIB:

                        compiler_options = build_compiler_options()
                        compiler_input_path = target_source_dir_path
                        compiler_input_pattern = target_source_dir_glob_pattern
                        compiler_output_path = target_output_dir_path

                        librarian_options = build_librarian_options()
                        librarian_output_path = fs.path.join(target_output_dir_path, f"{target_node_name}.lib")

                        with out_bff.library(target_node_name):
                            out_bff.emit_var_assignment("Compiler", format_compiler_node_name(toolchain_name))
                            out_bff.emit_var_assignment("CompilerInputPath", compiler_input_path)
                            out_bff.emit_var_assignment("CompilerInputPathRecurse", True)
                            out_bff.emit_var_assignment("CompilerInputPattern", compiler_input_pattern)
                            out_bff.emit_var_assignment("CompilerOutputPath", compiler_output_path)
                            out_bff.emit_var_assignment("CompilerOptions", " ".join(compiler_options),
                                                        should_split_str=True)
                            out_bff.line_break()
                            out_bff.emit_var_assignment("Librarian", toolchain_def["librarian_path"])
                            out_bff.emit_var_assignment("LibrarianOutput", librarian_output_path)
                            out_bff.emit_var_assignment("LibrarianOptions", " ".join(librarian_options),
                                                        should_split_str=True)

                        deploy_target_name = f"deploy-{target_node_name}"
                        with out_bff.alias(deploy_target_name):
                            out_bff.emit_var_assignment("Targets", target_node_name)

                        all_deploy_nodes.append(deploy_target_name)
                        per_build_type_deploy_nodes[build_type].append(deploy_target_name)
                        per_toolchain_deploy_nodes[toolchain_name].append(deploy_target_name)

                    elif target_kind == base.TargetKind.DYNAMIC_LIB:

                        compiler_options = build_compiler_options()
                        compiler_input_path = target_source_dir_path
                        compiler_input_pattern = target_source_dir_glob_pattern
                        compiler_output_path = target_output_dir_path

                        object_list_node_name = f"obj-{target_node_name}"

                        with out_bff.object_list(object_list_node_name):
                            out_bff.emit_var_assignment("Hidden", True)
                            out_bff.emit_var_assignment("Compiler", format_compiler_node_name(toolchain_name))
                            out_bff.emit_var_assignment("CompilerInputPath", compiler_input_path)
                            out_bff.emit_var_assignment("CompilerInputPathRecurse", True)
                            out_bff.emit_var_assignment("CompilerInputPattern", compiler_input_pattern)
                            out_bff.emit_var_assignment("CompilerOutputPath", compiler_output_path)
                            out_bff.emit_var_assignment("CompilerOptions", " ".join(compiler_options),
                                                        should_split_str=True)

                        #
                        linker_output_path = fs.path.join(target_output_dir_path, f"{target_node_name}.dll")

                        libraries = [object_list_node_name]
                        libraries += [format_target_node_name(lib, toolchain_name, build_type)
                                      for lib in target_impl["link_libs"]]

                        linker_options = build_linker_options(dll=True)

                        with out_bff.dll(target_node_name):
                            out_bff.emit_var_assignment("Libraries", libraries)
                            out_bff.emit_var_assignment("Linker", toolchain_def["linker_path"])
                            out_bff.emit_var_assignment("LinkerOutput", linker_output_path)
                            out_bff.emit_var_assignment("LinkerOptions", " ".join(linker_options),
                                                        should_split_str=True)

                        #
                        prebuild_deps = [target_node_name]
                        prebuild_deps += [f"deploy-{format_target_node_name(lib, toolchain_name, build_type)}"
                                          for lib in target_impl["runtime_libs"]]

                        deploy_target_name = f"deploy-{target_node_name}"
                        with out_bff.copy_dir(deploy_target_name):
                            out_bff.emit_var_assignment("PreBuildDependencies", prebuild_deps)
                            out_bff.emit_var_assignment("SourcePaths", target_output_dir_path)
                            out_bff.emit_var_assignment("SourcePathsPattern", ["*.dll", "*.pdb"])
                            out_bff.emit_var_assignment("Dest", deploy_dir_abs_path)

                        all_deploy_nodes.append(deploy_target_name)
                        per_build_type_deploy_nodes[build_type].append(deploy_target_name)
                        per_toolchain_deploy_nodes[toolchain_name].append(deploy_target_name)

                    elif target_kind == base.TargetKind.EXECUTABLE:

                        compiler_options = build_compiler_options()
                        compiler_input_path = target_source_dir_path
                        compiler_input_pattern = target_source_dir_glob_pattern
                        compiler_output_path = target_output_dir_path

                        object_list_node_name = f"obj-{target_node_name}"

                        with out_bff.object_list(object_list_node_name):
                            out_bff.emit_var_assignment("Hidden", True)
                            out_bff.emit_var_assignment("Compiler", format_compiler_node_name(toolchain_name))
                            out_bff.emit_var_assignment("CompilerInputPath", compiler_input_path)
                            out_bff.emit_var_assignment("CompilerInputPathRecurse", True)
                            out_bff.emit_var_assignment("CompilerInputPattern", compiler_input_pattern)
                            out_bff.emit_var_assignment("CompilerOutputPath", compiler_output_path)
                            out_bff.emit_var_assignment("CompilerOptions", " ".join(compiler_options),
                                                        should_split_str=True)

                        #
                        linker_output_path = fs.path.join(target_output_dir_path, f"{target_node_name}.exe")

                        libraries = [object_list_node_name]
                        libraries += [format_target_node_name(lib, toolchain_name, build_type)
                                      for lib in target_impl["link_libs"]]

                        linker_options = build_linker_options(dll=False)

                        with out_bff.exe(target_node_name):
                            out_bff.emit_var_assignment("Libraries", libraries)
                            out_bff.emit_var_assignment("Linker", toolchain_def["linker_path"])
                            out_bff.emit_var_assignment("LinkerOutput", linker_output_path)
                            out_bff.emit_var_assignment("LinkerOptions", " ".join(linker_options),
                                                        should_split_str=True)

                        #
                        prebuild_deps = [target_node_name]
                        prebuild_deps += [f"deploy-{format_target_node_name(lib, toolchain_name, build_type)}"
                                          for lib in target_impl["runtime_libs"]]

                        deploy_target_name = f"deploy-{target_node_name}"
                        with out_bff.copy_dir(deploy_target_name):
                            out_bff.emit_var_assignment("PreBuildDependencies", prebuild_deps)
                            out_bff.emit_var_assignment("SourcePaths", target_output_dir_path)
                            out_bff.emit_var_assignment("SourcePathsPattern", ["*.exe", "*.pdb"])
                            out_bff.emit_var_assignment("Dest", deploy_dir_abs_path)

                        all_deploy_nodes.append(deploy_target_name)
                        per_build_type_deploy_nodes[build_type].append(deploy_target_name)
                        per_toolchain_deploy_nodes[toolchain_name].append(deploy_target_name)

                    else:
                        raise RuntimeError("unsupported target kind")

        for build_type, deploy_nodes in per_build_type_deploy_nodes.items():
            build_type_all_targets_node_name = f"{self.ALL_TARGETS_TARGET_NAME}-{build_type}"

            with out_bff.alias(build_type_all_targets_node_name):
                out_bff.emit_var_assignment("Hidden", True)
                out_bff.emit_var_assignment("Targets", deploy_nodes)

            with out_bff.alias(f"deploy-{build_type_all_targets_node_name}"):
                out_bff.emit_var_assignment("Targets", build_type_all_targets_node_name)

        for toolchain_name, deploy_nodes in per_toolchain_deploy_nodes.items():
            toolchain_all_targets_node_name = f"{self.ALL_TARGETS_TARGET_NAME}-{toolchain_name}"

            with out_bff.alias(toolchain_all_targets_node_name):
                out_bff.emit_var_assignment("Hidden", True)
                out_bff.emit_var_assignment("Targets", deploy_nodes)

            with out_bff.alias(f"deploy-{toolchain_all_targets_node_name}"):
                out_bff.emit_var_assignment("Targets", toolchain_all_targets_node_name)

        all_targets_node_name = f"{self.ALL_TARGETS_TARGET_NAME}"

        with out_bff.alias(all_targets_node_name):
            out_bff.emit_var_assignment("Hidden", True)
            out_bff.emit_var_assignment("Targets", all_deploy_nodes)

        with out_bff.alias(f"deploy-{all_targets_node_name}"):
            out_bff.emit_var_assignment("Targets", all_targets_node_name)

        return out_bff.build()
