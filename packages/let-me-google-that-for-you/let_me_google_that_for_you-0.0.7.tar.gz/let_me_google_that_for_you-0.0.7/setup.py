from setuptools import setup, find_packages
 
classifiers = [
  'Development Status :: 5 - Production/Stable',
  'Intended Audience :: Education',
  'Operating System :: Microsoft :: Windows :: Windows 10',
  'License :: OSI Approved :: MIT License',
  'Programming Language :: Python :: 3'
]
 
setup(
  name='let_me_google_that_for_you',
  version='0.0.7',
  description='A simple Python module to let you google that for you.',
  url='',  
  author='Me',
  author_email='opkoskos450@gmail.com',
  license='MIT', 
  classifiers=classifiers,
  keywords='let_me_google_that', 
  packages=find_packages(),
  install_requires=[''] 
)