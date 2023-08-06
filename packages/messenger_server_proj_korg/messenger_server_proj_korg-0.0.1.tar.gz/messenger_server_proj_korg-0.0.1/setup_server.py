from setuptools import setup, find_packages

setup(name="messenger_server_proj_korg",
      version="0.0.1",
      description="messenger_server_proj_korg",
      author="Nick Korzhenevskiy",
      author_email="korg1000@yandex.ru",
      packages=find_packages(),
      install_requires=['PyQt5', 'sqlalchemy', 'pycryptodome', 'pycryptodomex']
      )
