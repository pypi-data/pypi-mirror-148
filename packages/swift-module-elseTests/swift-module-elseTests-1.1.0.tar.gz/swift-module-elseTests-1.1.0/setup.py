import setuptools

with open("README.rst", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="swift-module-elseTests",
    version="1.1.0",
    author="Monkey Hammer Copiseded",
    author_email="Wf6350177@163.com",
    description="hey,this is the first app apply to python 2.7 and python above version!",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://pypi.org/project/swift-module-copiseded/",
    project_urls={
        "Bug Tracker": "https://github.com/pypa/sampleproject/issues",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    package_dir={"": "swift apple"},
    packages=setuptools.find_packages(where="swift apple"),
    python_requires=">=2.7",
)
