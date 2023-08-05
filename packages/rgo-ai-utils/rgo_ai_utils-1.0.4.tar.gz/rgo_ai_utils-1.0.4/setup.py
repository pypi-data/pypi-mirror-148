import pathlib
from setuptools import setup

# The directory containing this file
HERE = pathlib.Path(__file__).parent

# The text of the README file
README = (HERE / "README.md").read_text()

# This call to setup() does all the work
setup(
    name="rgo_ai_utils",
    version="1.0.4",
    description="Imported as utils_shared. Utils that are shared between rgo ai repos",
    long_description=README,
    long_description_content_type="text/markdown",
    url="https://bitbucket.org/rgo-tech/semanticseg/src/master/",
    packages=["."],
    include_package_data=True,
    install_requires=["PyExifTool", "lxml", 'opencv-python', 'opencv-python-headless', 'tqdm', 'numpy', 'matplotlib'],
)
