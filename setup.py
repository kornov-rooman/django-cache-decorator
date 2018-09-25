from setuptools import setup, find_packages

from django_cache_decorator import __version__

with open('README.rst', 'r') as f:
    long_description = f.read()

setup(
    name='django-cache-decorator',
    version=__version__,
    packages=find_packages(),
    url='https://github.com/kornov-rooman/django-cache-decorator',
    license='MIT',
    author='A Piece of Watermelon',
    author_email='kornov.rooman@gmail.com',
    description='Django cache decorator',
    long_description=long_description,
    classifiers=[
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
        'License :: OSI Approved :: MIT License',
    ],
    requires=['django']
)
