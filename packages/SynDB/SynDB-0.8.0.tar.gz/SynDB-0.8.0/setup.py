from setuptools import setup

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(name="SynDB",
    version="0.8.0",
    description="simple database using json.",
    long_description_content_type="text/markdown",
    long_description=long_description,
    author="Josh Wells",
    author_email="bam0909@outlook.com",
    license="MIT",
    url="https://github.com/DeveloperJosh/SynDB",
    py_modules=['syndb']
)