import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="sddk", # Replace with your own username
    version="3.2",
    author="Vojtech Kase",
    author_email="vojtech.kase@gmail.com",
    description="A package to access sciencedata.dk",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/sdam-au/sddk",
    packages=setuptools.find_packages(),
    install_requires=[
        #"pyarrow>=3",
        #"plotly>=4",
        #"kaleido>=0.2.1",
        "beautifulsoup4>=4",
        "pandas>=1",
        "numpy>=1",
        "requests>=2",
        "matplotlib>=3.3.4",
        #"geopandas",
        #"shapely"
        ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.4',
)
