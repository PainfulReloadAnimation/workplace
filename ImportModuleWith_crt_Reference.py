'''
ImportModuleWith_crt_Reference.py
  Last Modified: 10 Oct, 2017
    - Included 'sys.dont_write_bytecode' and 'reload(crt_module)' directives
      to assist forum user "Metallicat" and others struggling with how a
      python interpreter works with imported modules.
      (see https://forums.vandyke.com/showthread.php?t=12852)
      
  Last Modified: 01 May, 2013
    - Original version
    
DESCRIPTION:
    This example illustrates how to import a custom module that uses the crt
    object. 
    
    A good writeup on this process can be found in VDS Scripting forums:
      https://forums.vandyke.com/showpost.php?p=45424&postcount=14
      
    This example script is based on information posted by saraza in the
    following forum thread:
      http://forums.vandyke.com/showthread.php?t=10734

    This script requires the companion module called crt_Module.py.  Here is
    the code of the companion script if you don't have it:
    
-------------------------------------------------------------------------------
    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    def Inject_crt_Object(obj_crt_API):
        # Make the crt variable global for use in multiple functions in the
        # module that might need access to the crt object.
        global crt
        # Associate the crt variable with the crt object passed in from the
        # main script.
        crt = obj_crt_API
        return

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    def Test_crt_Object():
        # Test using the crt object.
        crt.Dialog.MessageBox("I'm a function in a python module!")
        return "It was the best of times, it was the worst of times"

-------------------------------------------------------------------------------

'''

import sys, os

# NOTE: A python interpreter will automatically create a .pyc file for
#       any custom module that you import. These .pyc files might cause
#       some individuals grief, as now they have confusion over .py and
#       .pyc files of the same basename hanging around inside their script
#       source folders.
#       
#       Use 'sys.dont_write_bytecode = True', to PREVENT python from
#       automatically creating these .PYC files:
sys.dont_write_bytecode = True

# sys.path is a variable that tells a script where to look for modules when
# importing them.  Here is an example of how to add a path you want to use if
# you don't want to use a pre-defined path.
# First, get the path to the script that is running, assuming the module to
# be imported is in that same location:
strScriptPath = os.path.dirname(__file__)

# Next, inject the path to the script into sys.path, which is what python
# will refer to when looking for modules to be import'd:
if not strScriptPath in sys.path:
    # Inject the path of the running script if it is not in sys.path
    sys.path.insert(0, strScriptPath)

# Now, import our custom module.
import crt_Module
# NOTE: A python interpreter will cache a module in memory even if
#       the sys.dont_write_bytecode directive is set to True. In
#       SecureCRT, the python interpreter remains in place with its
#       cache of imported modules as long as SecureCRT remains running.
#       This behavior may cause some individuals grief, as they expect
#       changes they make to the source code of the module file to be
#       immediately reflected in the script file that imports the module
#       code.
#       In order to force the python interpreter to always load a fresh
#       copy of the module source, use the 'reload(module_name)' directive
#       right after your import statement for that module. For example:
reload(crt_Module)

# Now, pass the crt object to the imported module via this function
# so it can be used throughout the imported module code.
crt_Module.Inject_crt_Object(crt)

# Inside our Main() function here, we'll be calling a function that
# is defined within the imported module: Test_crt_Object()
# This function displays a message, and returns a value. The returned
# value is then displayed in another message box.
# 
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~    
def Main():
    # Show that we can use the crt object that was passed into the module.
    strMessage = crt_Module.Test_crt_Object()
    
    # Show that we can still use the crt object in the main script.
    crt.Dialog.MessageBox(strMessage)
    
    return

Main()