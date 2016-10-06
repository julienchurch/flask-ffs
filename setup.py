from setuptools import setup, find_packages
from codecs import open
from os import path

pwd = path.abspath(path.dirname(__file__))

with open(path.join(pwd, 'README.rst'), encoding='utf-8') as f:
  long_description = f.read()

CLASSIFIERS = [
    'Development Status :: 3 - Alpha'
  , 'Environment :: Web Environment'
  , 'Framework :: Flask'
  , 'Intended Audience :: Developers'
  , 'License :: OSI Approved :: MIT License'
  , 'Programming Language :: Python :: 3.3'
  , 'Programming Language :: Python :: 3.4'
  , 'Programming Language :: Python :: 3.5'
  , 'Topic :: Internet :: WWW/HTTP :: Dynamic Content'
  , 'Topic :: Software Development :: Libraries'
  ]

setup(
    name = 'flask-ffs',
    version = '0.3.0',
    description='A Flask library for the storage and retrieval of images on the file system.',
    long_description=long_description,
    url='https://github.com/julienchurch/ffs-images',
    download_url='https://github.com/julienchurch/flask-fs-images/tarball/0.1.0',
    author='Julien Church',
    author_email='julienchurch@gmail.com',
    license='MIT',
    classifiers=CLASSIFIERS,
    keywords='filesystem image',
    packages=find_packages(),
    install_requires=['Flask'],
    extras_require={},
    package_data={},
    data_files=[],
    entry_points={}
    )
