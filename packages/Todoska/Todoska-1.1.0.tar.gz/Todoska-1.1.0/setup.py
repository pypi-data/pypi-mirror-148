from setuptools import setup, find_packages
import setuptools

classifiers = [
  'Development Status :: 5 - Production/Stable',
  'Intended Audience :: Education',
  'Operating System :: Microsoft :: Windows :: Windows 10',
  'License :: OSI Approved :: MIT License',
  'Programming Language :: Python :: 3'
]
 
setup(
  name='Todoska',
  version='1.1.0',
  description='A Basic Todo Tracker in Cli',
  long_description='Testing the typer packages',
  url='https://github.com/Abbhiishek/Todoska',  
  author='Abhishek Kushwaha',
  author_email='abhishekkushwaha1479@gmail.com',
  license='MIT', 
  entry_points={
    'console_scripts': [
      'Todoska = todocli:__main__',

    ]
  },
  classifiers=classifiers,
  keywords=['Python' , 'cli' , 'Todo' ,'Todotracker' , 'todo-tracker' , 'todo-tracker-cli', 'Todoska'], 
  packages=find_packages(),
  python_requires='>=3.6',
  install_requires=['typer' , 'rich' ] 
)