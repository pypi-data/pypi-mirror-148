from setuptools import setup, find_packages

setup(name="fine_messanger_server",
      version="0.0.1",
      description="server",
      author="Vyacheslav",
      author_email="slavkin.131@gmail.com",
      packages=find_packages(),
      install_requires=['PyQt5', 'sqlalchemy', 'pycryptodome', 'pycryptodomex']
      )
