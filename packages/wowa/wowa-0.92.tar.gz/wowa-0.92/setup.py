from setuptools import setup

classifiers = [
    "Programming Language :: Python :: 3",
    "License :: OSI Approved :: GNU General Public License v3 (GPLv3)"
]

with open("README.md", "r") as fh:
    long_description = fh.read()

setup( 
    name="wowa",
    version="0.92",
    description="Calculate weighted OWA functions and extending bivariate means",
    long_description=open('README.md').read(),
    long_description_content_type="text/markdown",
    url="",
    author='Gleb Beliakov, Norbert Henseler',
    author_email='norbert.henseler@deakin.edu.au',
    license_file='LICENSE',
    py_modules=['wowa'],
    package_dir={'': 'src'},
    install_requires=['cffi>=1.0.0'],
    setup_requires=['cffi>=1.0.0'],
    cffi_modules=['./src/buildWowa.py:ffibuilder'],
    include_package_data=True,
    package_data={'':['tests/test.py']},
)

    
    