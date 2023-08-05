# Next

Next es un **administrador** de proyectos de **C/C++**, es diseñado como una solucion a la administracion que requieren este tipo de proyectos.

#### Requisitos
- [Curl](https://curl.se/)
- [Git](https://git-scm.com/)
- Un compilador de C++, recomendado [gcc](https://gcc.gnu.org/) o [clang](https://clang.llvm.org/)
- [Make](https://www.gnu.org/software/make/)
- [CMake](https://cmake.org/)

#### Instalación

- Linux
    ```
    curl -s https://raw.githubusercontent.com/KEGEStudios/Next/master/next-install.sh | bash -s
    ```
    - Añade ```$HOME/opt/Next/build``` a la variable ```$PATH```
- Windows
    - Clona este repositorio
    - Compila con cmake
    - Añade al PATH el ejecutable de next

#### Comandos

- **next create < nombre >** *Crea un nuevo proyecto con el nombre selecionado*
- **next build** *Compila el proyecto*
- **next run** *Ejecuta y compila si es e caso el peroyecto*
- **next --help** o **next -h** Muestra una guia de ayuda para el uso de **Next**
- **next --version** o **next -v** Muestra la version de next que se tiene instalado

#### Contribuidores

**Next** es prencipalmente apollado por el equipo de desarrollo del **Game Engine MOON** creado por **EGE Studios** ademas este esde codigo abierto por lo que cualquier persona que desee puede aportar a el.

#### Futuras verisiones

La version actual de Next es la v3.0.0 pero el desarrollo de Next esta en constante evolucion y se planea tener para las peroximas versiones:
- **next upgrade** Actualización sencilla de **Next**
- **next test** Intregracion de **Next** y Unit Testing
- **next doctor** Una forma facil de visualizar el estado de los compiladores de C/C++
- **next import** Conectar de forma sencilla librerias de C/C++ desde un servidor de unico de **Next** 

