import os
from disutils.core import setup
from disutils.command.install import INSTALL_SCHEMES


version = '.'.join([str(i) for i in __import__('contentbrowser').VERSION])


setup(
    name="contentbrowser",
    version=version,
    url="",
    description="An app to browse through a library of content in a django based cms.",
    author="Andre Engelbrecht",
    author_email='andre@teh-node.co.za',
    license='MIT',
    download_url='https://github.com/andrewebdev/django-contentbrowser/tarball/master',
    packages=find_packages('src'),
    package_dir={'': 'src'},
    keywords=['django', 'content', 'browser', 'library'],
    install_requires=[
        'setuptools',
        'django-appregister == 0.3.1',
    ],
    classifiers=[
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.7',
        'Development Status :: 4 - Beta',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Topic :: Software Development :: Libraries :: Application Frameworks',
    ],
    long_description="""\
"""
)
