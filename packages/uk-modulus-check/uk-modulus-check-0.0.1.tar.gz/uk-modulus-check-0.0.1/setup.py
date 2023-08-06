import re
from pathlib import Path

from setuptools import setup


def read(*parts):
    return Path(__file__).resolve().parent.joinpath(*parts).read_text().strip()


def read_version():
    regexp = re.compile(r"^__version__\W*=\W*\"([\d.abrc]+)\"")
    for line in read("uk_modulus_check", "__init__.py").splitlines():
        match = regexp.match(line)
        if match is not None:
            return match.group(1)
    else:
        raise RuntimeError("Cannot find version in uk_modulus_check/__init__.py")


with open("README.md", "r") as fh:
    long_description = fh.read()


setup(
    name="uk-modulus-check",
    version=read_version(),
    description="A thing to check UK bank sort code and IBAN",
    long_description=long_description,
    long_description_content_type="text/markdown",
    platforms=["macOS", "POSIX", "Windows"],
    author="ANNA",
    python_requires=">=3.10",
    project_urls={},
    author_email="yury.pliner@gmail.com",
    license="MIT",
    packages=["uk_modulus_check"],
    package_dir={"uk_modulus_check": "./uk_modulus_check"},
    package_data={"uk_modulus_check": ["py.typed"]},
    include_package_data=True,
)
