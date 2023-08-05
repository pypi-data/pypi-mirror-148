######################################################################
### author = Rafael Zamora 
### copyright = Copyright 2020-2022, Next Project 
### date = 20/03/2022
### license = PSF
### version = 3.2.0 
### maintainer = Rafael Zamora 
### email = rafa.zamora.ram@gmail.com 
### status = Production
######################################################################

#System Packages
import os

#Local Packages
import next.read_config
import next.write_config
import next.tools

def set(property, value):
    """Set a property to the current project

    Args:
        property (str): name of property
        value (str): value of property

    Returns:
        value_of_property([str, null]): new value of property
    """

    # default value of property
    value_of_property = "null"

    # alone Next version
    if(property != ""):

        # View the dir of current project {name}
        dir_project = os.getcwd()

        #Read config of current project
        config_obj = read_config.read_config(dir_project)

        #Wrapper for properties
        value_of_property = config_obj.set(property, value)

        #If it was set correctly
        if(value_of_property != "null"):
            
            #Write the new config
            write_config.write_property(config_obj, dir_project)
            
            # Message(Successful): Set property
            tools.message_successful('Set property ' + property + ': ' + value)
        
        else:
            # Message(Error): Could not set
            tools.message_error('Could not set ' + property + ': ' + value)

    #Value of new property ([str, null])
    return value_of_property