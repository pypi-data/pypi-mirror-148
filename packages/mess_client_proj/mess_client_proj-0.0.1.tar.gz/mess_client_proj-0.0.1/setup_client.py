from setuptools import setup, find_packages

setup(name="mess_client_proj",
      version="0.0.1",
      description="mess_client_proj",
      author="Nick Korzhenevskiy",
      author_email="korg1000@yandex.ru",
      packages=find_packages(),
      install_requires=['PyQt5', 'sqlalchemy', 'pycryptodome', 'pycryptodomex']
      )
