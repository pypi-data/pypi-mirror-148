from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="msds-tdm",
    version="1.0.2",
    author="Soutick Saha, Chintan Sawla",
    author_email="soutick2010@gmail.com, sawlachintan@gmail.com",
    description="MSDS Package",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/sawlachintan/msds-library",
    project_urls={
        "Bug Tracker": "https://github.com/sawlachintan/msds-library/issues",
    },
    packages=find_packages(exclude="tests"),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    package_data={
        'msds_tdm': ['*.xlsx']
    },
    python_requires=">=3.6",
    install_requires=[
        "pandas==1.2.4",
        "pdfplumber==0.6.0",
        "openpyxl",
    ],
)
