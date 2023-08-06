from setuptools import setup

setup(name='dbbkp',
      version='0.1.4',
      description='dbbkp Package',
      packages = ['dbbkp'],
      install_requires = ["numpy","pandas","matplotlib","utilum","sql_formatter"],
      zip_safe = False,
      )