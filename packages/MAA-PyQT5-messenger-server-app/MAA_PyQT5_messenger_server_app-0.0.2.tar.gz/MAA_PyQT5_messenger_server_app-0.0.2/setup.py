from setuptools import setup, find_packages

setup(name="MAA_PyQT5_messenger_server_app",
      version="0.0.2",
      description="Server part of application MAA_PyQT5_messenger",
      author="Magomed Magomedov",
      author_email="mag.mag@yandex.ru",
      packages=find_packages(),
      install_requires=['PyQt5', 'sqlalchemy', 'pycryptodome', 'pycryptodomex'],
      scripts=['server/server_run']
      )
