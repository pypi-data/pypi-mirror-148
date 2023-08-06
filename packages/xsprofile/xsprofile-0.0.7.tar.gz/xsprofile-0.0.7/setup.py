import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()
    
setuptools.setup(
    name="xsprofile",
    version="0.0.7",
    author="Will Conley",
    author_email="EcoRioGeo@gmail.com",
    long_description=long_description,
    long_description_content_type="text/markdown",
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.9",
        "License :: OSI Approved :: GNU General Public License v2 (GPLv2)",
        "Operating System :: Microsoft :: Windows :: Windows 10"
        ],
    py_modules=['utils'],
    package_dir={'':'src'},
    url="https://gitlab.com/Geomorph/xsprofile",
    python_requires=">=3.9",
    install_requires=[
        "geopandas",
        "rasterio",
        "matplotlib"
        ]
)