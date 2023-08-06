from setuptools import setup, find_packages

setup(name="MAA_PyQT5_messenger_client_app",
      version="0.0.1",
      description="Client part of application MAA_PyQT5_messenger",
      author="Magomed Magomedov",
      author_email="mag.mag@yandex.ru",
      packages=find_packages(),
      install_requires=['PyQt5', 'sqlalchemy', 'pycryptodome', 'pycryptodomex']
      )
