from setuptools import setup, find_packages


setup(
    name='cucu',
    version='0.0.0',
    license='',
    author="Rodney Gomes",
    author_email='rodneygomes@gmail.com',
    packages=find_packages('src'),
    package_dir={'': 'src'},
    url='https://github.com/rlgomes/cucu',
    keywords='e2e gherkin framework',
    install_requires=[ ],
)
