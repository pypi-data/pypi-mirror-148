from setuptools import setup, find_packages


setup(
    name='fgaurat_hello_lib',
    version='0.1',
    license='MIT',
    author="Fred Gaurat",
    author_email='fgaurat@gmail.com',
    packages=find_packages('src'),
    package_dir={'': 'src'},
    url='https://github.com/fgaurat/hello_world_example_pypi',
    keywords='example project',
    install_requires=[
          'cowsay',
      ],

)