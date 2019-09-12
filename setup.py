from setuptools import setup


setup(name='Bluetooth',
      version='1.0',
      description='Some learning with bluetooth',
      url='http://github.com/MaxMalinowski/learning-bluetooth',
      author='Max Malinowski',
      license='MIT',
      install_requires=[
          'Pybluez',
          'gattlib',
      ],
      zip_safe=False)
