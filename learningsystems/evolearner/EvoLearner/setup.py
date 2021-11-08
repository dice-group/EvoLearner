from setuptools import setup, find_packages

with open('README.md', 'r') as fh:
    long_description = fh.read()

setup(
    name='evolearner',
    description='Learning Description Logics with Evolutionary Algorithms',
    version='0.0.2',
    packages=find_packages(exclude=('tests', 'test.*', 'examples.*')),
    install_requires=['scikit-learn>=0.22.1',
                      'owlready2>=0.23',
                      'deap',
                      'rdflib',
                      'matplotlib',
                      'tabulate',
                      'gdown',
                      'pandas'],
    author='No Author',
    author_email='No email',
    classifiers=[
        "Programming Language :: Python :: 3.6",
        ],
    python_requires='>=3.6',
    long_description=long_description,
    long_description_content_type="text/markdown",
)
