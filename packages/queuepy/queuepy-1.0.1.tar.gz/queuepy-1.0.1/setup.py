import pathlib
from setuptools import setup

# The directory containing this file
HERE = pathlib.Path(__file__).parent

# The text of the README file
README = (HERE / "README.md").read_text()

# This call to setup() does all the work
setup(
    name="queuepy",
    version="1.0.1",
    description="Simple module to create queues",
    long_description=README,
    long_description_content_type="text/markdown",
    url="https://github.com/synnkfps/PyQueue",
    author="SynnK",
    author_email="",
    license="MIT",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3.10",
    ],
    packages=["queuepy"],
    include_package_data=True,
)
