from setuptools import setup, find_packages
import pathlib
from setuptools import setup


VERSION = '0.0.5'
DESCRIPTION = 'Inofficial API Wrapper for Unsplash API'

# The directory containing this file
HERE = pathlib.Path(__file__).parent

# The text of the README file
LONG_DESCRIPTION = (HERE / "README.md").read_text()


# Setting up
setup(
    name="unsplashapi",
    version=VERSION,
    author="SimonStaehli",
    author_email="<simon.staehli@students.fhnw.ch>",
    description=DESCRIPTION,
    long_description_content_type="text/markdown",
    long_description=LONG_DESCRIPTION,
    packages=find_packages(),
    install_requires=['requests'],
    keywords=['python', 'api', 'unsplash api', 'unsplash', 'unsplashapi'],
    python_requires='>=3',
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ]
)