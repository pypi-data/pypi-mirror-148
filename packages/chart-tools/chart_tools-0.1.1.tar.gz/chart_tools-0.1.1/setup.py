import pathlib
from setuptools import setup, find_packages

HERE = pathlib.Path(__file__).parent

README = (HERE / "README.md").read_text()

setup(
    name='chart_tools',
    version='0.1.1',
    description="Powerful visualizations, and an easy to use, interactive api for exploring and loading datasets",
    long_description=README,
    long_description_content_type="text/markdown",
    url='https://github.com/ryayoung',
    license='MIT',
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3.9",
    ],
    author="Ryan Young",
    author_email='ryanyoung99@live.com',
    packages=find_packages('src'),
    package_dir={'': 'src'},
    keywords='seaborn correlation heatmap',
    install_requires=[
          'seaborn',
          'matplotlib',
          'pandas',
          'numpy',
          'requests',
    ],
    python_requires='>=3.9'


)
