from setuptools import setup, find_packages

setup(
    name='idse',
    version='0.1.0',
    packages=find_packages(),
    install_requires=[
        'pexpect==4.9.0',
        'googletrans==4.0.0-rc1',
    ],
    entry_points={
        'console_scripts': [
            'idse=idse.idse:main',
        ],
    },
    author='Shota Iuchi',
    author_email='shotaiuchi.develop@gmail.com',
    description='',
    long_description=open('README.md').read(),
    license='MIT',
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
    ],
    keywords='crop, image, adb, screenshot',
    url='https://github.com/ShotaIuchi/crop-image',
)
