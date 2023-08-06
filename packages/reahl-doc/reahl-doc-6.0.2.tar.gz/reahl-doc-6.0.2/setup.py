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
    name='reahl-doc',
    version='6.0.2',
    description='Documentation and examples for Reahl.',
    long_description='Reahl is a web application framework that allows a Python programmer to work in terms of useful abstractions - using a single programming language.\n\nReahl-doc contains documentation and examples of Reahl.\n\nSee http://www.reahl.org/docs/5.2/tutorial/gettingstarted-install.d.html for installation instructions. ',
    url='http://www.reahl.org',
    maintainer='Iwan Vosloo',
    maintainer_email='iwan@reahl.org',
    packages=['reahl', 'reahl.doc', 'reahl.doc.examples', 'reahl.doc.examples.features', 'reahl.doc.examples.features.access', 'reahl.doc.examples.features.carousel', 'reahl.doc.examples.features.dynamiccontent', 'reahl.doc.examples.features.i18nexample', 'reahl.doc.examples.features.i18nexample.i18nexamplemessages', 'reahl.doc.examples.features.layout', 'reahl.doc.examples.features.pageflow', 'reahl.doc.examples.features.persistence', 'reahl.doc.examples.features.tabbedpanel', 'reahl.doc.examples.features.validation', 'reahl.doc.examples.howtos', 'reahl.doc.examples.howtos.ajaxbootstrap', 'reahl.doc.examples.howtos.ajaxbootstrap.ajaxbootstrap_dev', 'reahl.doc.examples.howtos.bootstrapsass', 'reahl.doc.examples.howtos.bootstrapsassmultihomed', 'reahl.doc.examples.howtos.chartplotly', 'reahl.doc.examples.howtos.chartplotly2', 'reahl.doc.examples.howtos.customisingerrorpages', 'reahl.doc.examples.howtos.customisingerrorpages.customisingerrorpages_dev', 'reahl.doc.examples.howtos.dynamiccontenterrors', 'reahl.doc.examples.howtos.hellodockernginx', 'reahl.doc.examples.howtos.hellonginx', 'reahl.doc.examples.howtos.optimisticconcurrency', 'reahl.doc.examples.howtos.optimisticconcurrency.optimisticconcurrency_dev', 'reahl.doc.examples.howtos.pagerbootstrap', 'reahl.doc.examples.howtos.pagerbootstrap.pagerbootstrap_dev', 'reahl.doc.examples.howtos.paymentpaypal', 'reahl.doc.examples.howtos.responsivedisclosure', 'reahl.doc.examples.howtos.responsivedisclosure.responsivedisclosure_dev', 'reahl.doc.examples.tutorial', 'reahl.doc.examples.tutorial.accessbootstrap', 'reahl.doc.examples.tutorial.accessbootstrap.accessbootstrap_dev', 'reahl.doc.examples.tutorial.addressbook1', 'reahl.doc.examples.tutorial.addressbook1.addressbook1_dev', 'reahl.doc.examples.tutorial.addressbook2', 'reahl.doc.examples.tutorial.addressbook2.addressbook2_dev', 'reahl.doc.examples.tutorial.addressbook2bootstrap', 'reahl.doc.examples.tutorial.addressbook2bootstrap.addressbook2bootstrap_dev', 'reahl.doc.examples.tutorial.addresslist', 'reahl.doc.examples.tutorial.bootstrapgrids', 'reahl.doc.examples.tutorial.componentconfigbootstrap', 'reahl.doc.examples.tutorial.componentconfigbootstrap.componentconfigbootstrap_dev', 'reahl.doc.examples.tutorial.datatablebootstrap', 'reahl.doc.examples.tutorial.datatablebootstrap.datatablebootstrap_dev', 'reahl.doc.examples.tutorial.dynamiccontent', 'reahl.doc.examples.tutorial.dynamiccontent.dynamiccontent_dev', 'reahl.doc.examples.tutorial.hello', 'reahl.doc.examples.tutorial.helloanywhere', 'reahl.doc.examples.tutorial.i18nexamplebootstrap', 'reahl.doc.examples.tutorial.i18nexamplebootstrap.i18nexamplebootstrap_dev', 'reahl.doc.examples.tutorial.i18nexamplebootstrap.i18nexamplebootstrapmessages', 'reahl.doc.examples.tutorial.jobsbootstrap', 'reahl.doc.examples.tutorial.jobsbootstrap.jobsbootstrap_dev', 'reahl.doc.examples.tutorial.login1bootstrap', 'reahl.doc.examples.tutorial.login1bootstrap.login1bootstrap_dev', 'reahl.doc.examples.tutorial.login2bootstrap', 'reahl.doc.examples.tutorial.login2bootstrap.login2bootstrap_dev', 'reahl.doc.examples.tutorial.migrationexamplebootstrap', 'reahl.doc.examples.tutorial.migrationexamplebootstrap.migrationexamplebootstrap_dev', 'reahl.doc.examples.tutorial.pageflow1', 'reahl.doc.examples.tutorial.pageflow1.pageflow1_dev', 'reahl.doc.examples.tutorial.pagelayout', 'reahl.doc.examples.tutorial.parameterised1', 'reahl.doc.examples.tutorial.parameterised2', 'reahl.doc.examples.tutorial.parameterised2.parameterised2_dev', 'reahl.doc.examples.tutorial.sessionscopebootstrap', 'reahl.doc.examples.tutorial.sessionscopebootstrap.sessionscopebootstrap_dev', 'reahl.doc.examples.tutorial.slots', 'reahl.doc.examples.tutorial.tablebootstrap', 'reahl.doc.examples.tutorial.tablebootstrap.etc', 'reahl.doc.examples.tutorial.tablebootstrap.tablebootstrap_dev', 'reahl.doc.examples.web', 'reahl.doc.examples.web.basichtmlinputs', 'reahl.doc.examples.web.basichtmlinputs.basichtmlinputs_dev', 'reahl.doc.examples.web.basichtmlwidgets', 'reahl.doc.examples.web.fileupload', 'reahl.doc_dev', 'reahl.messages'],
    py_modules=[],
    include_package_data=True,
    namespace_packages=['reahl', 'reahl.messages'],
    install_requires=['reahl-web>=6.0,<6.1', 'reahl-component>=6.0,<6.1', 'reahl-sqlalchemysupport>=6.0,<6.1', 'reahl-web-declarative>=6.0,<6.1', 'reahl-domain>=6.0,<6.1', 'reahl-domainui>=6.0,<6.1', 'reahl-commands>=6.0,<6.1', 'reahl-dev>=6.0,<6.1', 'reahl-paypalsupport>=6.0,<6.1', 'pytest>=3.0', 'setuptools>=51.0.0', 'plotly>=5.1.0,<5.6.99999'],
    setup_requires=['pytest-runner', 'reahl-component-metadata', 'setuptools >= 51.0.0', 'setuptools-git >= 1.1', 'toml', 'wheel'],
    tests_require=['pytest>=3.0', 'Sphinx', 'sphinxcontrib-plantuml', 'flaky>=3.7.0', 'reahl-tofu>=6.0,<6.1', 'reahl-stubble>=6.0,<6.1', 'reahl-dev>=6.0,<6.1', 'reahl-webdev>=6.0,<6.1', 'reahl-browsertools>=6.0,<6.1', 'reahl-postgresqlsupport>=6.0,<6.1', 'reahl-sqlitesupport>=6.0,<6.1', 'reahl-mysqlsupport>=6.0,<6.1'],
    extras_require={'pillow': ['Pillow>=2.5,<7.1.999']},
    cmdclass={'install_test_dependencies': InstallTestDependencies}
)
