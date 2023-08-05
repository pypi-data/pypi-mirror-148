from __future__ import annotations

from conans import ConanFile, tools
from conans.model import Generator
from conans.errors import ConanInvalidConfiguration
import traceback
import jsz.rapidbuild.conan

required_conan_version = ">=1.43"


# noinspection PyBroadException
class RapidGenerator(Generator):
    # noinspection PyPropertyDefinition
    @property
    def filename(self):
        pass

    @property
    def content(self):
        try:
            self.conanfile.output.info("Rapid: Running...")

            rapid_os = jsz.rapidbuild.conan.to_rapid_os(self.conanfile.settings.os)
            if rapid_os is None:
                raise ConanInvalidConfiguration(f"Rapid: unsupported OS '{self.conanfile.settings.os}'.")

            rapid_toolchain = jsz.rapidbuild.conan.to_rapid_toolchain(self.conanfile.settings.compiler,
                                                                 self.conanfile.settings.compiler.version)
            if rapid_toolchain is None:
                raise ConanInvalidConfiguration(f"Rapid: unsupported compiler '{self.conanfile.settings.compiler}',"
                                                f" version '{self.conanfile.settings.compiler.version}'.")

            vc_vars = tools.vcvars_dict(self.conanfile)
            deps_cpp_info = self.conanfile.deps_cpp_info

            return {
                jsz.rapidbuild.conan.get_third_party_manifest_filename():
                    jsz.rapidbuild.conan.generate_third_party_manifest_from_conan_deps_info(deps_cpp_info),
                jsz.rapidbuild.conan.get_toolchain_manifest_filename():
                    jsz.rapidbuild.conan.generate_toolchain_manifest_from_conan_vc_vars(rapid_toolchain, vc_vars)
            }

        except Exception:
            traceback.print_exc()


class RapidGeneratorPackage(ConanFile):
    name = "rapidbuild"
    version = "0.1"
    license = "MIT"
