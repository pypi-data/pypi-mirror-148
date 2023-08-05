from setuptools import setup, find_packages


setup(
    name='cyera',
    version='0.1',
    license='MIT',
    author="Cyera",
    author_email='ellali456@gmail.com',
    packages=find_packages('src'),
    package_dir={'': 'src'},
    keywords='cyera',
    install_requires=[
          'scikit-learn',
      ],

)
