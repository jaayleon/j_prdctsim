import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="j_prdctsim",
    version="0.0.1",
    author="J Leon Batulayan",
    author_email="jleon.batulayan@gmail.com",
    description="A small example package",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/jaayleon/j_prdctsim",
    project_urls={

    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    package_dir={"j_prdctsim": "j_prdctsim"},
    packages=setuptools.find_packages(),
    python_requires=">=3.6",
)
