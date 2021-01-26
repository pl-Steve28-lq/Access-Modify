import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="Access-Modify",
    version="1.0.4",
    author="Steve28",
    author_email="holiday28784@gmail.com",
    description="Python module which includes private, or protected class methods for your classes.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/pl-Steve28-lq/PythonUtils",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
