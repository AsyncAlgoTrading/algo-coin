from setuptools import setup, find_packages
from distutils.extension import Extension
from codecs import open
import os
import os.path

here = os.path.abspath(os.path.dirname(__file__))

with open(os.path.join(here, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

sources = []
outputs = []
for path, subdirs, files in os.walk('algocoin/src'):
    for name in files:
        fp = os.path.join(path, name)
        if fp.endswith('cpp'):
            outputs.append(fp.replace('.cpp', '').replace('/src', ''))
            sources.append(fp)

print(outputs)

setup(
    name='algocoin',
    version='0.0.3',
    description='Algorithmic trading library for cryptocurrencies',
    long_description=long_description,
    url='https://github.com/timkpaine/algo-coin',
    download_url='https://github.com/timkpaine/algo-coin/archive/v0.0.3.tar.gz',
    author='Tim Paine',
    author_email='timothy.k.paine@gmail.com',
    license='GPL',

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

    # You can just specify the packages manually here if your project is
    # simple. Or you can use find_packages().
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
    #   py_modules=["my_module"],

    # install_requires=['peppercorn'],

    # extras_require={
    #     'dev': ['check-manifest'],
    #     'test': ['coverage'],
    # },

    # package_data={
    #     'sample': ['package_data.dat'],
    # },

    # data_files=[('my_data', ['data/data_file'])],

    entry_points={
        'console_scripts': [
            'algocoin=algocoin:main',
        ],
    },

    ext_modules=[
        # Extension('algocoin/_extension', include_dirs=['algocoin/include'], sources=['algocoin/src/test.cpp'], libraries=['boost_python']),
        Extension(x,
                  include_dirs=["algocoin/include"],
                  sources=[y],
                  libraries=["boost_python"]) for x, y in zip(outputs, sources)
    ]
)
