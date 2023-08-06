from setuptools import setup, find_packages


setup(
    name='drlab_minilib',
    version='0.1',
    license='MIT',
    author="Rafal Labedzki",
    author_email='rlabed@sgh.waw.pl',
    packages=find_packages('src'),
    package_dir={'': 'src'},
    install_requires=[
          'sklearn', 
          'pandas',
          'matplotlib'
      ],

)