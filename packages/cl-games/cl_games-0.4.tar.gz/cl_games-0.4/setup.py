import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="cl_games",
    version="0.4",
    author="Aaranyak Ghosh",
    author_email="aaranyak.ghosh@gmail.com",
    description="A package for creating video games for command line",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/aaranyak/cl_games_V1-beta",
    project_urls={
        "Bug Tracker": "https://github.com/pypa/sampleproject/issues",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    package_dir={"": "src"},
    packages=setuptools.find_packages(where="src"),
    python_requires=">=3.6",
    install_requires=['pynput'],
)
