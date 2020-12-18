import os

from conans import ConanFile, CMake, tools


class CapstoneConan(ConanFile):
    name = "capstone"
    description = "Capstone disassembly/disassembler framework"
    version = "4.0.2"
    license = "BSD-3-Clause"
    url = "https://github.com/Torsm/conan-capstone"
    homepage = "https://github.com/aquynh/capstone"
    settings = "os", "compiler", "build_type", "arch"
    exports_sources = ["CMakeLists.txt"]
    generators = "cmake"
    options = {"shared": [True, False], "fPIC": [True, False]}
    default_options = {"shared": False, "fPIC": True}

    _cmake = None

    @property
    def _source_subfolder(self):
        return "source_subfolder"

    @property
    def _build_subfolder(self):
        return "build_subfolder"

    def config_options(self):
        if self.settings.os == "Windows":
            del self.options.fPIC

    def source(self):
        tools.get(**self.conan_data["sources"][self.version])
        folder_name = "capstone-{}".format(self.version)
        os.rename(folder_name, self._source_subfolder)

    def _configure_cmake(self):
        if self._cmake:
            return self._cmake
        self._cmake = CMake(self)
        self._cmake.definitions["CAPSTONE_BUILD_STATIC"] = not self.options.shared
        self._cmake.definitions["CAPSTONE_BUILD_SHARED"] = self.options.shared
        self._cmake.configure(build_folder=self._build_subfolder)
        return self._cmake

    def build(self):
        cmake = self._configure_cmake()
        cmake.build()

    def package(self):
        self.copy("LICENSE*.txt", src=self._source_subfolder, dst="licenses")
        cmake = self._configure_cmake()
        cmake.install()

    def package_info(self):
        self.cpp_info.libs = ["capstone"]
