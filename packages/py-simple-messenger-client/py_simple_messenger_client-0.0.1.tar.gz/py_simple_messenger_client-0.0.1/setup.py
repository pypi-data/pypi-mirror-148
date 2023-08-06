from setuptools import setup, find_packages

setup(name="py_simple_messenger_client",
      version="0.0.1",
      description="Simple messenger client",
      author="Andrey Yablokov",
      author_email="andrewyablokov@yandex.ru",
      packages=find_packages(),
      install_requires=['PyQt5', 'sqlalchemy', 'pycryptodome', 'pycryptodomex'],
      )
