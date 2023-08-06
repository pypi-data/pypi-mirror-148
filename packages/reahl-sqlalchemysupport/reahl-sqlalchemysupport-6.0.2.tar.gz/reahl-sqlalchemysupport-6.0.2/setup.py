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
    name='reahl-sqlalchemysupport',
    version='6.0.2',
    description='Support for using SqlAlchemy with Reahl.',
    long_description='Reahl is a web application framework that allows a Python programmer to work in terms of useful abstractions - using a single programming language.\n\nThis package contains infrastructure necessary to use Reahl with SqlAlchemy or Elixir. ',
    url='http://www.reahl.org',
    maintainer='Iwan Vosloo',
    maintainer_email='iwan@reahl.org',
    packages=['reahl', 'reahl.sqlalchemysupport', 'reahl.sqlalchemysupport_dev'],
    py_modules=[],
    include_package_data=False,
    namespace_packages=['reahl'],
    install_requires=['reahl-component>=6.0,<6.1', 'reahl-commands>=6.0,<6.1', 'SQLAlchemy>=1.2.0,<1.4.999', 'alembic>=0.9.6,<1.7.999'],
    setup_requires=['pytest-runner', 'reahl-component-metadata', 'setuptools >= 51.0.0', 'setuptools-git >= 1.1', 'toml', 'wheel'],
    tests_require=['pytest>=3.0', 'reahl-tofu>=6.0,<6.1', 'reahl-sqlitesupport>=6.0,<6.1', 'reahl-domain>=6.0,<6.1', 'reahl-dev>=6.0,<6.1', 'reahl-stubble>=6.0,<6.1'],
    extras_require={},
    cmdclass={'install_test_dependencies': InstallTestDependencies}
)
