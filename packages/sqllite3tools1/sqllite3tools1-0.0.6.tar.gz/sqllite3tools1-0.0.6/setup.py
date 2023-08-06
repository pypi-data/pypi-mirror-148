from setuptools import setup, find_packages
import os

VERSION = '0.0.6'
DESCRIPTION = 'SQLITE tools'
LONG_DESCRIPTION = 'this package is designed to manage the database'

about = {}
here = os.path.abspath(os.path.dirname(__file__))
with open(os.path.join(here, "sqllite3tools1", "__version__.py"), "r") as f:
    exec(f.read(), about)

with open("README.md", "r") as f:
    readme = f.read()

# Setting up
setup(
    name="sqllite3tools1",
    version=VERSION,
    author="SanjarbekDev",
    author_email="<sanjarbeksodiqov0302@gmail.com>",
    description=DESCRIPTION,
    long_description=readme,
    long_description_content_type="text/markdown",
    packages=find_packages(),
    keywords=['execute','commit','fetchone','fetchall','create_table','info','select'],
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ]
)