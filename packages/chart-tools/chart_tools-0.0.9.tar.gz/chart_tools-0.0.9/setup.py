from setuptools import setup, find_packages


setup(
    name='chart_tools',
    version='0.0.9',
    license='MIT',
    author="Ryan Young",
    author_email='ryanyoung99@live.com',
    packages=find_packages('src'),
    package_dir={'': 'src'},
    url='https://github.com/ryayoung',
    keywords='seaborn correlation heatmap',
    install_requires=[
          'seaborn',
          'matplotlib',
          'pandas',
          'numpy',
          'requests',
      ],

)
