######################################################################
### author = Rafael Zamora 
### copyright = Copyright 2020-2022, Next Project 
### date = 12/03/2022
### license = PSF
### version = 3.3.0 
### maintainer = Rafael Zamora 
### email = rafa.zamora.ram@gmail.com 
### status = Production
######################################################################

#System Packages
import shutil
import os

#Local Packages
import src.read_config
import src.tools

def clean():
    """Clean Build of current Project
    """
    
    # Get current Directory
    this_dir = os.getcwd()
    try:
        
        # Read config of proyect
        config_obj = src.read_config.read_config(this_dir)

        # If the configuration is not empty
        if config_obj != False:
            
            try:
                # Remove the directory "build_dir"
                shutil.rmtree(config_obj.get("build_dir"))
                
                # Message(Successful): The build_dir delete
                src.tools.message_successful('Clean ' + this_dir + '/' + config_obj.get("build_dir"))
            except OSError as err:
                # Message(Error): OSError generate
                src.tools.message_error(str(err))
    except OSError as exc:
        
        # Message(Error): OSError generate
        src.tools.message_error(str(exc))
        
        # Exit to program
        exit()