from setuptools import setup, find_packages

setup(name="small_py_mess_server",
      version="0.5.1",
      description="mess_server",
      author="Tankred",
      author_email="brother.tankred@gmail.com",
      packages=find_packages(),
      install_requires=['PyQt5', 'sqlalchemy', 'pycryptodome', 'pycryptodomex']
      )
