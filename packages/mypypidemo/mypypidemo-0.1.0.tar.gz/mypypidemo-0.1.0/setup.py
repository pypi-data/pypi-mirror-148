import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name='mypypidemo',
    version='0.1.0',
    packages=['mypypidemo'],
    author="Ashok Agarwal",
    author_email="aagarwal.jobs@gmail.com",
    description="A python math package",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/aagarwalnextroll/mypypidemo",

    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
