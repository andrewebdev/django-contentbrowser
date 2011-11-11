from setuptools import setup, find_packages

setup(
    name="contentbrowser",
    version="0.1",
    url="",
    description="An app to manage content in any django based cms.",
    author="Andre Engelbrecht",
    packages=find_packages('src'),
    package_dir={'': 'src'},
    install_requires=[
        'setuptools',
    ],
)
