import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="hahusms",
    version="0.0.1",
    author="Chapi Menge",
    author_email="chapimenge3@gmail.com",
    description="A simple python package to send SMS via HahuCloud API",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/chapimenge3/hahusms/",
    project_urls={
        "Bug Tracker": "https://github.com/chapimenge3/hahusms/issues"
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    package_dir={"hahusms": "hahusms"},
    packages=setuptools.find_packages(),
    python_requires=">=3.7",
    install_requires=[
        "requests",
    ],
)