import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()


install_requires = [
    "numpy>=1.23.2",
    "matplotlib>=3.5.3",
    "pyserial>=3.5",
    "pymodbus>=2.5.3,<2.6",
    "bronkhorst-propar>=1.0",
    ]

setuptools.setup(
     name='pycatalicism',
     version='1.0.1.10',
     author="Denis Leybo",
     author_email="leybodv@gmail.com",
     description="Program controls catalytic activity of materials measurement equipment as well calculations",
     long_description=long_description,
     long_description_content_type="text/markdown",
     url="https://github.com/leybodv/pycatalicism",
     packages=setuptools.find_packages(),
     install_requires = install_requires,
     python_requires='>3.10.0',
     entry_points={
                        'console_scripts': [
                                'pycat=pycatalicism.pycat:main',
                        ]},
     classifiers=[
         "Programming Language :: Python :: 3",
         "License :: OSI Approved :: MIT License",
         "Operating System :: OS Independent",
     ],
 )
