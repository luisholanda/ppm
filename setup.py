from setuptools import setup

setup(name='ppm',
      version=0.1,
      description='Python Package Manager',
      url='https://gitlab.com/luisholanda/ppm.git',
      author='Luis Holanda',
      author_email='luiscmholanda@gmail.com',
      license='GNU',
      packages=['ppm'],
      install_requires=[
            'pip>=9.0.1',
      ],
      zip_safe=False)
