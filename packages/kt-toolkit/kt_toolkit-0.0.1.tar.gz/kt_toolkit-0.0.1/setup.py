#!/usr/bin/env python
# coding=utf-8

import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="kt_toolkit",
    version="0.0.1",
    author="LiuQQ",
    author_email="voidmain@126.com",
    description="kt_toolkit",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Liu-lqq/kt_toolkit",
    project_urls={
        "Bug Tracker": "https://github.com/Liu-lqq/kt_toolkit/issues",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    package_dir={"": "src"},
    packages=setuptools.find_packages(where="src"),
    python_requires=">=3.5",
    include_package_data=True,
    install_requires=['requests','pandas','tqdm','beautifulsoup4'],
)

