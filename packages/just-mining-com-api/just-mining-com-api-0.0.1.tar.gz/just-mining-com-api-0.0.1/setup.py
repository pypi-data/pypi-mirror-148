import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="just-mining-com-api",            # This is the name of the package
    version="0.0.1",                        # The initial release version
    author="Nicolas MARTIN",                # Full name of the author
    description="Python wrapper for just-mining.com API",
    long_description=long_description,      # Long description read from the the readme file
    long_description_content_type="text/markdown",
    url="https://github.com/PhunkyBob/just-mining-com-api",
    project_urls={
        "Bug Tracker": "https://github.com/PhunkyBob/just-mining-com-api/issues",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Operating System :: OS Independent",
    ],                                      # Information to filter the project on PyPi website
    py_modules=["just_mining_com_api"],
    package_dir={'':'just_mining_com_api/src'},                 # Directory of the source code of the package
    packages=setuptools.find_packages(),    # List of all python modules to be installed
    python_requires='>=3.6',                # Minimum version requirement of the package
    install_requires=['requests']           # Install other dependencies if any
)