from setuptools import setup, find_packages


setup(
    name='papflix',
    version='0.0.6',
    license='MIT',
    author="kpaparid",
    author_email='kpaparid@gmail.com',
    packages=find_packages('src'),
    package_dir={'': 'src'},
    url='https://github.com/pypa/sampleproject',
    keywords='example project',
    install_requires=[
          'scikit-learn',
      ],

)