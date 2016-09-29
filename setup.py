from setuptools import setup

setup(name='FlaskApp',
      version='1.0',
      description='Addressbook API',
      author='Max Atkinson',
      author_email='itsmaxatk@gmail.com',
      url='http://www.python.org/sigs/distutils-sig/',
     install_requires=['Flask>=0.10.1', 'Flask-SQLAlchemy==0.16', 'Flask-WTF'],
     )
