import setuptools

with open("README.txt", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name		= "cjpy", 
    version		= "0.2.5",
    author		= "Jaesub Hong",
    author_email	= "jhong@cfa.harvard.edu",
    packages	= ['cjpy'],

    description	   = "Command liner with JSON based input file",
    long_description = long_description,
    long_description_content_type="text/markdown",

    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.5',
    install_requires=[
		'textwrap3>=0.9.2'
	    ]
)
