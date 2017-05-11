import setuptools

setuptools.setup(
	name = 'pysevone',
	version = '0.0.1',
	author = 'Mike Cronce',
	author_email = 'mcronce@sevone.com',
	description = (
		'A Python implementation of the SevOne APIs, along with a command-line'
		'utility that uses that API'
	),
	license = 'MIT',
	keywords = 'sevone',
	url = 'http://www.github.com/sevone/pysevone',
	install_requires = [
		'argparse',
		'configparser',
		'requests'
	],
	packages = ['sevrest'],
	scripts = ['sevone']
)

