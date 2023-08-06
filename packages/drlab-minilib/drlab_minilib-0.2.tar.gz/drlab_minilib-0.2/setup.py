from setuptools import setup, find_packages


setup(
    name='drlab_minilib',
    version='0.2',
    license='MIT',
    author="Rafal Labedzki",
    author_email='rlabed@sgh.waw.pl',
    packages=find_packages(),
    # package_dir={'drlab_minilib'},
    install_requires=[
          'sklearn', 
          'pandas',
          'matplotlib'
      ],

)