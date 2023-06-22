from setuptools import setup, find_packages

from lb_lib import __version__

setup(
    name='lb_lib',
    version=__version__,
    url='https://github.com/Wilfongjt/lb_lib',
    author='James Wilfong',
    author_email='wilfongjt@gmail.com',
    packages=find_packages()
)