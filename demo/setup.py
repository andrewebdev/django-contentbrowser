from setuptools import setup, find_packages

setup(
    name="demo",
    version="0.1",
    url="",
    author="Andre Engelbrecht",
    packages=find_packages('src'),
    package_dir={'': 'src'},
    install_requires=[
        'setuptools',
    ],
)
