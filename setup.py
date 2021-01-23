# -*- coding:utf-8 -*-  
# __auth__ = mocobk
# email: mailmzb@qq.com

import setuptools

with open("README.md", "r", encoding='utf-8') as fh:
    long_description = fh.read()

setuptools.setup(
    name="py-mock",
    version="1.2.0",
    author="mocobk",
    author_email="mailmzb@qq.com",
    description="Mock.js for Python3",
    long_description=long_description,
    long_description_content_type="text/markdown",
    keywords="pymock,Mock,Mock.js,better-mock",
    url="https://github.com/mocobk/pymock",
    packages=['pymock'],
    install_requires=['py-mini-racer'],
    classifiers=[
        "Programming Language :: Python :: 3 :: Only",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    package_data={'pymock': ['js/*.js']},
)
