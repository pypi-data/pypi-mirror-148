from setuptools import setup, find_packages


setup(
    name='mycolorlogger',
    version='0.6',
    license='MIT',
    author="raaj",
    author_email='advrter@gmail.com',
    packages=find_packages('src'),
    package_dir={'': 'src'},
    url='https://github.com/codingbeast/mylogger',
    keywords='logger',
    install_requires=[
          'colorlog==5.0.1',
      ],

)