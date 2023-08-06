
import setuptools

# Reads the content of your README.md into a variable to be used in the setup below
with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name='CloserLookFewShot',                           # should match the package folder
    packages=['CloserLookFewShot'],                 	# should match the package folder
    version='0.0.2',                                		# important for updates
    license='Attribution-NonCommercial 4.0 International',	# should match your chosen license
    description='CloserLookFewShot implementation',
    long_description=long_description,              	# loads your README.md
    long_description_content_type="text/markdown",  	# README.md is of type 'markdown'
    author='VinC',
    author_email='vinchengme@gmail.com',
    url='https://github.com/yiminzme/CloserLookFewShot', 
    project_urls = {                                	# Optional
        "Bug Tracker": "https://github.com/wyharveychen/CloserLookFewShot/issues"
    },
    install_requires=[									# list all packages that your package uses
        'pytorch',
        'h5py',
                      ],
    keywords=["meta learning", "Closer look few shot"], # descriptive meta-data
    classifiers=[                                   	# https://pypi.org/classifiers
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Documentation',
        'Programming Language :: Python :: 3.7',
    ],
    
    download_url="https://github.com/yiminzme/CloserLookFewShot/archive/refs/tags/v0.0.2.tar.gz",
)