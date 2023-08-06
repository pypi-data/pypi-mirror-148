import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="yagnesh",
    version="0.0.1",
    author="Example Author",
    author_email="author@example.com",
    description="A small example package",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/pypa/sampleproject",
    project_urls={
        "Bug Tracker": "https://github.com/pypa/sampleproject/issues",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    package_dir={"": "myapp"},
    packages=setuptools.find_packages(where="myapp"),
    python_requires=">=3.6",

    entry_points={
        'lms.djangoapp': [
            "myapp = myapp.apps:MyappConfig",
        ],
        'cms.djangoapp': [
            "myapp = myapp.apps:MyappConfig",
        ],
        'openedx.block_structure_transformer': [
            'load_date_data = myapp.field_data:DateOverrideTransformer'
        ],

    },
)
