import setuptools

with open("README.md", 'r', encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="currency-api-py",
    version="0.1.0",
    author="Marseel Eeso",
    author_email="marseeleeso@gmail.com",
    description="A python async wrapper for the currency-api API",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Marseel-E/currency-api-py",
    project_urls={
        "Bug Tracker": "https://github.com/Marseel-E/currency-api-py/issues"
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    packages=['currencyApi'],
    python_requires=">=3.8",
)
