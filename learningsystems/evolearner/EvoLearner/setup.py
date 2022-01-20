from setuptools import setup, find_packages

with open('README.md', 'r') as fh:
    long_description = fh.read()

setup(
    name='evolearner',
    description='Learning Description Logics with Evolutionary Algorithms',
    version='0.0.2',
    packages=find_packages(exclude=('tests', 'test.*', 'examples.*')),
    install_requires=['scikit-learn==0.24.2',
                      'owlready2==0.35',
                      'deap==1.3.1',
                      'rdflib==5.0.0',
                      'matplotlib==3.3.4',
                      'tabulate==0.8.9',
                      'pandas==1.1.5'],
    author='No Author',
    author_email='No email',
    classifiers=[
        "Programming Language :: Python :: 3.6",
        ],
    python_requires='==3.6.9',
    long_description=long_description,
    long_description_content_type="text/markdown",
)
