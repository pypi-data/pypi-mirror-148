from setuptools import find_packages, setup

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name="ceader",
    version="0.0.2",
    license="MIT",
    author="Kamil Jankowski",
    author_email="mr.kamil.jankowski@gmail.com",
    packages=find_packages(exclude=("./tests",)),
    url="https://github.com/cerebre-io/ceader",
    keywords="Header",
    python_requiers=">=3.8",
    include_package_data=True,
    description="Tool for automatically adding a header to files in the form of a comment.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    entry_points={
        "console_scripts": [
            "ceader=ceader.__main__:main",
        ]
    },
)

# python setup.py sdist
# python setup.py sdist bdist_wheel
# python -m twine upload --verbose --repository testpypi dist/*
# ceader --mode add_header --files-dir data --header-path tests/data/header.txt --extensions .py .yaml --debug
