from setuptools import setup, find_packages

setup(
    name="idse_googletrans",
    version="0.1",
    packages=find_packages(),
    entry_points={
        'idse.plugins': [
            'idse_googletrans = idse_googletrans.idse_googletrans:IdseGoogletrans'
        ]
    }
)
