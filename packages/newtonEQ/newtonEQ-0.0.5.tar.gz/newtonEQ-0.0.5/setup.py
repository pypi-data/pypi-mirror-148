from setuptools import setup, find_packages
 
classifiers = [
  'Development Status :: 5 - Production/Stable',
  'Intended Audience :: Education',
  'Operating System :: Microsoft :: Windows :: Windows 10',
  'License :: OSI Approved :: MIT License',
  'Programming Language :: Python :: 3'
]

 
setup(
  name='newtonEQ',
  version='0.0.5',
  description='A library of useful college physics formulas',
  long_description=open('README.txt').read() + '\n\n' + open('CHANGELOG.txt').read(),
  url='',  
  author='Simon Varadaraj',
  author_email='s.varadaraj03@gmail.com',
  license='MIT', 
  classifiers=classifiers,
  keywords=['physics', 'college', 'science'], 
  packages=find_packages(),
  install_requires=['multipledispatch'] 
)