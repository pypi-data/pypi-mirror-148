import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="yagnesh_demo",
    version="0.0.1",
    author="yagnesh",
    author_email="yagneshnayi7@gmail.com",
    description="my Openedx ",
    long_description=long_description,
    long_description_content_type="text/markdown",
   
    project_urls={
        "Bug Tracker": "https://github.com/pypa/sampleproject/issues",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    package_dir={"": "mydemo"},
    packages=setuptools.find_packages(where="mydemo"),
    python_requires=">=3.6",
)
