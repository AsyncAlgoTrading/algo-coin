from setuptools import setup, find_packages
from codecs import open
import io
import os
import os.path

pjoin = os.path.join
here = os.path.abspath(os.path.dirname(__file__))
name = 'algocoin'


def get_version(file, name='__version__'):
    path = os.path.realpath(file)
    version_ns = {}
    with io.open(path, encoding="utf8") as f:
        exec(f.read(), {}, version_ns)
    return version_ns[name]


version = get_version(pjoin(here, name, '_version.py'))

with open(os.path.join(here, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

requires = [
    'aat>=0.0.4',
]

requires_dev = [
    'flake8>=3.7.8',
    'mock',
    'pybind11>=2.4.0',
    'pytest>=4.3.0',
    'pytest-cov>=2.6.1',
    'Sphinx>=1.8.4',
    'sphinx-markdown-builder>=0.5.2',
] + requires

setup(
    name=name,
    version=version,
    description='Algorithmic trading library for cryptocurrencies',
    long_description=long_description,
    url='https://github.com/timkpaine/algo-coin',
    download_url='https://github.com/timkpaine/algo-coin/archive/v0.0.3.tar.gz',
    author='Tim Paine',
    author_email='timothy.k.paine@gmail.com',
    license='Apache 2.0',
    install_requires=requires,
    extras_require={'dev': requires_dev},

    classifiers=[
        'Development Status :: 3 - Alpha',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
    ],

    keywords='algorithmic trading cryptocurrencies',
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
    entry_points={
        'console_scripts': [
            'algocoin=algocoin:main',
        ],
    },
)
