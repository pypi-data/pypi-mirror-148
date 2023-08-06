from setuptools import setup, find_packages

setup(name="magdych-mess-client",
      version="0.1.0",
      description="Messenger Client",
      author="Magdych Sergey",
      author_email="magdych@mail.ru",
      packages=find_packages(),
      install_requires=['PyQt5', 'sqlalchemy', 'pycryptodome', 'pycryptodomex']
      )
