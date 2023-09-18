from setuptools import setup, find_packages

#from pylyttlebit import __version__
from git_script import __version__

setup(
    name='git_script',
    version=__version__,
    url='https://github.com/Wilfongjt/lb_lib',
    author='James Wilfong',
    author_email='wilfongjt@gmail.com',
    packages=find_packages()
)