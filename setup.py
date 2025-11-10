from setuptools import setup, find_packages

setup(
    name='axiom',
    version='2.0.0',
    description='Axiom — Infrastructure Intelligence CLI Tool',
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        'requests>=2.31.0',
        'dnspython>=2.4.2',
        'python-whois>=0.8.0',
    ],
    entry_points={
        'console_scripts': ['axiom=axiom.cli:main'],
    },
)
