import setuptools

setuptools.setup(
    name="DMS_APP",
    version="0.0.1",
    author="Datamoulds",
    author_email="author@example.com",
    description="A small example package",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    package_dir={"": "app"},
    packages=setuptools.find_packages(where="app"),
    python_requires=">=3.8.8",
)