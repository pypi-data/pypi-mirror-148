import abc
from contextlib import contextmanager
from enum import Enum, auto
from pathlib import Path
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

    def _emit_array(self, name: str, values: list, *, should_split_str=False):
        self._emit_line(".{} = ".format(name))
        self._emit_line("{")
        self._indent()
        for v in values:
            self._emit_line("{},".format(self._format_value(v, should_split_str=should_split_str)))
        self._dedent()
        self._emit_line("}")

    def _emit_struct(self, name: str, dictionary: dict, *, should_split_str=False):
        self._emit_line(".{} = ".format(name))
        self._emit_line("[")
        self._indent()
        for key, value in dictionary.items():
            self.emit_var_assignment(key, value, should_split_str=should_split_str)
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
            self._emit_line(".{} = {}".format(name, self._format_value(value, should_split_str=should_split_str)))

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

    @contextmanager
    def vcxproject(self, name: str):
        self._begin_function("VCXProject", name)
        yield
        self._end_function()

    @contextmanager
    def vssolution(self, name: str):
        self._begin_function("VSSolution", name)
        yield
        self._end_function()

    def build(self):
        return "\n".join(self._lines)

    def _format_value(self, value, *, should_split_str):

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

            if not should_split_str:
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


def format_obj_node_name(target_node_name: str):
    return f"obj-{target_node_name}"


def format_build_node_name(target_node_name: str):
    return f"make-{target_node_name}"


def format_deploy_node_name(target_node_name: str):
    return f"deploy-{target_node_name}"


class CompilerFamily(Enum):
    MSVC = auto()
    CLANG = auto()
    CLANG_CL = auto()
    GCC = auto()


class CouldNotDetermineCompilerFamily(RuntimeError):
    pass


def compiler_family_to_fastbuild_value(f: CompilerFamily):
    return {
        CompilerFamily.MSVC: "msvc",
        CompilerFamily.CLANG: "clang",
        CompilerFamily.CLANG_CL: "clang-cl",
        CompilerFamily.GCC: "gcc"
    }[f]


def guess_compiler_family_from_compiler_path(path: str) -> CompilerFamily:
    filename = Path(path).parts[-1]
    if filename == "cl" or filename == "cl.exe":
        return CompilerFamily.MSVC
    if filename == "clang" or filename == "clang.exe" or filename == "clang++" or filename == "clang++.exe":
        return CompilerFamily.CLANG
    if filename == "clang-cl" or filename == "clang-cl.exe":
        return CompilerFamily.CLANG_CL
    if filename == "gcc":
        return CompilerFamily.GCC
    raise CouldNotDetermineCompilerFamily(f"compiler path: {path}")


class CompilerArgFormatter(abc.ABC):
    @abc.abstractmethod
    def format_input_output_args(self, output_dir_path: str, output_base_name) -> list[str]:
        pass

    @abc.abstractmethod
    def format_definition_compiler_arg(self, name: str, value: Any) -> str:
        pass

    @abc.abstractmethod
    def format_include_dir_arg(self, include_dir: str) -> str:
        pass


class CompilerArgFormatterMSVC(CompilerArgFormatter):
    def format_input_output_args(self, output_dir_path: str, output_base_name) -> list[str]:
        intermediate_pdb_path = fs.path.join(output_dir_path, f"{output_base_name}-lib.pdb")
        return ["/nologo", "/c", "\"%1\"", "/Fo\"%2\"", f"/Fd\"{intermediate_pdb_path}\""]

    def format_definition_compiler_arg(self, name: str, value: Any) -> str:
        if value is not None:
            return f"/D\"{name}={value}\""
        else:
            return f"/D\"{name}\""

    def format_include_dir_arg(self, include_dir: str) -> str:
        return f"/I\"{include_dir}\""


class CompilerArgFormatterClang(CompilerArgFormatter):
    def format_input_output_args(self, output_dir_path: str, output_base_name) -> list[str]:
        return ["-c", "%1", "-o", "%2"]

    def format_definition_compiler_arg(self, name: str, value: Any) -> str:
        if value is not None:
            return f"-D\"{name}={value}\""
        else:
            return f"-D\"{name}\""

    def format_include_dir_arg(self, include_dir: str) -> str:
        return f"-I\"{include_dir}\""


class CompilerArgFormatterGCC(CompilerArgFormatterClang):
    pass


class CompilerArgFormatterClangCL(CompilerArgFormatterMSVC):
    pass


def create_compiler_arg_formatter(f: CompilerFamily) -> CompilerArgFormatter:
    return {
        CompilerFamily.MSVC: CompilerArgFormatterMSVC(),
        CompilerFamily.CLANG: CompilerArgFormatterClang(),
        CompilerFamily.CLANG_CL: CompilerArgFormatterClangCL(),
        CompilerFamily.GCC: CompilerArgFormatterGCC()
    }[f]


def build_compiler_options(
        arg_formatter: CompilerArgFormatter,
        output_dir_path: str, output_base_name: str,
        base_args: list[str],
        base_include_dirs: list[str], base_definitions: dict[str, Any],
        target_include_dirs: list[str], target_definitions: dict[str, Any],
):
    args = arg_formatter.format_input_output_args(output_dir_path, output_base_name)
    args += base_args
    args += [arg_formatter.format_include_dir_arg(include_dir) for include_dir in base_include_dirs]
    args += [arg_formatter.format_definition_compiler_arg(name, value) for name, value in base_definitions.items()]
    args += [arg_formatter.format_include_dir_arg(include_dir) for include_dir in target_include_dirs]
    args += [arg_formatter.format_definition_compiler_arg(name, value) for name, value in target_definitions.items()]
    return args


class LibrarianFamily(Enum):
    MSVC = auto()
    LLVM = auto()
    GCC = auto()


class CouldNotDetermineLibrarianFamily(RuntimeError):
    pass


def guess_librarian_family_from_path(path: str) -> LibrarianFamily:
    filename = Path(path).parts[-1]
    if filename == "lib" or filename == "lib.exe":
        return LibrarianFamily.MSVC
    if filename == "llvm-ar" or filename == "llvm-ar.exe":
        return LibrarianFamily.LLVM
    if filename == "ar" or filename == "ar.exe":
        return LibrarianFamily.GCC
    raise CouldNotDetermineLibrarianFamily(f"librarian path: {path}")


class LibrarianArgFormatter(abc.ABC):
    @abc.abstractmethod
    def format_input_output_args(self) -> list[str]:
        pass


class LibrarianArgFormatterMSVC(LibrarianArgFormatter):
    def format_input_output_args(self) -> list[str]:
        return ["/NOLOGO", "/MACHINE:X64", "/WX", "\"%1\"", "/OUT:\"%2\""]


class LibrarianArgFormatterLLVM(LibrarianArgFormatter):
    def format_input_output_args(self) -> list[str]:
        return ["rc", "%2", "%1"]


class LibrarianArgFormatterGCC(LibrarianArgFormatterLLVM):
    pass


def create_librarian_arg_formatter(f: LibrarianFamily):
    return {
        LibrarianFamily.MSVC: LibrarianArgFormatterMSVC(),
        LibrarianFamily.LLVM: LibrarianArgFormatterLLVM(),
        LibrarianFamily.GCC: LibrarianArgFormatterGCC(),
    }[f]


def build_librarian_options(arg_formatter: LibrarianArgFormatter):
    return arg_formatter.format_input_output_args()


class LinkerFamily(Enum):
    LINK = auto()
    LLD_LINK = auto()
    LD_LLD = auto()
    LD = auto()


class CouldNotDetermineLinkerFamily(RuntimeError):
    pass


def guess_linker_family_from_path(path: str) -> LinkerFamily:
    filename = Path(path).parts[-1]
    if filename == "link" or filename == "link.exe":
        return LinkerFamily.LINK
    if filename == "lld-link" or filename == "lld-link.exe":
        return LinkerFamily.LLD_LINK
    if filename == "ld.lld" or filename == "ld.lld.exe":
        return LinkerFamily.LD_LLD
    if filename == "ld" or filename == "ld.exe":
        return LinkerFamily.LD
    raise CouldNotDetermineLinkerFamily(f"linker path: {path}")


class LinkerArgFormatter(abc.ABC):
    @abc.abstractmethod
    def format_input_output_declaration(
            self, output_dir_path: str, output_base_name: str, target_kind: base.TargetKind
    ) -> list[str]:
        pass

    @abc.abstractmethod
    def format_lib_arg(self, lib: str) -> str:
        pass

    @abc.abstractmethod
    def format_lib_dir_arg(self, lib_dir: str) -> str:
        pass


class LinkerArgFormatterLink(LinkerArgFormatter):
    def format_input_output_declaration(
            self, output_dir_path: str, output_base_name: str, target_kind: base.TargetKind
    ) -> list[str]:
        output_pdb_path = fs.path.join(output_dir_path, f"{output_base_name}-lib.pdb")
        args = ["/nologo", "\"%1\"", "/out:\"%2\"", f"/pdb:\"{output_pdb_path}\""]
        if target_kind == base.TargetKind.DYNAMIC_LIB:
            args += ["/dll"]
        return args

    def format_lib_arg(self, lib: str) -> str:
        return lib

    def format_lib_dir_arg(self, lib_dir: str) -> str:
        return f"/libpath:\"{lib_dir}\""


class LinkerArgFormatterLLDLink(LinkerArgFormatterLink):
    pass


class LinkerArgFormatterLDLLD(LinkerArgFormatter):
    def format_input_output_declaration(
            self, output_dir_path: str, output_base_name: str, target_kind: base.TargetKind
    ) -> list[str]:
        args = ["\"%1\"", "-o \"%2\""]
        if target_kind == base.TargetKind.DYNAMIC_LIB:
            args += ["--shared"]
        return args

    def format_lib_arg(self, lib: str) -> str:
        return f"-l\"{lib}\""

    def format_lib_dir_arg(self, lib_dir: str) -> str:
        return f"-L\"{lib_dir}\""


class LinkerArgFormatterLD(LinkerArgFormatterLDLLD):
    pass


def create_linker_arg_formatter(f: LinkerFamily):
    return {
        LinkerFamily.LINK: LinkerArgFormatterLink(),
        LinkerFamily.LLD_LINK: LinkerArgFormatterLLDLink(),
        LinkerFamily.LD_LLD: LinkerArgFormatterLDLLD(),
        LinkerFamily.LD: LinkerArgFormatterLD()
    }[f]


def build_linker_options(
        arg_formatter: LinkerArgFormatter,
        output_dir_path: str, output_base_name: str, output_target_kind: base.TargetKind,
        base_args: list[str],
        base_link_libs: list[str], base_lib_dirs: list[str],
        external_link_libs: list[str], external_lib_dirs: list[str]
):
    if output_target_kind != base.TargetKind.DYNAMIC_LIB and output_target_kind != base.TargetKind.EXECUTABLE:
        raise RuntimeError()
    
    args = arg_formatter.format_input_output_declaration(output_dir_path, output_base_name, output_target_kind)
    args += base_args
    args += [arg_formatter.format_lib_arg(lib) for lib in base_link_libs]
    args += [arg_formatter.format_lib_dir_arg(lib_dir) for lib_dir in base_lib_dirs]
    # External libs are added manully, not through "Libraries" variable.
    # If the extension is skipped, fastbuild tries to use "obj"
    args += [arg_formatter.format_lib_arg(f"{lib}.lib") for lib in external_link_libs]
    args += [arg_formatter.format_lib_dir_arg(lib_dir) for lib_dir in external_lib_dirs]

    return args


class BuildScriptEmitterFastbuild(base.BuildScriptEmitter):
    ALL_TARGETS_TARGET_NAME = "rapid_all"

    def filename(self):
        return "fbuild.bff"

    # noinspection PyUnreachableCode
    def contents(self, source_dir_abs_path, configure_dir_abs_path, build_dir_abs_path,
                 toolchains_manifest, toolchains_settings, build_types, targets_names, targets_impls) -> str:

        intermediate_dir_abs_path = fs.path.join(build_dir_abs_path, "intermediate")
        deploy_dir_abs_path = fs.path.join(build_dir_abs_path, "bin")

        out_bff = BFFEmitter()
        out_bff.once()

        for toolchain_name, toolchain_def in toolchains_manifest.items():
            with out_bff.compiler(format_compiler_node_name(toolchain_name)):
                compiler_path = toolchain_def["compiler_path"]
                compiler_family = guess_compiler_family_from_compiler_path(compiler_path)

                out_bff.emit_var_assignment("Executable", compiler_path)
                out_bff.emit_var_assignment("CompilerFamily", compiler_family_to_fastbuild_value(compiler_family))
                out_bff.emit_var_assignment("ExtraFiles", toolchain_def["compiler_extra_files"])

        all_nodes: list[str] = []
        per_toolchain_nodes: dict[str, list[str]] = {
            toolchain_name: [] for toolchain_name in toolchains_manifest.keys()
        }
        per_build_type_nodes: dict[str, list[str]] = {
            build_type: [] for build_type in build_types
        }
        config_vector_nodes: dict[str, dict[str, list[str]]] = {
            toolchain_name: {
                build_type: [] for build_type in build_types
            } for toolchain_name in toolchains_manifest.keys()
        }

        for toolchain_name, toolchain_def in toolchains_manifest.items():

            toolchain_compiler_family = guess_compiler_family_from_compiler_path(toolchain_def["compiler_path"])
            toolchain_librarian_family = guess_librarian_family_from_path(toolchain_def["librarian_path"])
            toolchain_linker_family = guess_linker_family_from_path(toolchain_def["linker_path"])

            compiler_arg_formatter = create_compiler_arg_formatter(toolchain_compiler_family)
            librarian_arg_formatter = create_librarian_arg_formatter(toolchain_librarian_family)
            linker_arg_formatter = create_linker_arg_formatter(toolchain_linker_family)
            
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

                    target_output_dir_path = fs.path.join(intermediate_dir_abs_path, target_node_name)

                    compiler_options = build_compiler_options(
                        compiler_arg_formatter, target_output_dir_path, target_node_name,
                        toolchain_build_type_compiler_args,
                        toolchain_include_dirs, toolchain_build_type_definitions,
                        target_impl["include_dirs"], target_impl["definitions"]
                    )
                    compiler_input_path = target_impl["source_dir"]
                    compiler_input_pattern = ["*.c", "*.cpp", "*.cxx"]
                    
                    if target_kind == base.TargetKind.STATIC_LIB:

                        librarian_options = build_librarian_options(librarian_arg_formatter)
                        librarian_output_path = fs.path.join(target_output_dir_path, f"{target_node_name}.lib")

                        make_node_name = format_build_node_name(target_node_name)
                        with out_bff.library(make_node_name):
                            out_bff.emit_var_assignment("Hidden", True)
                            out_bff.emit_var_assignment("Compiler", format_compiler_node_name(toolchain_name))
                            out_bff.emit_var_assignment("CompilerInputPath", compiler_input_path)
                            out_bff.emit_var_assignment("CompilerInputPathRecurse", True)
                            out_bff.emit_var_assignment("CompilerInputPattern", compiler_input_pattern)
                            out_bff.emit_var_assignment("CompilerOutputPath", target_output_dir_path)
                            out_bff.emit_var_assignment("CompilerOptions", " ".join(compiler_options),
                                                        should_split_str=True)
                            out_bff.line_break()
                            out_bff.emit_var_assignment("Librarian", toolchain_def["librarian_path"])
                            out_bff.emit_var_assignment("LibrarianOutput", librarian_output_path)
                            out_bff.emit_var_assignment("LibrarianOptions", " ".join(librarian_options),
                                                        should_split_str=True)

                        # Deploy step does nothing for static libs.
                        deploy_node_name = format_deploy_node_name(target_node_name)
                        with out_bff.alias(deploy_node_name):
                            out_bff.emit_var_assignment("Hidden", True)
                            out_bff.emit_var_assignment("Targets", make_node_name)

                        with out_bff.alias(target_node_name):
                            out_bff.emit_var_assignment("Targets", deploy_node_name)

                    elif target_kind == base.TargetKind.DYNAMIC_LIB:

                        object_list_node_name = format_obj_node_name(target_node_name)
                        with out_bff.object_list(object_list_node_name):
                            out_bff.emit_var_assignment("Hidden", True)
                            out_bff.emit_var_assignment("Compiler", format_compiler_node_name(toolchain_name))
                            out_bff.emit_var_assignment("CompilerInputPath", compiler_input_path)
                            out_bff.emit_var_assignment("CompilerInputPathRecurse", True)
                            out_bff.emit_var_assignment("CompilerInputPattern", compiler_input_pattern)
                            out_bff.emit_var_assignment("CompilerOutputPath", target_output_dir_path)
                            out_bff.emit_var_assignment("CompilerOptions", " ".join(compiler_options),
                                                        should_split_str=True)

                        #
                        linker_output_path = fs.path.join(target_output_dir_path, f"{target_node_name}.dll")

                        libraries = [object_list_node_name]
                        libraries += [format_build_node_name(format_target_node_name(lib, toolchain_name, build_type))
                                      for lib in target_impl["link_libs"]]

                        linker_options = build_linker_options(
                            linker_arg_formatter, target_output_dir_path, target_node_name, target_kind,
                            toolchain_build_type_linker_args,
                            toolchain_build_type_link_libs, toolchain_lib_dirs,
                            target_impl["link_libs_external"], target_impl["link_libs_external_dirs"]
                        )

                        make_node_name = format_build_node_name(target_node_name)
                        with out_bff.dll(make_node_name):
                            # out_bff.emit_var_assignment("Hidden", True)  # DLL does not support .Hidden
                            out_bff.emit_var_assignment("Libraries", libraries)
                            out_bff.emit_var_assignment("Linker", toolchain_def["linker_path"])
                            out_bff.emit_var_assignment("LinkerOutput", linker_output_path)
                            out_bff.emit_var_assignment("LinkerOptions", " ".join(linker_options),
                                                        should_split_str=True)

                        #
                        prebuild_deps = [make_node_name]
                        prebuild_deps += [format_deploy_node_name(format_target_node_name(lib, toolchain_name, build_type))
                                          for lib in target_impl["runtime_libs"]]

                        deploy_node_name = format_deploy_node_name(target_node_name)
                        with out_bff.copy_dir(deploy_node_name):
                            out_bff.emit_var_assignment("Hidden", True)
                            out_bff.emit_var_assignment("PreBuildDependencies", prebuild_deps)
                            out_bff.emit_var_assignment("SourcePaths", target_output_dir_path)
                            out_bff.emit_var_assignment("SourcePathsPattern", ["*.dll", "*.pdb"])
                            out_bff.emit_var_assignment("Dest", deploy_dir_abs_path)

                        with out_bff.alias(target_node_name):
                            out_bff.emit_var_assignment("Targets", deploy_node_name)

                    elif target_kind == base.TargetKind.EXECUTABLE:

                        object_list_node_name = format_obj_node_name(target_node_name)

                        with out_bff.object_list(object_list_node_name):
                            out_bff.emit_var_assignment("Hidden", True)
                            out_bff.emit_var_assignment("Compiler", format_compiler_node_name(toolchain_name))
                            out_bff.emit_var_assignment("CompilerInputPath", compiler_input_path)
                            out_bff.emit_var_assignment("CompilerInputPathRecurse", True)
                            out_bff.emit_var_assignment("CompilerInputPattern", compiler_input_pattern)
                            out_bff.emit_var_assignment("CompilerOutputPath", target_output_dir_path)
                            out_bff.emit_var_assignment("CompilerOptions", " ".join(compiler_options),
                                                        should_split_str=True)

                        #
                        linker_output_path = fs.path.join(target_output_dir_path, f"{target_node_name}.exe")

                        libraries = [object_list_node_name]
                        libraries += [format_build_node_name(format_target_node_name(lib, toolchain_name, build_type))
                                      for lib in target_impl["link_libs"]]

                        linker_options = build_linker_options(
                            linker_arg_formatter, target_output_dir_path, target_node_name, target_kind,
                            toolchain_build_type_linker_args, toolchain_build_type_link_libs, toolchain_lib_dirs,
                            target_impl["link_libs_external"], target_impl["link_libs_external_dirs"]
                        )

                        make_node_name = format_build_node_name(target_node_name)
                        with out_bff.exe(make_node_name):
                            # out_bff.emit_var_assignment("Hidden", True)  # Executable does not support .Hidden
                            out_bff.emit_var_assignment("Libraries", libraries)
                            out_bff.emit_var_assignment("Linker", toolchain_def["linker_path"])
                            out_bff.emit_var_assignment("LinkerOutput", linker_output_path)
                            out_bff.emit_var_assignment("LinkerOptions", " ".join(linker_options),
                                                        should_split_str=True)

                        #
                        prebuild_deps = [make_node_name]
                        prebuild_deps += [format_deploy_node_name(format_target_node_name(lib, toolchain_name, build_type))
                                          for lib in target_impl["runtime_libs"]]

                        deploy_node_name = format_deploy_node_name(target_node_name)
                        with out_bff.copy_dir(deploy_node_name):
                            # CopyDir does not support .Hidden, however it is not listed with -showtargets.
                            # out_bff.emit_var_assignment("Hidden", True)
                            out_bff.emit_var_assignment("PreBuildDependencies", prebuild_deps)
                            out_bff.emit_var_assignment("SourcePaths", target_output_dir_path)
                            out_bff.emit_var_assignment("SourcePathsPattern", ["*.exe", "*.pdb"])
                            out_bff.emit_var_assignment("Dest", deploy_dir_abs_path)

                        with out_bff.alias(target_node_name):
                            out_bff.emit_var_assignment("Targets", deploy_node_name)

                    else:
                        raise RuntimeError("unsupported target kind")

                    all_nodes.append(target_node_name)
                    per_build_type_nodes[build_type].append(target_node_name)
                    per_toolchain_nodes[toolchain_name].append(target_node_name)
                    config_vector_nodes[toolchain_name][build_type].append(target_node_name)

        for build_type, nodes in per_build_type_nodes.items():
            with out_bff.alias(f"{self.ALL_TARGETS_TARGET_NAME}-{build_type}"):
                out_bff.emit_var_assignment("Targets", nodes)

        for toolchain_name, nodes in per_toolchain_nodes.items():
            with out_bff.alias(f"{self.ALL_TARGETS_TARGET_NAME}-{toolchain_name}"):
                out_bff.emit_var_assignment("Targets", nodes)

        for toolchain_name, per_toolchain_per_build_type_visible_nodes in config_vector_nodes.items():
            for build_type, nodes in per_toolchain_per_build_type_visible_nodes.items():
                with out_bff.alias(f"{self.ALL_TARGETS_TARGET_NAME}-{toolchain_name}-{build_type}"):
                    out_bff.emit_var_assignment("Targets", nodes)

        with out_bff.alias(f"{self.ALL_TARGETS_TARGET_NAME}"):
            out_bff.emit_var_assignment("Targets", all_nodes)

        # vc projects and sln
        bff_path = fs.path.join(f"{configure_dir_abs_path}", "fbuild.bff")
        vs_dir_abs_path = fs.path.join(configure_dir_abs_path, "vs")

        project_nodes = []
        for target_name in targets_names:
            target_source_dir_abs_path = fs.path.join(source_dir_abs_path, target_name)
            project_out_abs_path = fs.path.join(vs_dir_abs_path, f"{target_name}.vcxproj")

            project_node_name = f"vcxproj-{target_name}"
            with out_bff.vcxproject(project_node_name):
                out_bff.emit_var_assignment("ProjectOutput", project_out_abs_path)
                out_bff.emit_var_assignment("ProjectInputPaths", target_source_dir_abs_path)
                out_bff.emit_var_assignment("ProjectBasePath", target_source_dir_abs_path)

                if False:
                    project_configs = []
                    for toolchain_name in toolchains_manifest.keys():
                        for build_type in build_types:
                            target_impl = targets_impls[base.build_target_key(target_name, toolchain_name, build_type)]
                            target_node_name = format_target_node_name(target_name, toolchain_name, build_type)

                            cfg = {}

                            cfg["Platform"] = "x64"
                            cfg["PlatformToolset"] = "v142"
                            cfg["Config"] = f"{toolchain_name}-{build_type}"

                            cfg["Target"] = target_node_name
                            cfg["ProjectBuildCommand"] = f"fbuild -ide -config \"{bff_path}\" {target_node_name}"
                            cfg["ProjectRebuildCommand"] = f"fbuild -ide -config \"{bff_path}\" -clean {target_node_name}"
                            # ProjectCleanCommand

                            cfg["LocalDebuggerCommand"] = fs.path.join(build_dir_abs_path, f"{target_node_name}.exe")

                            include_dirs_intellisense = ""
                            for include_dir in target_impl["include_dirs"]:
                                include_dirs_intellisense += f"{include_dir};"

                            cfg["IncludeSearchPath"] = include_dirs_intellisense

                            definitions_intellisense = ""
                            for definition in target_impl["definitions"]:
                                definitions_intellisense += f"{definition};"

                            cfg["PreprocessorDefinitions"] = definitions_intellisense

                            project_configs.append(cfg)

                    out_bff.emit_var_assignment("ProjectConfigs", project_configs)
                else:
                    out_bff._emit_line(".ProjectConfigs = {}")

                    for toolchain_name in toolchains_manifest.keys():
                        for build_type in build_types:
                            target_impl = targets_impls[base.build_target_key(target_name, toolchain_name, build_type)]
                            target_node_name = format_target_node_name(target_name, toolchain_name, build_type)

                            out_bff._emit_line(".cfg = [")
                            out_bff._indent()

                            out_bff.emit_var_assignment("Platform", "x64")
                            out_bff.emit_var_assignment("PlatformToolset", "v142")
                            out_bff.emit_var_assignment("Config", f"{toolchain_name}-{build_type}")
                            #out_bff.emit_var_assignment("Config", "Debug")
                            out_bff.line_break()
                            out_bff.emit_var_assignment("Target", target_node_name)
                            out_bff.emit_var_assignment("ProjectBuildCommand", f"fbuild -ide -config \"{bff_path}\" {target_node_name}")
                            out_bff.emit_var_assignment("ProjectRebuildCommand", f"fbuild -ide -config \"{bff_path}\" -clean {target_node_name}")
                            # ProjectCleanCommand
                            out_bff.emit_var_assignment("LocalDebuggerCommand", fs.path.join(build_dir_abs_path, f"{target_node_name}.exe"))
                            out_bff.line_break()

                            include_dirs_intellisense = ""
                            for include_dir in target_impl["include_dirs"]:
                                include_dirs_intellisense += f"{include_dir};"

                            out_bff.emit_var_assignment("IncludeSearchPath", include_dirs_intellisense)

                            definitions_intellisense = ""
                            for definition in target_impl["definitions"]:
                                definitions_intellisense += f"{definition};"

                            out_bff.emit_var_assignment("PreprocessorDefinitions", definitions_intellisense)

                            out_bff._dedent()
                            out_bff._emit_line("]")

                            out_bff._emit_line(".ProjectConfigs + .cfg")


            project_nodes.append(project_node_name)

        # special 'all' project
        all_targets_project_path = fs.path.join(vs_dir_abs_path, f"{self.ALL_TARGETS_TARGET_NAME}.vcxproj")

        project_node_name = f"vcxproj-{self.ALL_TARGETS_TARGET_NAME}"
        with out_bff.vcxproject(project_node_name):
            out_bff.emit_var_assignment("ProjectOutput", all_targets_project_path)

            if False:
                project_configs = []
                for toolchain_name in toolchains_manifest.keys():
                    for build_type in build_types:
                        target_node_name = format_target_node_name(self.ALL_TARGETS_TARGET_NAME, toolchain_name, build_type)

                        cfg["Platform"] = "x64"
                        cfg["PlatformToolset"] = "v142"
                        cfg["Config"] = f"{toolchain_name}-{build_type}"

                        cfg["Target"] = target_node_name
                        cfg["ProjectBuildCommand"] = f"fbuild -ide -config \"{bff_path}\" {target_node_name}"
                        cfg["ProjectRebuildCommand"] = f"fbuild -ide -config \"{bff_path}\" -clean {target_node_name}"
                        # ProjectCleanCommand

                        cfg["LocalDebuggerCommand"] = ""

                out_bff.emit_var_assignment("ProjectConfigs", project_configs, should_split_str=True)
            else:
                out_bff._emit_line(".ProjectConfigs = {}")

                for toolchain_name in toolchains_manifest.keys():
                    for build_type in build_types:
                        target_node_name = format_target_node_name(self.ALL_TARGETS_TARGET_NAME, toolchain_name, build_type)

                        out_bff._emit_line(".cfg = [")
                        out_bff._indent()

                        out_bff.emit_var_assignment("Platform", "x64")
                        out_bff.emit_var_assignment("PlatformToolset", "v142")
                        out_bff.emit_var_assignment("Config", f"{toolchain_name}-{build_type}")
                        #out_bff.emit_var_assignment("Config", "Debug")
                        out_bff.line_break()
                        out_bff.emit_var_assignment("Target", target_node_name)
                        out_bff.emit_var_assignment("ProjectBuildCommand", f"fbuild -ide -config \"{bff_path}\" {target_node_name}")
                        out_bff.emit_var_assignment("ProjectRebuildCommand", f"fbuild -ide -config \"{bff_path}\" -clean {target_node_name}")
                        # ProjectCleanCommand
                        out_bff.emit_var_assignment("LocalDebuggerCommand", "")

                        out_bff._dedent()
                        out_bff._emit_line("]")
                        out_bff._emit_line(".ProjectConfigs + .cfg")

        project_nodes.append(project_node_name)

        # solution
        sln_path = fs.path.join(vs_dir_abs_path, "generated.sln")

        with out_bff.vssolution("rapid_sln"):
            out_bff.emit_var_assignment("SolutionOutput", sln_path)
            out_bff.emit_var_assignment("SolutionProjects", project_nodes)
            out_bff.line_break()

            if False:
                sln_configs = []

                for toolchain_name in toolchains_manifest.keys():
                    for build_type in build_types:
                        cfg = {
                            "Platform": "x64",
                            "Config": f"{toolchain_name}-{build_type}",
                            "SolutionPlatform": toolchain_name,
                            "SolutionConfig": build_type,
                            "SolutionBuildProject": all_targets_project_path
                        }
                        sln_configs.append(cfg)
                out_bff.emit_var_assignment("SolutionConfigs", sln_configs)
                out_bff.line_break()

                sln_deps = [
                    {
                        "Projects": project_nodes,
                        "Dependencies": [all_targets_project_path]
                    }
                ]

                out_bff.emit_var_assignment("SolutionDependencies", sln_deps, should_split_str=True)

            else:
                out_bff._emit_line(".SolutionConfigs = {}")

                for toolchain_name in toolchains_manifest.keys():
                    for build_type in build_types:

                        out_bff._emit_line(".cfg = [")
                        out_bff._indent()

                        out_bff.emit_var_assignment("Platform", "x64")
                        out_bff.emit_var_assignment("Config", f"{toolchain_name}-{build_type}")
                        out_bff.emit_var_assignment("SolutionPlatform", toolchain_name)
                        out_bff.emit_var_assignment("SolutionConfig", build_type)
                        out_bff.emit_var_assignment("SolutionBuildProject", all_targets_project_path)

                        out_bff._dedent()
                        out_bff._emit_line("]")
                        out_bff._emit_line(".SolutionConfigs + .cfg")
                out_bff.line_break()

                out_bff._emit_line(".SolutionDependencies = {}")

                out_bff._emit_line(".dep = [")
                out_bff._indent()

                out_bff.emit_var_assignment("Projects", project_nodes)
                out_bff.emit_var_assignment("Dependencies", [all_targets_project_path])

                out_bff._dedent()
                out_bff._emit_line("]")
                out_bff._emit_line(".SolutionDependencies + .dep")
            out_bff.line_break()

            out_bff.emit_var_assignment("SolutionVisualStudioVersion", "15.0")
            out_bff.emit_var_assignment("SolutionMinimumVisualStudioVersion", "15.0")

        return out_bff.build()
