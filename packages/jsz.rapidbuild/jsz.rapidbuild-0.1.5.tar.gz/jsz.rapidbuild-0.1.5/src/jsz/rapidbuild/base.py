from abc import ABC, abstractmethod
import sys
import subprocess
import os.path
from enum import Enum, auto


def sanitize_path(path):
    return os.path.normpath(path)


def sanitize_paths(paths):
    ret = []
    for p in paths:
        p = sanitize_path(p)
        if len(p) != 0:
            ret.append(p)
    return ret


def build_target_key(target_name: str, toolchain_name: str, build_type: str):
    return "{}_{}_{}".format(target_name, toolchain_name, build_type)


class TargetKind(Enum):
    STATIC_LIB = auto()
    DYNAMIC_LIB = auto()
    EXECUTABLE = auto()

    @staticmethod
    def from_string(s: str):
        return {
            "rapid_static_lib": TargetKind.STATIC_LIB,
            "rapid_dynamic_lib": TargetKind.DYNAMIC_LIB,
            "rapid_exe": TargetKind.EXECUTABLE,
        }[s]

    def to_string(self):
        return {
            TargetKind.STATIC_LIB: "rapid_static_lib",
            TargetKind.DYNAMIC_LIB: "rapid_dynamic_lib",
            TargetKind.EXECUTABLE: "rapid_exe",
        }[self]


BUILD_TYPE_DEBUG = "debug"
BUILD_TYPE_RELEASE = "release"

TOOLCHAIN_MSVC16 = "msvc16"
TOOLCHAIN_LLVM13 = "llvm13"


class Logger(ABC):
    @abstractmethod
    def log_info(self, *args):
        pass

    @abstractmethod
    def log_error(self, *args):
        pass


class LoggerDefault(Logger):
    def log_info(self, *args):
        print(*args, file=sys.stdout)

    def log_error(self, *args):
        print(*args, file=sys.stderr)


class ProcessRunner(ABC):
    @abstractmethod
    def run(self, args, *, env, check):
        pass


class ProcessRunnerDefault(ProcessRunner):
    def run(self, args, *, env, check):
        subprocess.run(args, env=env, check=check)


class SystemConfigManifestProvider(ABC):
    @abstractmethod
    def run(self, working_dir_abs_path):
        pass

    @abstractmethod
    def get_toolchains_manifest(self):
        pass

    @abstractmethod
    def get_third_party_manifest(self):
        pass


class ToolchainSettingsProvider(ABC):
    @abstractmethod
    def get_toolchain_settings(self):
        pass


class BuildScriptEmitter(ABC):
    @abstractmethod
    def filename(self):
        pass

    @abstractmethod
    def contents(self, build_dir_abs_path, toolchains_manifest, toolchains_settings, build_types, targets_names,
                 targets_impls) -> str:
        pass
