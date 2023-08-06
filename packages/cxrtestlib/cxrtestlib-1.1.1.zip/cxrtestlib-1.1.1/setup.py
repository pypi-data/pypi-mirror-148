# from  distutils.core import setup
from setuptools import setup


def readme_file():
    with open("README.rst", encoding="utf-8") as rf:
        return rf.read()


setup(name="cxrtestlib", version="1.1.1", description="thie is nb lib",
      packages=["cxrtestlib"], py_modules=["Tool"], author="Cxr", author_email="1318304701@qq.com",
      long_description=readme_file(), license="MIT")
