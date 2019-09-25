import setuptools

setuptools.setup(
    name="lumigo-log-shipper",
    version="1.0.2",
    author="Lumigo LTD (https://lumigo.io)",
    author_email="support@lumigo.io",
    description="Ship logs to lumigo platform",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/lumigo-io/lumigo-python-log-shipper.git",
    package_dir={"": "src"},
    packages=setuptools.find_packages("src"),
    install_requires=["boto3", "attr"],
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
)
