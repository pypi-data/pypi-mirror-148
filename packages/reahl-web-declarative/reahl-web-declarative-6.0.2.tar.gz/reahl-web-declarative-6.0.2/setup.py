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
    name='reahl-web-declarative',
    version='6.0.2',
    description='An implementation of Reahl persisted classes using SqlAlchemy.',
    long_description='Reahl is a web application framework that allows a Python programmer to work in terms of useful abstractions - using a single programming language.\n\nSome core elements of Reahl can be implemented for use with different persistence technologies. This is such an implementation based on SqlAlchemy. ',
    url='http://www.reahl.org',
    maintainer='Iwan Vosloo',
    maintainer_email='iwan@reahl.org',
    packages=['reahl', 'reahl.webdeclarative', 'reahl.webdeclarative_dev'],
    py_modules=[],
    include_package_data=True,
    namespace_packages=['reahl'],
    install_requires=['reahl-sqlalchemysupport>=6.0,<6.1', 'reahl-web>=6.0,<6.1', 'reahl-component>=6.0,<6.1'],
    setup_requires=['pytest-runner', 'reahl-component-metadata', 'setuptools >= 51.0.0', 'setuptools-git >= 1.1', 'toml', 'wheel'],
    tests_require=['WebOb>=1.8,<1.8.999', 'pytest>=3.0', 'reahl-tofu>=6.0,<6.1', 'reahl-stubble>=6.0,<6.1', 'reahl-dev>=6.0,<6.1', 'reahl-webdev>=6.0,<6.1', 'reahl-browsertools>=6.0,<6.1', 'reahl-domain>=6.0,<6.1', 'reahl-postgresqlsupport>=6.0,<6.1'],
    extras_require={},
    cmdclass={'install_test_dependencies': InstallTestDependencies}
)
