from setuptools import setup, find_packages

setup(
    name="idse_googletrans",
    version="0.1",
    packages=find_packages(),
    install_requires=[
        'googletrans==4.0.0rc1',
    ],
    entry_points={
        'idse.plugins': [
            'idse_googletrans = idse_googletrans.idse_googletrans:IdseGoogletrans'
        ]
    }
)
