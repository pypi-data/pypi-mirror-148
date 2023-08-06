from setuptools import setup, find_packages

setup(name="Andy_mess_client",
      version="0.0.1",
      description="Messenger Client",
      author="Andrei Shorokhov",
      author_email="andr2409@bk.ru",
      packages=find_packages(),
      install_requires=['PyQt5', 'sqlalchemy', 'pycryptodome', 'pycryptodomex'],
      scripts=['client/client_run']
      )
