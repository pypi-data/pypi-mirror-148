from setuptools import setup
from setuptools import find_packages

setup(
    name='Annoroad_OMIC_vis',
    version='1.0.1',
    description='Hi-C OMIC display tools',
    author='Zhao Yue',
    author_email='zhao_yue000@163.com',
    packages=find_packages(exclude=('Annoroad_OMIC_viz.testing*')),
      entry_points={
      'console_scripts':['Annoroad_vis=src.Annoroad_OMIC_viz.example.main:main',],
      },
)
