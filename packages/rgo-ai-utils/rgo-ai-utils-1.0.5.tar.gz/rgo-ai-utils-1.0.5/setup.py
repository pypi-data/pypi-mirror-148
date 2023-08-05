import pathlib
from setuptools import setup

# The directory containing this file
HERE = pathlib.Path(__file__).parent

# The text of the README file
README = (HERE / "README.md").read_text()

# This call to setup() does all the work
setup(
    name="rgo-ai-utils",
    version="1.0.5",
    description="Utils that are shared between rgo ai repos",
    long_description=README,
    long_description_content_type="text/markdown",
    url="https://bitbucket.org/rgo-tech/semanticseg/src/master/",
    packages=["rgo_ai_utils"],
    include_package_data=True,
    install_requires=["PyExifTool", "lxml", 'opencv-python', 'opencv-python-headless', 'tqdm', 'numpy', 'matplotlib'],
)
