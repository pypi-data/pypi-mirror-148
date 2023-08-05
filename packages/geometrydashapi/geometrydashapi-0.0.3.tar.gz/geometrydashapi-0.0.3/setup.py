from setuptools import setup, find_packages
 
classifiers = [
  'Development Status :: 5 - Production/Stable',
  'Intended Audience :: Education',
  'Operating System :: Microsoft :: Windows :: Windows 10',
  'License :: OSI Approved :: MIT License',
  'Programming Language :: Python :: 3'
]
 
setup(
  name='geometrydashapi',
  version='0.0.3',
  description='Geometry Dash API for coding in Python.',
  long_description=open('README.txt').read() + '\n\n' + open('CHANGELOG.txt').read(),
  url='https://www.youtube.com/channel/UCCmKgOlJwEEZIwRhGxcaL4Q',  
  author='Rylixmods SFC',
  author_email='rylixmods@gmail.com',
  license='MIT', 
  classifiers=classifiers,
  keywords=['gd', 'geometrydash', 'gdhacking', 'gdcoding', 'geomnetrydashapi', 'gdapi'], 
  packages=find_packages(),
  install_requires=['requests'] 
)
