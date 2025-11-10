from setuptools import setup, find_packages

setup(
    name="axiom",
    version="2.0.0",
    description="Axiom — Infrastructure Intelligence CLI Tool",
    author="gh0st359",
    author_email="",
    url="https://github.com/gh0st359/axiom",
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        "requests>=2.31.0",
        "dnspython>=2.4.2",
        "python-whois>=0.8.0",
        "colorama>=0.4.6",
        "rich>=13.0.0",
        "tqdm>=4.66.1"
    ],
    python_requires=">=3.8",
    entry_points={
        "console_scripts": [
            "axiom=axiom.cli:main",
        ],
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
        "Topic :: Security",
        "Topic :: Software Development :: Build Tools",
    ],
)
