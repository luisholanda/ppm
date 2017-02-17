from setuptools import setup, find_packages

setup(
    name='ppm',
    version=0.1,
    description='The Python Package Manager that make your life easier.',
    classifiers=[
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Topic :: Software Development :: Build Tools",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
    ],
    keywords='easy_install distutils setuptools',
    url='https://gitlab.com/luisholanda/ppm.git',
    author='Luis Holanda',
    author_email='luiscmholanda@gmail.com',
    license='MIT',
    packages=find_packages(exclude=['spec']),
    install_requires=[
        'pip>=9.0.1',
    ],
    zip_safe=False,
    entry_points={
        'console_scripts': [
            'ppm = ppm:main'
        ]
    }
)
