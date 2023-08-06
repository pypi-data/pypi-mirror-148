import setuptools
with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()
setuptools.setup(
    name="votes_package_x21127336",
    # Replace with your own username above
    version="0.0.1",
    author="Rohit Salvi",
    author_email="x21127336@student.ncirl.ie",
    description="A package created to handle votes",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/rohitsalvi23/x21127336-CPP-Library.git",
    packages=setuptools.find_packages(),
    # if you have libraries that your module/package/library
    #you would include them in the install_requires argument
    install_requires=[''],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
python_requires='>=3.6',
)