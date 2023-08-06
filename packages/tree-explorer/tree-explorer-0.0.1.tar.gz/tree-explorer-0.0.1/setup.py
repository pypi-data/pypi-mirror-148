import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

with open('requirements.txt', 'r') as file:
    requirements = file.read()

setuptools.setup(
    name="tree-explorer",
    version="0.0.1",
    author="Alessandro Gussoni",
    author_email="alessandro.gussoni@hotmail.com",
    description="Python package to explore Decision tree based model structure",
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=setuptools.find_packages(exclude="test"),
    license='MIT',
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',

    install_requires=requirements.split('\n')
)
