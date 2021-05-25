import pathlib, platform
from setuptools import find_packages, setup


HERE = pathlib.Path(__file__).parent
README = (HERE / "README.md").read_text()

if platform.system() == 'Windows':
    I_R = [
        'cython==0.29.22',
        'bitshares',
        'pypubsub',
        'kivy[base]',
        'kivymd'
    ]
else:
    I_R = [
        'cython',
        'bitshares',
        'pypubsub',
        'kivy',
        'kivymd'
    ]

setup(
    name='PoolTool',
    version='2.1.0',
    description='A simple Python tool to help anyone use Liquidity Pools on the BitShares blockchain.',
    long_description=README,
    long_description_content_type='text/markdown',
    author='Brendan Jensen (iamredbar)',
    author_email='iamredbar@protonmail.com',
    license='MIT',
    url='https://github.com/iamredbar/PoolTool',
    packages=find_packages(),
    install_requires=I_R,
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
