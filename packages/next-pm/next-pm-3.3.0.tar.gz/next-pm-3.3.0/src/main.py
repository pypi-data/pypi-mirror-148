######################################################################
### author = Rafael Zamora 
### copyright = Copyright 2020-2022, Next Project 
### date = 29/01/2022
### license = PSF
### version = 3.3.0 
### maintainer = Rafael Zamora 
### email = rafa.zamora.ram@gmail.com 
### status = Production
######################################################################

# Packages Dependencies
import click

#Local Packages
import src.info_next
import src.version_next
import src.create_next
import src.build_next
import src.run_next
import src.clean_next
import src.config_env
import src.config_get
import src.config_set
import src.config_add
import src.tools
import src.exce_next
import src.use_next

### Update 29/03/2022
### ✓ create                   Create a new Next project.
### ✓ build                    Build this project
### ✓ run                      Run your app
### ✓ clean                    Remove the binaries
### ✓ version                  List Next and plugins version.
### ✓ info                     Print Info verbose of Next
### ✓ add                      Add to property of current Next Project
### ✓ get                      Get to property of current Next Project
### ✓ set                      Set to property of current Next Project
### ✓ exce                     Excecute a command perzonalized

### × use                      Use a new library
### × remove                   Remove a library
### × install                  Install a Plugin
### × upgrade                  Upgrade a Plugin or Next
### × doctor                   Show information about the installed tooling.

@click.group()
def main():
    src.tools.load_env()
    pass

@main.command('info', short_help='view info the Next')
def info():
    src.info_next.info()

@main.command('version', short_help='view version the Next')
@click.option('--all',default=0, required=False, help='view version of all NextPackages installed <default=0>')
def version(all):
    # alone Next version
    if(all == 0):
        src.version_next.version()
    # all NextPackages
    elif(all == 1):
        src.version_next.version_all()
    # Error Not show any version
    else:
        exit()

@main.command('check_env', short_help='check env the NextPackages')
def check_env():
    src.config_env.check_env()

@main.command('create', short_help='Create a new project of Next', options_metavar='<name> <options>')
@click.argument('name', required=True, type=str, metavar='')
@click.option('--build_dir', required=False, type=str, help='Select Build Dir')
@click.option('--name_build', required=False, type=str, help='Select name of build')
@click.option('--build_system_exe', required=False, type=str, help='Select Build System executable')
@click.option('--c_compiler', required=False, type=str, help='Select C Compiler')
@click.option('--cxx_compiler', required=False, type=str, help='Select C++ Compiler')
@click.option('--build_system', required=False, type=str, help='Select Build System')
@click.option('--type_project', required=False, type=str, help='Select Type Project')
def create(name, build_dir, name_build, build_system_exe, c_compiler, cxx_compiler, build_system, type_project):
    src.create_next.create(name, build_dir, name_build, build_system_exe, c_compiler, cxx_compiler, build_system, type_project)

@main.command('build', short_help='Build a project of Next')
def build():
    src.build_next.build()

@main.command('run', short_help='Run a project of Next')
def run():
    src.run_next.run()

@main.command('clean', short_help='Clean a project of Next')
def clean():
    src.clean_next.clean()

@main.command('get', short_help='Get property of current Next Project')
@click.option('--property',default="name", required=True, help='Select property of current Next Project <default=name>')
def get(property):
    value_of_property = src.config_get.get(property)
    if isinstance(value_of_property, list):
        value_in_str = ''
        value_in_str += '['
        for x in value_of_property:
            value_in_str += x + ','
        len_value = len(value_in_str)
        value_in_str = value_in_str[:len_value-1]
        value_in_str += ']' 
    else:
        value_in_str = value_of_property
    
    print(property + ": " + value_in_str)

@main.command('set', short_help='Set property of current Next Project')
@click.option('--property',default="name", required=True, help='Select property of current Next Project <default=name>')
@click.option('--value',default="name", required=True, help='Select value of current Next Project <default=null>')
def set(property, value):
    src.config_set.set(property, value)


@main.command('add', short_help='Add to property of current Next Project')
@click.option('--property',default="name", required=True, help='Select property of current Next Project <default=name>')
@click.option('--value',default="name", required=True, help='Select value of current Next Project <default=null>')
def add(property, value):
    src.config_add.add(property, value)
    
@main.command('exce', short_help='Add to property of current Next Project')
@click.argument('command')
def exce(command):
    src.exce_next.exce(command)
    
@main.command('use', short_help='Add new library in current project')
@click.argument('library')
def use(library):
    src.use_next.use_path(library)

#if __name__ == "__main__":
#main()
