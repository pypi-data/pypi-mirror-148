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
import os
import subprocess

#Local Packages
import src.read_config
import src.tools

def build():
    """Build project from current directory
    """
    
    try:
        
        # Current directory
        this_dir = os.getcwd()
        
        try:
            
            # Read config of proyect
            config_obj = src.read_config.read_config(this_dir)

            # If the configuration is not empty
            if config_obj != False:

                try:
                    # Try create build_dir
                    os.mkdir(config_obj.get("build_dir"))
                    
                    # Message(Successful): The build_dir directory was created
                    src.tools.message_successful(this_dir + '/' + config_obj.get("build_dir"))
                    
                except:
                    # Message(Waiting): The build_dir folder already exists
                    src.tools.message_warning("Warning " + this_dir + "/" + config_obj.get("build_dir") +  " folder already exists")
                
                # Entering the directory build_dir
                os.chdir(config_obj.get("build_dir"))
                
                # Message(Waiting): Build Proyect
                src.tools.message_waiting("Build Proyect")

                # Command to build the project of Cmake
                subprocess.run([
                    "cmake", this_dir + "/.", 
                    "-G" + config_obj.get("build_system"), 
                    "-DCMAKE_CXX_COMPILER=" +  config_obj.get("cxx_compiler"), 
                    "-DCMAKE_C_COMPILER=" +  config_obj.get("c_compiler"),
                    "-D" + config_obj.get("type_project") +"=on" ] + config_obj.get("cmake_flags"))

                # Command to build the project of build_system
                subprocess.run([config_obj.get("build_system_exe")] + config_obj.get("build_system_flags"))
            # The configuration is empty
            else:
                # Message(Warning): The configuration is empty
                src.tools.message_warning("The configuration is empty")

        except OSError as exc:
            
            # Message(Error): OSError generate
            src.tools.message_error(str(exc))
    except OSError as err:
        
        # Message(Error): OSError generate
        src.tools.message_error(str(err))
        
        # Exit to program
        exit()