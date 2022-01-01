import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="disto-TwoPTwentySix",
    version="0.0.1",
    author="226",
    author_email="napstaa967alt@gmail.com",
    description="Discord api wrapper for python.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/napstaa967/DISTO",
    project_urls={
        "Bug Tracker": "https://github.com/napstaa967/DISTO/issues",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    package_dir={"": "src"},
    packages=setuptools.find_packages(where="src"),
    python_requires=">=3.10.1",
)