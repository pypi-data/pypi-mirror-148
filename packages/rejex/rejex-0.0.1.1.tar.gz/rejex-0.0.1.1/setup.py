import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="rejex",
    version="0.0.1.1",
    author="Terroid",
    author_email="skandabhairava@gmail.com",
    description="Tool used to build regex expressions for python",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/skandabhairava/Rejex",
    project_urls={
        "Bug Tracker": "https://github.com/skandabhairava/Rejex/issues",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    package_dir={"": "src"},
    packages=setuptools.find_packages(where="src"),
    python_requires=">=3.6",
)