#!/usr/bin/env python

"""The setup script."""

from setuptools import setup, find_packages

requirements = ['click', 'pip', 'requests','tqdm', 'fastapi', 'uvicorn',
                'aiofiles', 'python-multipart', 'typing', 'numpy==1.22.4', 'numba==0.56.4', 'biopython', 'selenium']


test_requirements = ['pytest>=3', ]

setup(
    author="Michael Lee, Sergei Kuznetsov, Evenezer Yiheego, Nina Wetzig",
    author_email='s0sekuzn@uni-bonn.de, s0niwetz@uni-bonn.de',
    python_requires='>=3.6',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
    ],
    description="Group3 Package",
    entry_points={
        'console_scripts': [
            'src=src.cli:cli',
        ],
    },
    install_requires=requirements,
    license="MIT license",
    include_package_data=True,
    keywords='src',
    name='src',
    packages=find_packages(include=['src', 'src.*']),
    test_suite='tests',
    tests_require=test_requirements,
    version='0.1.0',
    zip_safe=False,
)
