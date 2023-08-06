from setuptools import setup, find_packages

setup(name="Andy_mess_server",
      version="0.0.1",
      description="Messenger Server",
      author="Andrei Shorokhov",
      author_email="andr2409@bk.ru",
      packages=find_packages(),
      install_requires=['PyQt5', 'sqlalchemy', 'pycryptodome', 'pycryptodomex'],
      scripts=['server/server_run']
      )