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

#System Packages
import shutil
import os
import datetime
import platform

#Local Packages
import src.read_config
import src.tools

# String for add in cmake/vendor.cmake
vendor_basic = """
#__NAME_LIB_LOWER__ added __DATE__
include(__FILE_IMPORT_LIB__)

set( INCLUDE_LIBS
    ${INCLUDE_LIBS}
    ${__NAME_LIB_UPPER___INCLUDE_DIR}
)

set( LIBS
    ${LIBS}
    ${__NAME_LIB_UPPER__})
"""

def use_path(library_dir):
    """Add library to this project from full path

    Args:
        library_dir (str): full path of library
    """
    
    # Get current Directory
    this_dir = os.getcwd()
    
    #Get NEXT_DIR env
    next_dir = ""
    try:
        #Search NEXT_PACKAGES_DIR
        next_dir = os.environ['NEXT_DIR']
        
        # Message(Info): NEXT_DIR find in 
        src.tools.message_info('NEXT_DIR in: ' + next_dir)

    except:
        # Message(Error): Not Find NEXT_DIR
        src.tools.message_error('It was not found ENV NEXT_DIR')  
        exit()

    try:
        
        # Read config of proyect
        config_obj = src.read_config.read_config(this_dir)
        
        # Read config of library
        config_lib = src.read_config.read_config(library_dir)

        # If the configuration is not empty
        if config_obj != False and config_lib != False:
            
            try:
                
                # Get NEXT_DIR/assets/import_base.cmake
                import_base_file = next_dir + "/assets/import_base.cmake"
                
                #Get properties of library
                name_project_lib = config_lib.get('name_project')
                
                name_build_lib = config_lib.get('name_build')
                
                build_dir_lib = config_lib.get('build_dir')
                
                # Generate name of import cmake
                file_import_lib = 'cmake/' + name_project_lib + '.cmake'
                
                # Copy the import_base.cmake
                shutil.copyfile(import_base_file,file_import_lib)
                
            #### Verify exist binary
        
                # Try Generate Default name_build_lib_abs
                name_build_lib_abs = library_dir + '/' + build_dir_lib + '/' + name_build_lib
                
                if os.path.isfile(name_build_lib_abs):
                    
                    # Message(Info): Library binary file found
                    src.tools.message_info('Library binary file found: ' + name_build_lib_abs)
                else:
                    
                    # Message(Warning): Library binary file not found
                    src.tools.message_warning('Library binary not found')
                    
                    # Message(Info): Search file
                    src.tools.message_info('Want to search yes/no')
                    
                    res = input()
                    
                #### Search likely binaries
                    if res == 'yes':
                        # Message(Waiting): Search file
                        src.tools.message_waiting('Search')
                        # Verify that it exists name_build_lib
                        
                        likely_binaries_local = []
                        
                        likely_binaries_abs = []
                        
                        files_build_abs = src.tools.absoluteFilePaths(library_dir + '/' + build_dir_lib)
                        
                        files_build_local = os.listdir(library_dir + '/' + build_dir_lib)
                        
                        # Get likely files relative path
                        for file in files_build_local:
                            if file.find(name_build_lib) != -1:
                                likely_binaries_local.append(file)
                                
                        # Get likely files full path
                        for file_local in likely_binaries_local:
                            for file_abs in files_build_abs:
                                if file_abs.find(file_local) != -1:
                                    likely_binaries_abs.append(file_abs)
                        
                        # Message(Info): Mathches Found
                        src.tools.message_info('Matches found')
                        i = 1
                        for f in likely_binaries_abs:
                            print( str(i) + ') ' + f)
                            i = i + 1
                        
                        # Message(Info): Select the binary
                        src.tools.message_info('Select a Binary \'n\' to cancelr')
                        res = input()
                        
                        # Binary not selected
                        if res == 'n':
                            # Message(Warning): Select the binary
                            src.tools.message_warning('You will need to add the library binary manually.')
                            
                            name_build_lib_abs = ''
                        else:
                            # Adding the binary
                            name_build_lib_abs = likely_binaries_abs[int(res) - 1]
                        
                    else:
                        # Message(Warning): Select the binary
                        src.tools.message_warning('You will need to add the library binary manually.')
                        
                        # Clean the name_build_lib_abs
                        name_build_lib_abs = ''
                        
                # Configuration of file_import_lib
                src.tools.remplace_in_file(file_import_lib, '__NAME_PROJECT_UPPER_CASE__', name_project_lib.upper())
                
                src.tools.remplace_in_file(file_import_lib, '__DIR_LIB__', library_dir)
                
                src.tools.remplace_in_file(file_import_lib, '__FILE_BUILD_ABS__', name_build_lib_abs)

                # Remplace \ route for /
                system = platform.system()
                if system != 'Linux':
                    src.tools.remplace_in_file(file_import_lib, '\\', '/')
                
                
                # Write in cmake/vendor.cmake
                file_vendor = open(this_dir + '/cmake/vendor.cmake', 'a')
                
                file_vendor.write(vendor_basic)
                
                file_vendor.close()
                
                # Configuration of cmake/vendor.cmake
                src.tools.remplace_in_file(this_dir + '/cmake/vendor.cmake', '__NAME_LIB_UPPER__', name_project_lib.upper())
                
                src.tools.remplace_in_file(this_dir + '/cmake/vendor.cmake', '__NAME_LIB_LOWER__', name_project_lib.lower())

                src.tools.remplace_in_file(this_dir + '/cmake/vendor.cmake', '__FILE_IMPORT_LIB__', file_import_lib)
                
                src.tools.remplace_in_file(this_dir + '/cmake/vendor.cmake', '__DATE__', str(datetime.datetime.now()))     
                
                # Message(Successful): Library added
                src.tools.message_successful(library_dir + 'added in: ' + this_dir)
                
            except OSError as err:
                # Message(Error): OSError generate
                src.tools.message_error(str(err))
    except OSError as exc:
        
        # Message(Error): OSError generate
        src.tools.message_error(str(exc))
        
        # Exit to program
        exit()