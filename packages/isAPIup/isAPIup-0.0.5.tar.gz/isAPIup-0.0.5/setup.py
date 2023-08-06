from setuptools import setup
import pathlib

# The directory containing this file
HERE = '/isAPIup/isAPIup.py'

# The text of the README file
README = open("README.md").read()

# This call to setup() does all the work
setup(
    name="isAPIup",
    version="0.0.5",
    description="isAPIup is a Length based API testing and monitoring library",
    long_description=README,
    long_description_content_type="text/markdown",
    url="https://github.com/Sandeeppushp/isAPIup",
    author="Sandeep Pushp",
    author_email="sandeepkumarpushp@gmail.com",
    license="MIT",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
    ],
    packages=["isAPIup"],
    python_requires='>=3.2',
    include_package_data=True,
    install_requires=["requests"],
)
