######################################################################
### author = Rafael Zamora 
### copyright = Copyright 2020-2022, Next Project 
### date = 20/03/2022
### license = PSF
### version = 3.2.0 
### maintainer = Rafael Zamora 
### email = rafa.zamora.ram@gmail.com 
### status = Development
######################################################################

#System Packages
import os

#Local Packages
import next.read_config
import next.write_config
import next.tools

def add(property, value):
    """Adds a new property to the current project

    Args:
        property (str): name of new property
        value (str): value of new property

    Returns:
        value_of_property([str, null]): value of new property
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
        value_of_property = config_obj.add(property, value)

        #If it was added correctly
        if(value_of_property != "null"):
            
            #Write the new config
            write_config.write_property(config_obj, dir_project)
            
            # Message(Successful): Added property
            tools.message_successful('Added property ' + property + ': ' + value)
            
        else:
            # Message(Error): Could not add
            tools.message_error('Could not add ' + property + ': ' + value)

    #Value of new property ([str, null])
    return value_of_property