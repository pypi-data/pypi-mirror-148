######################################################################
### author = Rafael Zamora 
### copyright = Copyright 2020-2022, Next Project 
### date = 28/03/2022
### license = PSF
### version = 3.3.1 
### maintainer = Rafael Zamora 
### email = rafa.zamora.ram@gmail.com 
### status = Production
######################################################################

# Update 28/03/2022
VERSION = "3.3.1"

#System Packages
import os

#Local Packages
import src.read_config
import src.tools


def version():
    # Message(Info): Next Version
    src.tools.message_info("Next version: " + VERSION)

def version_all():
    
    # Next Packages Dierctory
    next_packages_dir = ""
    try:
        #Search NEXT_PACKAGES_DIR
        next_packages_dir = os.environ['NEXT_PACKAGES_DIR']
        
        # Message(Info): NEXT_PACKAGES_DIR in:
        src.tools.message_info("NEXT_PACKAGES_DIR in: " +  next_packages_dir)

    except:
        # Message(Error): Not Find NEXT_PACKAGES_DIR
        src.tools.message_error("It was not found ENV NEXT_PACKAGES_DIR in func --src.version_next.version_all()--")
        exit()

    # Get Subdirectories 
    list_next_packages = os.listdir(next_packages_dir)

    for next_pakage_dir in list_next_packages:

        # Read COnfig for DIrectory
        config_obj = src.read_config.read_config(next_packages_dir+ "/" + next_pakage_dir)

        # If exists src.config_t
        if config_obj != False:
            
            # Message(Info): Get Version of Proects
            src.tools.message_info(config_obj.name_project + " " + config_obj.version + "\n")
    