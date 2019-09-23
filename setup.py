import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="python-log-shipper",
    version="1.0.0",
    author="Lumigo",
    author_email="lumigo.io",
    description="Ship logs to lumigo platform",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/lumigo-io/lumigo-python-log-shipper.git",
    package_dir={"": "src"},
    packages=setuptools.find_packages("src"),
    install_requires=["dacite"],
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
)
