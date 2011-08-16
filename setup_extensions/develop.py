import setuptools, sys, glob
from setuptools.command.develop import develop as _develop
from distutils.errors import DistutilsArgError

class develop(_develop):

    user_options =  [
        ('ignore-developer-dependencies', None, "Try not to use this! Ignores developer dependencies, such as coverage etc"),
    ] + _develop.user_options

    boolean_options = [
        'ignore-developer-dependencies',
    ] + _develop.boolean_options

    def initialize_options(self):
        _develop.initialize_options(self)
        self.ignore_developer_dependencies = False
        self.no_compile = None  # make DISTUTILS_DEBUG work right!

    def finalize_options(self):
        _develop.finalize_options(self)

    def run(self):
        if not self.ignore_developer_dependencies:
            self.distribution.install_requires.append(self.distribution.extras_require.get('develop', []))

        return _develop.run(self)
