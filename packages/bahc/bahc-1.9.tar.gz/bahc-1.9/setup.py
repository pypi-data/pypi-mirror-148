from setuptools import setup

setup(	name='bahc',
      	version='1.9',
      	packages=['bahc'],
	install_requires=[	'numpy>=1.14.2',
				'fastcluster>=1.1.24',
				'statsmodels>= 0.11.1'
				],
	#scripts=['bin/bahc','bin/svhc_benchmark','bin/svhc_plot'],
	author='Christian Bongiorno',
	author_email='christian.bongiorno@centralesupelec.fr',
	license='GPL',
	zip_safe=False

      )

