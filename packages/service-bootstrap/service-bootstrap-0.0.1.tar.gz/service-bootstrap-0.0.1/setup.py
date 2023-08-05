import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()


setuptools.setup(
    name="service-bootstrap",
    version="0.0.1",
    description="Framework for setting up service",
    author="Rafał Zarajczyk",
    author_email="rzarajczyk@gmail.com",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/rzarajczyk/homie-helpers",
    keywords=["HOMIE", "MQTT"],
    packages=['bootstrap'],
    package_dir={'bootstrap': './src/bootstrap'},
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires=["pyyaml~=6.0", "tzlocal"],
)
