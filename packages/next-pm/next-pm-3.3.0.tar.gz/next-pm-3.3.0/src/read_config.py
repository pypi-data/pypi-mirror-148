######################################################################
### author = Rafael Zamora 
### copyright = Copyright 2020-2022, Next Project 
### date = 28/03/2022
### license = PSF
### version = 3.3.0 
### maintainer = Rafael Zamora 
### email = rafa.zamora.ram@gmail.com 
### status = Production
######################################################################

#System Packages
import os

#Local Packages
import src.config_t
import src.tools

def _this_is_a_dir(dir):
    """Identify if this is Dir

    Args:
        dir (str): Direction of proyect

    Returns:
        bool: Flag
    """
    
    # Flag 
    done = False

    # Is a Directory
    if os.path.isdir(dir):
        done = True
        
        # Message(Successful): Is a directory
        src.tools.message_successful(dir + " Is a directory")
    else:
        
        # Message(Error): Not ss a directory
        src.tools.message_error(dir + " Not is a directory")
    
    return done

def _exists_config_file(dir):
    """Identify if it exists config.yaml

    Args:
        dir (str): Direction of project

    Returns:
        bool: Flag
    """
    
    # Flag
    done = False
    try:
        
        #Try open config.yaml
        config_file = open( dir + "/config.yaml", "r")
        config_file.close()
        
        # Message(Successful): Is a directory
        src.tools.message_successful("Exists config.yaml in :" + dir)
        
        done = True
    except:
        # Message(Error): Not is a directory
        src.tools.message_error("Not exists config.yaml in :" + dir)
    
    return done

def read_config(dir):
    """Read Config of Project

    Args:
        dir (str): Dir of Project

    Returns:
        [src.config_t, bool]: Data or Flag
    """
    
    # Identify if this is a Proyect of Next
    if _this_is_a_dir(dir) and _exists_config_file(dir):
        
        # Create src.config_t object
        config_obj = src.config_t.config_t(dir)
        
        # Message(Successful): Is a directory
        src.tools.message_successful(dir + " Is a project of Next")
                
        # Return src.config_t object
        return config_obj
    
    # Message(Error): Not is a project Next
    src.tools.message_error(dir + " Not is a project of Next")
    return False