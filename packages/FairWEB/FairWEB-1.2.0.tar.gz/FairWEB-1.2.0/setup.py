from setuptools import setup, find_packages
import os

current = os.getcwd()

setup(
    name='FairWEB',
    version='1.2.0',
    description='Full HTML WebPage Downloader and Data Extractor.',
    url='https://github.com/chazzcoin/fairweb',
    author='ChazzCoin',
    author_email='chazzcoin@gmail.com',
    license='BSD 2-clause',
    packages=find_packages(),
    install_requires=['FCoRE>=1.0.2', 'FairNLP>=1.1.0', 'FairMongo>=1.0.4'],
    classifiers=[
        'Development Status :: 1 - Planning',
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: BSD License',
        'Operating System :: POSIX :: Linux',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
    ]
)