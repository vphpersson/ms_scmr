from setuptools import setup, find_packages
setup(
    name='ms_scmr',
    version='0.1',
    packages=find_packages(),
    install_requires=[
        'rpc @ https://github.com/vphpersson/rpc/tarball/master',
        'msdsalgs @ https://github.com/vphpersson/msdsalgs/tarball/master'
    ]
)
