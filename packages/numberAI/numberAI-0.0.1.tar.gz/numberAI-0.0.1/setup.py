from setuptools import setup, find_packages
 
classifiers = [
  'Development Status :: 5 - Production/Stable',
  'Intended Audience :: Education',
  'Operating System :: Microsoft :: Windows :: Windows 10',
  'License :: OSI Approved :: MIT License',
  'Programming Language :: Python :: 3'
]
 
setup(
  name='numberAI',
  version='0.0.1',
  description='A simple machine learning libary for generating numbers',
  long_description="Its point is to teach people that you dont need to be a genius to make learning machines.\nAnd im super happy to see your reactions!",
  url='',  
  author='Rocko Visser',
  author_email='rockodagamer@gmail.com',
  license='MIT',
  classifiers=classifiers,
  keywords='AI, ML, machine learning, generation',
  packages=find_packages(),
  install_requires=['numpy']
)
