from . import base


class ToolchainSettingsProviderDefault(base.ToolchainSettingsProvider):
    @staticmethod
    def _get_toolchain_settings_msvc():
        return {
            "compiler_args": {
                "all": [
                    # warning level 4, as errors, all
                    '/W4', '/WX', '/Wall',
                    # Info: the compiler performed inlining on the given function, although it was not marked
                    # for inlining.
                    '/wd4711',
                    # do not report warnings from third parties
                    '/experimental:external', '/external:anglebrackets', '/external:W0',
                    # specifies that are sources are C + +
                    '/TP',
                    # set standard
                    '/std:c++17', '/permissive-',
                    # enable string pooling
                    '/GF',
                    # disable RTTI
                    '/GR-',
                    # s: Enables standard C++ stack unwinding.catches only standard C++ exceptions when you
                    #    use catch(...) syntax.
                    # c: Compiler assumes that functions declared as extern "C" never throw a C + + exception.
                    '/EHsc',
                    # no acquire / release semantics for volatile vars
                    '/volatile:iso',
                    # require to always define the class before declaring a pointer-to-member
                    '/vmb',
                    # disable M$ C extensions
                    # '/Za ' # not recommended for C + + code
                ],
                base.BUILD_TYPE_DEBUG: [
                    '/MDd',
                    # disable optimization
                    '/Od',
                    # debug format: PDB
                    '/Zi',
                    # faster PDB generation
                    '/Zf',
                    # floats according to standard
                    '/fp:strict',
                    # enable buffer security checks
                    '/GS',
                    '/sdl',
                    # enable control flow guards
                    '/guard:cf',
                    # enable EH continuation metadata(must be also present in linker args)
                    '/guard:ehcont',
                    # enable all runtime checks.RTCc rejects conformant code, so it is not supported by
                    # the C++ Standard Library
                    '/RTCsu'
                ],
                base.BUILD_TYPE_RELEASE: [
                    '/MD '
                    # enable optimization
                    '/O2 '
                    # fast floats
                    '/fp:fast '
                    # disable buffer security checks
                    '/GS- '
                    # + '/sdl- ' // it overrides / GS -
                    # disable control flow guards
                    '/guard:cf- '
                    # disable EH continuation metadata
                    '/guard:ehcont- '
                ],
            },
            "definitions": {
                "all": {
                    "_MT": None,
                    "_DLL": None,
                },
                base.BUILD_TYPE_DEBUG: {
                    "_DEBUG": None,
                },
                base.BUILD_TYPE_RELEASE: {
                },
            },
            "linker_args": {
                "all": [
                    "/WX",
                    "/IGNORE:4099",
                    "/machine:x64"
                ],
                base.BUILD_TYPE_DEBUG: [
                    "/DEBUG",
                    "/GUARD:CF"
                ],
                base.BUILD_TYPE_RELEASE: [
                    "/GUARD:CF"
                ],
            },
            "link_libs": {
                "all": [
                    'kernel32.lib',
                    'user32.lib',
                    'gdi32.lib',
                    'shell32.lib',
                    'winspool.lib',
                    'ole32.lib',
                    'oleaut32.lib',
                    'uuid.lib',
                    'comdlg32.lib',
                    'advapi32.lib',
                ],
                base.BUILD_TYPE_DEBUG: [
                    'ucrtd.lib',
                    'vcruntimed.lib',
                    'msvcrtd.lib',
                    'msvcprtd.lib',
                ],
                base.BUILD_TYPE_RELEASE: [
                    'ucrt.lib',
                    'vcruntime.lib',
                    'msvcrt.lib',
                    'msvcprt.lib',
                ],
            },
        }

    @staticmethod
    def _get_toolchain_settings_llvm():
        return {
            "compiler_args": {
                "all": [
                    # warnings
                    '-Wall', '-Wextra', '-pedantic', '-pedantic-errors', '-Werror',
                    # set standard
                    '-std=c++17',
                    # disable RTTI
                    '-fno-rtti',
                    # disable exceptions
                    '-fno-exceptions',
                    # use a best-case representation method for member pointers
                    '-fcomplete-member-pointers',
                ],
                base.BUILD_TYPE_DEBUG: [
                    '-O0',
                    '-g',
                ],
                base.BUILD_TYPE_RELEASE: [
                    '-O3',
                    '-ffast-math',
                ],
            },
            "definitions": {
                "all": {
                    "_MT": None,
                    "_DLL": None,
                },
                base.BUILD_TYPE_DEBUG: {
                    "_DEBUG": None,
                },
                base.BUILD_TYPE_RELEASE: {
                },
            },
            "linker_args": {
                "all": [
                    "/WX",
                    "/machine:x64"
                ],
                base.BUILD_TYPE_DEBUG: [
                    "/DEBUG",
                    "/GUARD:CF"
                ],
                base.BUILD_TYPE_RELEASE: [
                    "/GUARD:CF"
                ],
            },
            "link_libs": {
                "all": [
                    'kernel32.lib',
                    'user32.lib',
                    'gdi32.lib',
                    'shell32.lib',
                    'winspool.lib',
                    'ole32.lib',
                    'oleaut32.lib',
                    'uuid.lib',
                    'comdlg32.lib',
                    'advapi32.lib',
                ],
                base.BUILD_TYPE_DEBUG: [
                    'ucrtd.lib',
                    'vcruntimed.lib',
                    'msvcrtd.lib',
                    'msvcprtd.lib',
                ],
                base.BUILD_TYPE_RELEASE: [
                    'ucrt.lib',
                    'vcruntime.lib',
                    'msvcrt.lib',
                    'msvcprt.lib',
                ],
            },
        }

    def get_toolchain_settings(self):
        return {
            base.TOOLCHAIN_MSVC16: self._get_toolchain_settings_msvc(),
            base.TOOLCHAIN_LLVM13: self._get_toolchain_settings_llvm(),
        }
