# setup.py
import setuptools

with open("README.md", "r") as infile:
    readme_text = infile.read()

setuptools.setup(
    # Package name and version.
    name="opinf",
    version="0.0.0",

    # Package description, license, and keywords.
    description="Operator inference for data-driven, "
                "non-intrusive model reduction of dynamical systems.",
    license="MIT",
    long_description=readme_text,
    long_description_content_type="text/markdown",
    url="https://github.com/Willcox-Research-Group/opinf",
    classifiers=[
        "Programming Language :: Python :: 3",
        "Natural Language :: English",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Topic :: Scientific/Engineering",
        "Intended Audience :: Science/Research",
        "Development Status :: 1 - Planning",
    ],

    # Humans to contact about this code.
    author="Willcox Research Group",
    author_email="shanemcq@utexas.edu",
    maintainer="Shane A. McQuarrie",
    maintainer_email="shanemcq@utexas.edu",

    # Technical details: source code, dependencies, test suite.
    packages=setuptools.find_packages(where="src"),
    package_dir={"": "src"},
    python_requires=">=3.6",
    install_requires=[],
)
