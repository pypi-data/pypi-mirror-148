from setuptools import setup, find_packages
import os, io


keyword = "MITM Manipulate IPAddress Network-Calculate NetMet PyNews PyWeathers".split(" ")

def Find_Packages():
	getdirectory = os.getcwd()
	fpath = os.path.join(getdirectory, 'NetMet')
	fpath = fpath.replace("\\", "/")
	if os.path.exists(fpath):
		return ['NetMet']
	else:
		return find_packages()

with open('README.md') as f:
    long_description = f.read()

with open('requirements.txt') as f:
    required = f.read().splitlines()

__VERSIONS__ = 1
mails = '<LCFHERSHELL@TUTANOTA.COM>'.lower()

setup(
	name='NetMet',
    version=__VERSIONS__,
    long_description_content_type= "text/markdown",
    long_description=long_description,
    author="alfiandecker2",
    author_email=mails,
    url='https://github.com/LcfherShell/NetMet.git',
    license= 'MIT',
    packages= Find_Packages(),
    required=required,
    classifiers=[
		'Development Status :: 1 - Planning',
		'Intended Audience :: Developers',
		'License :: OSI Approved :: MIT License',
		'Programming Language :: Cython',
		'Programming Language :: Python',
		'Operating System :: MacOS',
		'Operating System :: POSIX',
		'Operating System :: Unix',
		'Operating System :: Microsoft :: Windows'
		],
    python_requires='>=2.6, !=3.0.*, !=3.1.*, !=3.2.*, !=3.3.*, <4',
    zip_safe= False,
    keywords= keyword
      )