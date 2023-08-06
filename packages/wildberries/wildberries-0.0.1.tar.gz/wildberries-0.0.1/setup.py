import setuptools

with open("README.md", "r") as fh:
	long_description = fh.read()

requirements = ["requests>=2.27.1"]

setuptools.setup(
	name="wildberries",
	version="0.0.1",
	author="Konstantin Belov",
	author_email="russianosint@gmail.com",
	description="Unofficial python library for wildberries",
	long_description=long_description,
	long_description_content_type="text/markdown",
	url="https://github.com/russianosint/wildberries",
	packages=setuptools.find_packages(),
	install_requires=requirements,
	classifiers=[
		"Programming Language :: Python :: 3.8",
		"License :: OSI Approved :: MIT License",
		"Operating System :: OS Independent",
	],
	python_requires='>=3.6',
)