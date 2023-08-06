from setuptools import setup
import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name='ebesumusic',
    version='5.2.8',
    description='ebesumusic python discord',
    author= 'Kushal Bhavsar',
    url = 'https://github.com/Spidy20/PyMusic_Player',
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=setuptools.find_packages(),
    keywords=['music player python', 'music player tkinter', 'music player gui'],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires = [
        'aiohttp>=3.8.1',
        'async-timeout>=4.0.2',
        'wavelink>=1.2.4'
    ]
)
