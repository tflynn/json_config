from setuptools import setup, find_packages

setup(name='json_config',
      version='0.1',
      description='',
      url='https://github.com/tflynn/json_config.git',
      author='Tracy Flynn',
      author_email='tracysflynn@gmail.com',
      license='MIT',
      packages=find_packages(exclude=["*.tests", "*.tests.*", "tests.*", "tests"]),
      install_requires=[
          "standard_logger>=0.4",
          "pyxutils>=0.1"],
      test_suite='nose.collector',
      tests_require=['nose'],
      zip_safe=False)
