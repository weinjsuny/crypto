from setuptools import setup

setup(
    name='crypto',
    version='4',
    packages=['coinbase_connector',
              'connector_components',
              'bitfinex_connector',
              'configurations',
              'database',
              'images'],
    url='https://github.com/RedBanies3ofThem/crypto',
    license='To be confirmed',
    author='Jonathan Sadighian',
    author_email='jonathan.m.sadighian@gmail.com',
    description='Application to record streaming order and trade tick data from Coinbase and Bitfinex into an Arctic Tick Store',
    install_requires=['requests',
                        'asyncio',
                        'sortedcontainers',
                        'numpy',
                        'websockets',
                        'arctic',
                        'pytz',
                        'pandas',
                        'datetime']
)
