from setuptools import setup, find_packages
setup(
    name = 'python-pyster',
    version = '0.1.17',
    license = 'MIT',
    description = 'Python unit testing made easy with pyster!',
    author = 'Wrench56',
    author_email = 'dmarkreg@gmail.com',
    url = 'https://github.com/Wrench56/pyster',
    install_requires = ['rich'],
    long_description = 'Please find more information on my Github page!',
    entry_points={
         "console_scripts": [
            "pysterminal=pyster.pysterminal:main"
        ]
    },
    packages=find_packages()
)