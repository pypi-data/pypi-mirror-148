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
    name='reahl-component',
    version='6.0.2',
    description='The component framework of Reahl.',
    long_description='Reahl is a web application framework that allows a Python programmer to work in terms of useful abstractions - using a single programming language.\n\nThe reahl-component framework extends setuptools distribution packages to package and distribute more than just code. ',
    url='http://www.reahl.org',
    maintainer='Iwan Vosloo',
    maintainer_email='iwan@reahl.org',
    packages=['reahl', 'reahl.component', 'reahl.component_dev', 'reahl.messages'],
    py_modules=[],
    include_package_data=False,
    namespace_packages=['reahl', 'reahl.messages'],
    install_requires=['Babel>=2.1,<2.9.999', 'python-dateutil>=2.8,<2.8.999', 'wrapt>=1.11.0,<1.13.999', 'setuptools>=51.0.0', 'pip>=10.0.0', 'toml'],
    setup_requires=['pytest-runner', 'reahl-component-metadata', 'setuptools >= 51.0.0', 'setuptools-git >= 1.1', 'toml', 'wheel'],
    tests_require=['pytest>=3.0', 'graphviz', 'reahl-tofu>=6.0,<6.1', 'reahl-stubble>=6.0,<6.1', 'reahl-dev>=6.0,<6.1', 'reahl-sqlalchemysupport>=6.0,<6.1', 'reahl-sqlitesupport>=6.0,<6.1', 'reahl-mysqlsupport>=6.0,<6.1'],
    extras_require={},
    cmdclass={'install_test_dependencies': InstallTestDependencies}
)
