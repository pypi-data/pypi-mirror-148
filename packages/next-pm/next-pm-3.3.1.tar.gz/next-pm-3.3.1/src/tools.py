######################################################################
### author = Rafael Zamora 
### copyright = Copyright 2020-2022, Next Project 
### date = 12/03/2022
### license = PSF
### version = 3.3.1 
### maintainer = Rafael Zamora 
### email = rafa.zamora.ram@gmail.com 
### status = Production
######################################################################

# Packages Systems
import os
import platform

# Packages Dependencies
import ruamel.yaml

def remplace_in_file(file_location, old_text, new_text):
    try:
        #input file
        fin = open(file_location, "rt")

        old_data = fin.readlines()

        new_data = ""

        #for each line in the input file
        for line in old_data:
            #read replace the string and write to output file
            new_data += line.replace(old_text, new_text)
        #close input and output files
        fin.close()

        #output file to write the result to
        fout = open(file_location, "wt")

        #Write new data
        fout.write(new_data)

        #Close output file
        fout.close()
    except BaseException as err:
        print("Not remplace " + old_text + " in " + file_location)
        print(f"Unexpected {err=}, {type(err)=}")
        
def load_env():
    """load the environment variables in the current execution
    """
    try:
        env_yaml = ''
        
        file = ''
        
        _data = {}
        
        #Get Home Dir
        system = platform.system()
        
        if system == 'Linux':
            print('Linux System')
            home_dir = os.environ['HOME']
        else:
            print('Windows System')
            home_dir = os.environ['LOCALAPPDATA']
        
        next_env_file_dir = home_dir + '/.next/env.yaml'
        
        env_yaml = ruamel.yaml.YAML()
        
        env_yaml.preserve_quotes = True

        #Read the file
        file = open( next_env_file_dir, "r")

        #Safe the data
        _data = env_yaml.load(file)
        
        #Load the environment variables in the current execution
        for x in _data:
            print(x + '= ' + _data[x])
            os.environ[x] = _data[x]
        
    except:
        
        print("Error at Load Env")
        
from colorama  import Fore
from colorama import Style
from colorama import Back
from colorama import init

# For colorama in Windows load ANSI
system = platform.system()
if system != 'Linux':
    init(convert = True)

def message_error(str):
    print(f'{Fore.RED}{Style.BRIGHT} <<ERROR>> {Style.RESET_ALL}' + str)
    
def message_warning(str):
    print(f'{Fore.YELLOW}{Style.BRIGHT} <<WARNING>> {Style.RESET_ALL}' + str)
    
def message_successful(str):
    print(f'{Fore.LIGHTGREEN_EX}{Style.BRIGHT} <<SUCCESSFUL>> {Style.RESET_ALL}' + str)
    
def message_info(str):
    print(f'{Fore.WHITE}{Style.BRIGHT} <<INFO>> {Style.RESET_ALL}' + str)
    
def message_waiting(str):
    print(f'{Fore.BLUE}{Style.BRIGHT} <<WAITING...>> {Style.RESET_ALL}' + str)
    
def absoluteFilePaths(directory):
    for dirpath,_,filenames in os.walk(directory):
        for f in filenames:
            yield os.path.abspath(os.path.join(dirpath, f))