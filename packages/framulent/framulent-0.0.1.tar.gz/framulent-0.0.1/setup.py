from setuptools import setup, find_namespace_packages


with open("framulent/VERSION") as version_file:
    version = version_file.read().strip()

kwds = {}
try:
    kwds['long_description'] = open('README.md').read()
    kwds['long_description_content_type'] = 'text/markdown'
except IOError:
    pass

setup(
    name="framulent",
    version=version,
    author="William Harvey",
    author_email="drwjharvey@gmail.com",
    description="Cromulent Dataframe Computing",
    url="https://github.com/miiohio/framulent",
    packages=["framulent"] + find_namespace_packages(include=["framulent.*"]),
    package_data={"framulent": ["VERSION", "py.typed"]},
    install_requires=[
        "duckdb >= 0.3.4",
        "mypy >= 0.942",
        "typing_extensions >= 4.2.0"
    ],
    **kwds
)
