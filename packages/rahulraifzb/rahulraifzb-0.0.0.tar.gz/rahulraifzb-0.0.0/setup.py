import os
import codecs
from setuptools import  setup,find_packages

here = os.path.abspath(os.path.dirname(__file__))

with codecs.open(os.path.join(here,"README.md"),encoding="utf-8") as fh:
    long_description = "\n" + fh.read()

setup(
    name="rahulraifzb",
    packages=["rahulraifzb"],
    versions="0.1",
    license="MIT",
    description="This is versy basic package which is used to return the hello",
    author="Rahul Rai",
    author_email="rrai06125@gmail.com",
    url="https://github.com/Rahulraifzb/hello.git",
    keywords=["hello","some","meaning"],
    install_require=[
        "django",
        "crispy_forms"
    ],
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ]
)