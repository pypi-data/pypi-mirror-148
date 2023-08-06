import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="dean",
    version="0.8",
    author="Simon Klüttermann",
    author_email="Simon.Kluettermann@gmx.de",
    description="Very minimal statistics module. Useful when you dont have the disk space for numpy",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/psorus/simplestat/",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=2.7',
    install_requires=[
      ],
    download_url='https://github.com/psorus/simplestat/archive/0.8.tar.gz',
    
)  
