from setuptools import setup


with open("README.md", "r") as file:
    long_description = file.read()

setup(name='r2c-isg',
      version='1.0.0',
      description='Return2Corp input set generator.',
      long_description=long_description,
      long_description_content_type="text/markdown",
      url='https://github.com/returntocorp/inputset-generator',
      author='Ben Fulton',
      author_email='fulton.benjamin@gmail.com',
      packages=['inputset-generator'],
      entry_points={
          'console_scripts': ['r2c-isg=inputset-generator.cli:cli'],
      },
      python_requires='>=3.6',
      zip_safe=False)
