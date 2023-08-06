from setuptools import setup, find_packages

with open("README.md", "r") as f:
    long_desc = f.read()

setup(
    name='mynum',
    version='0.0.2',
    packages=find_packages(),
    url='https://biningo.github.io/',
    license='MIT',
    author='Example Author',
    author_email='icepan5@gmail.com',
    description='test',
    long_description=long_desc,
    long_description_content_type="text/markdown",
    install_requires=[],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6'
)
