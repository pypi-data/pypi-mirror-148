######################################################################
### author = Rafael Zamora 
### copyright = Copyright 2020-2022, Next Project 
### date = 12/03/2022
### license = PSF
### version = 3.2.0
### maintainer = Rafael Zamora 
### email = rafa.zamora.ram@gmail.com 
### status = Production
######################################################################


from setuptools import setup, find_packages

setup(
    name = 'next-pm',
    packages = ['next'],   
    include_package_data=True,    # muy importante para que se incluyan archivos sin extension .py
    version = '3.2.0',
    description = 'Next es un administrador de proyectos de C/C++, es diseñado como una solucion a la administracion que requieren este tipo de proyectos.)',
    author='Rafael Zamora',
    author_email="rafa.zamora.ram@gmail.com",
    license="PSF",
    url="https://github.com/reitmas32/Next/tree/v3.2.0.pipy",
    classifiers = ["Programming Language :: Python :: 3",\
        "License :: OSI Approved :: Python Software Foundation License",\
        "Development Status :: 5 - Production/Stable", "Intended Audience :: Developers", \
        "Operating System :: OS Independent", \
        "Topic :: Software Development :: Build Tools"],
    keywords=['C/C++', 'package', 'libraries', 'developer', 'manager',
              'dependency', 'tool', 'c', 'c++', 'cpp'],
    entry_points={
        'console_scripts': [
            'next=next.next:main'
        ],
    },
    )