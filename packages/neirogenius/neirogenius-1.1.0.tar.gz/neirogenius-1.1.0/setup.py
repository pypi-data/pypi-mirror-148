from setuptools import setup

with open("README.md", "r", encoding="utf-8") as readme_file:
    long_description = readme_file.read()

setup(
    name="neirogenius",
    version="1.1.0",
    license="Apache License 2.0",
    description="Simple wrapper for the Neirogenius API",
    author="itsSourCream",
    author_email="me@itssourcream.space",
    packages=["neirogenius"],
    install_requires=["requests"],
    url="https://github.com/itsSourCream/NeirogeniusPY",
    long_description=long_description,
    long_description_content_type="text/markdown",
)
