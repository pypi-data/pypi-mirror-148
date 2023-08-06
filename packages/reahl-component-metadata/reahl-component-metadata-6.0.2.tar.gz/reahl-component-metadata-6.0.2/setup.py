from setuptools import setup, Command
class InstallTestDependencies(Command):
    user_options = []
    def run(self):
        import sys
        import subprocess
        if self.distribution.tests_require: subprocess.check_call([sys.executable, "-m", "pip", "install", "-q"]+self.distribution.tests_require)

    def initialize_options(self):
        pass

    def finalize_options(self):
        pass

setup(
    name='reahl-component-metadata',
    version='6.0.2',
    description='Plugin fro build tools to be able to write reahl-component metadata.',
    long_description='Reahl is a web application framework that allows a Python programmer to work in terms of useful abstractions - using a single programming language.\n\nThe reahl-component-metadata package extends setuptools\'s setup() call to take an extra "component" keyword argument for packaging the extra metadata reahl-component requires.\n\nThis package is very small and meant to be a build dependency of packages that are Reahl components. ',
    url='http://www.reahl.org',
    maintainer='Iwan Vosloo',
    maintainer_email='iwan@reahl.org',
    packages=['reahl', 'reahl.componentmetadata'],
    py_modules=[],
    include_package_data=False,
    namespace_packages=['reahl'],
    install_requires=['toml'],
    setup_requires=['pytest-runner', 'setuptools >= 51.0.0', 'setuptools-git >= 1.1', 'wheel'],
    tests_require=[],
    extras_require={},
    cmdclass={'install_test_dependencies': InstallTestDependencies}
)
