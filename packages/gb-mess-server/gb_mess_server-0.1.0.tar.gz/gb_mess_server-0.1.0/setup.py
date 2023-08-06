from setuptools import setup, find_packages

setup(name="gb_mess_server",
      version="0.1.0",
      description="Messenger for Server",
      author="Nikita Savchenko",
      author_email="nikita.savchenko.developer@gmail.com",
      packages=find_packages(),
      install_requires=['PyQt5', 'sqlalchemy', 'pycryptodome', 'pycryptodomex'],
      scripts=['server/server_run']
      )
