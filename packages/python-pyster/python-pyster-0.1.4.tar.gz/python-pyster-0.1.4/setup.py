from setuptools import setup
setup(
    name = 'python-pyster',
    version = '0.1.4',
    license = 'MIT',
    description = 'Python unit testing made easy with pyster!',
    author = 'Wrench56',
    author_email = 'dmarkreg@gmail.com',
    url = 'https://github.com/Wrench56/pyster',
    install_requires = ['rich'],
    scripts = [
        'pysterminal.py',
        '__init__.py',
        'endreport.py',
        'options.py',
        'pyster.py',
        'errors/test_failure.py',
        'errors/non_overridable_error.py'
        ],
    long_description = 'Please find more information on my Github page!',
    entry_points={
         "console_scripts": [
            "pysterminal=pyster.pysterminal:main"
        ]
    },
    packages=['errors']
)