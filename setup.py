from setuptools import setup, find_packages
from codecs import open
import os
import os.path

here = os.path.abspath(os.path.dirname(__file__))

with open(os.path.join(here, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

with open(os.path.join(here, 'requirements.txt'), encoding='utf-8') as f:
    requires = [s for s in f.read().split('\n') if not s.startswith('-e')]

setup(
    name='algocoin',
    version='0.0.3',
    description='Algorithmic trading library for cryptocurrencies',
    long_description=long_description,
    url='https://github.com/timkpaine/algo-coin',
    download_url='https://github.com/timkpaine/algo-coin/archive/v0.0.3.tar.gz',
    author='Tim Paine',
    author_email='timothy.k.paine@gmail.com',
    license='Apache 2.0',
    install_requires=requires,

    classifiers=[
        'Development Status :: 3 - Alpha',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
    ],

    keywords='algorithmic trading cryptocurrencies',
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
    extras_require={'dev': requires + ['pytest', 'pytest-cov', 'pylint', 'flake8']},
    entry_points={
        'console_scripts': [
            'algocoin=algocoin:main',
        ],
    },
)
