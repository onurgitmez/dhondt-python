from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as f:
    long_description = f.read()

setup(
    name="dhondt",
    version="0.1",
    packages=find_packages(),
    package_data={
        'dhondt': ['data/*']
    },
    install_requires=[
        "pandas"
    ],
    author="Ali Onur Gitmez",
    author_email="alionur@gitmez.com",
    description="A package to simulate elections using the D'Hondt method.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    license="MIT",
    keywords="election simulation dhondt",
    url="https://github.com/onurgitmez/dhondt-python",
    include_package_data=True
)
