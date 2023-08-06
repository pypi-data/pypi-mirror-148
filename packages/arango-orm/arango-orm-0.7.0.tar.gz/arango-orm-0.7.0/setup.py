from setuptools import setup, find_packages

requires = ["six", "python-arango>=4.0", "marshmallow"]
setup(
    name="arango-orm",
    version="0.7.0",
    description="A SQLAlchemy like ORM implementation for arangodb",
    long_description=(
        "A SQLAlchemy like ORM implementation using "
        " python-arangoas the backend library"
    ),
    classifiers=["Programming Language :: Python"],
    author="Kashif Iftikhar",
    author_email="kashif@compulife.com.pk",
    url="https://github.com/threatify/arango-orm",
    license="GNU General Public License v3 (GPLv3)",
    keywords="arangodb orm python",
    packages=find_packages(),
    install_requires=requires,
)
