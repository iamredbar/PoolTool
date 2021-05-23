import pathlib

from setuptools import find_packages, setup


HERE = pathlib.Path(__file__).parent
README = (HERE / "README.md").read_text()

setup(
    name='PoolTool',
    version='2.0.5',
    description='A simple Python tool to help anyone use Liquidity Pools on the BitShares blockchain.',
    long_description=README,
    long_description_content_type='text/markdown',
    author='Brendan Jensen (iamredbar)',
    author_email='iamredbar@protonmail.com',
    license='MIT',
    url='https://github.com/iamredbar/PoolTool',
    packages=find_packages(),
    install_requires=[
        'kivy[base]',
        'kivymd',
        'bitshares',
        'pypubsub'
    ],
    classifiers=[
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9'
    ],
    package_data={
        'PoolTool': ['*.kv', 'assets/*.jpg'],
    },
    entry_points={
        'console_scripts': [
            'PoolTool = PoolTool.controller:main'
        ]
    }
)
