"""setup.py for mockend"""

__author__ = "Mohsen Ghorbani"
__email__ = "m.ghorbani2357@gmail.com"
__copyright__ = "Copyright 2022, Mohsen Ghorbani"

from setuptools import setup, find_packages

import versioneer

REQUIREMENTS = filter(None, open('requirements.txt').read().splitlines())

setup(name='mockend',
      author=__author__,
      author_email=__email__,
      url="https://github.com/mghorbani2357/mockend",
      license="MIT",
      zip_safe=False,
      version=versioneer.get_version(),
      cmdclass=versioneer.get_cmdclass(),
      packages=find_packages(),
      install_requires=list(REQUIREMENTS),
      entry_points={
          'console_scripts': ['mockend=mockend.__main__:rawFEED'],
      },
      classifiers=[k for k in open('CLASSIFIERS').read().split('\n') if k],
      long_description=open('README.rst').read(),
      long_description_content_type='text/x-rst',
      description='Mockend is a simple tool for mocking endpoints',
      )
