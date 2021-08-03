from setuptools import setup, find_packages
setup(
    name='ms_scmr',
    version='0.1',
    packages=find_packages(),
    install_requires=[
        'rpc @ git+ssh://git@github.com/vphpersson/rpc.git#egg=rpc',
        'msdsalgs @ git+ssh://git@github.com/vphpersson/msdsalgs.git#egg=msdsalgs',
        'msdsalgs @ git+ssh://git@github.com/vphpersson/ndr.git#egg=ndr'
    ]
)
