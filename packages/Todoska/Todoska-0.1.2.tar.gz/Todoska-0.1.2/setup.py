from setuptools import setup, find_packages
 
classifiers = [
  'Development Status :: 5 - Production/Stable',
  'Intended Audience :: Education',
  'Operating System :: Microsoft :: Windows :: Windows 10',
  'License :: OSI Approved :: MIT License',
  'Programming Language :: Python :: 3'
]
 
setup(
  name='Todoska',
  version='0.1.02',
  description='A Basic Todo Tracker in Cli',
  long_description=open('README.txt').read() + '\n\n' + open('CHANGELOG.txt').read(),
  url='https://github.com/Abbhiishek/Todoska',  
  author='Abhishek Kushwaha',
  author_email='abhishekkushwaha1479@gmail.com',
  license='MIT', 
  classifiers=classifiers,
  keywords='Python , cli , Todo ,Todotracker , todo-tracker', 
  packages=find_packages(),
  install_requires=['typer' , 'rich' , 'pysqlite3'] 
)