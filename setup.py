import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()


setuptools.setup(
     name='pycatalicism',
     version='0.1',
     scripts=['pycat'] ,
     author="Denis Leybo",
     author_email="leybodv@gmail.com",
     description="Program controls catalytic activity of materials measurement equipment as well calculations",
     long_description=long_description,
   long_description_content_type="text/markdown",
     url="https://github.com/leybodv/pycatalicism",
     packages=setuptools.find_packages(),
     classifiers=[
         "Programming Language :: Python :: 3",
         "License :: OSI Approved :: MIT License",
         "Operating System :: OS Independent",
     ],
 )
