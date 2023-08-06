import setuptools

setuptools.setup(
    name="pg_database_manager",
    version="0.0.1",
    author="Zubkov Maxim",
    author_email="maksim.zubkov1234@gmil.com",
    description="",
    url="https://github.com/maxonclaxon/pg_database_manager",
    project_urls={
        "Bug Tracker": "https://github.com/maxonclaxon/pg_database_manager/issues",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    package_dir={"": "database_manager"},
    packages=setuptools.find_packages(where="database_manager"),
    python_requires=">=3.9",
)