from setuptools import setup
from os import path

# directory containing this file
file_dir = path.abspath(path.dirname(__file__))

# Add this so the README file can be visible on the website
with open(path.join(file_dir, 'README.md'), encoding='utf-8') as f:
	description = f.read()

setup(
	name='idjwi',
	version='0.1.0',
	author='Muhoza Ursus Bizumuremyi',
	long_description= description,
	long_description_content_type="text/markdown",
	author_email='writetoursus@gmail.com',
	url="https://idjwi.readthedocs.io/",
	license='MIT',
	packages=['idjwi'],
	include_package_data= True,
	install_requires=['numpy', 'pandas'],
	classifiers=[
		"Intended Audience :: Developers",
		"License :: OSI Approved :: MIT License",
		"Programming Language :: Python",
		"Programming Language :: Python :: 3",
		"Programming Language :: Python :: 3.6",
		"Programming Language :: Python :: 3.7",
		"Programming Language :: Python :: 3.8",
		"Programming Language :: Python :: 3.9",
		"Operating System :: OS Independent"]

)

