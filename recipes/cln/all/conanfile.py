import glob
import os

from conans import ConanFile, AutoToolsBuildEnvironment, VisualStudioBuildEnvironment, tools
from conans.errors import ConanInvalidConfiguration

class ClnConan(ConanFile):
    name = "cln"
    description = ""
    license = "MIT"
    topics = "cln", "cln"
    homepage = "https://github.com/OSGeo/gdal"
    url = "https://github.com/conan-io/conan-center-index"
    generators = "pkg_config"
    requires = "gmp/6.2.0"
    settings = "os", "arch", "compiler", "build_type"
    options = {
        "shared": [True, False],
        "fPIC": [True, False],
    }
    default_options = {
        "shared": False,
        "fPIC": True,
    }

    _autotools= None

    @property
    def _source_subfolder(self):
        return "source_subfolder"

    @property
    def _build_subfolder(self):
        return "build_subfolder"

    def _configure_autotools(self):
        if self._autotools:
            return self._autotools

        self._autotools = AutoToolsBuildEnvironment(self, win_bash=tools.os_info.is_windows)

        return self._autotools

    def config_options(self):
        if self.settings.os == "Windows":
            del self.options.fPIC

    def configure(self):
        pass

    def build_requirements(self):
        self.build_requires("autoconf/2.69")
        self.build_requires("libtool/2.4.6")

    def source(self):
        tools.get(**self.conan_data["sources"][self.version])
        os.rename(self.name + "-" + self.version, self._source_subfolder)

    def build(self):
        autotools = self._configure_autotools()
        with tools.chdir(self._source_subfolder):
            autotools.configure()
            autotools.make(args=["-j3"])
            # autotools.make(args=["-j%s" % str(tools.cpu_count())])

    def package(self):
        autotools = self._configure_autotools()
        with tools.chdir(self._source_subfolder):
            autotools.install()

    def package_info(self):
        self.cpp_info.libs = tools.collect_libs(self)
