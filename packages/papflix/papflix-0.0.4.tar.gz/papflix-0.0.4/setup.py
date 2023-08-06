from setuptools import setup, find_packages


import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()
setup(
    name="papflix",
    version="0.0.4",
    author="kpaparid",
    author_email="kpaparid@gmail.com",
    description="A small example package",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/pypa/sampleproject",
    project_urls={
        "Bug Tracker": "https://github.com/pypa/sampleproject/issues",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    package_dir={"": "src"},
    packages=setuptools.find_packages(where="src"),
    include_package_data=True,
    
    install_requires=['pyjarowinkler==1.8','PySide2==5.15.2.1','python_Levenshtein==0.12.2','requests==2.27.1','setuptools==58.1.0','tmdbv3api==1.7.6'],
    python_requires=">=3.6",

)