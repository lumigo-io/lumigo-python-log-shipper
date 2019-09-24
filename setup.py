import os
import setuptools

VERSION_PATH = os.path.join(
    os.path.dirname(__file__), "src", "lumigo_log_shipper", "VERSION"
)

setuptools.setup(
    name="python-log-shipper",
    version=open(VERSION_PATH).read(),
    author="Lumigo LTD (https://lumigo.io)",
    author_email="support@lumigo.io",
    description="Ship logs to lumigo platform",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/lumigo-io/lumigo-python-log-shipper.git",
    package_dir={"": "src"},
    packages=setuptools.find_packages("src"),
    install_requires=[],
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
)
