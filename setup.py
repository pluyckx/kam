#!/usr/bin/python3

from setuptools import setup,  find_packages

setup(name="kam",
      version="1.0.0",
      description="Keep the machine alive on activity",
      url="http://github.com/pluyckx/kam",
      author="Philip Luyckx",
      author_email="philip.luyckx+kam@gmail.com",
      license="GPLV2",
      packages=find_packages(),
      zip_safe=False,
      install_requeres=['psutils>=1.2.1']
)
