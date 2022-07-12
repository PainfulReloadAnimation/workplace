# $language = "Python3"
# $interface = "1.0"

# Lab switches:
#	GLI-BF1-2
#	G-SGN-BF513-2


import os
import sys

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
import normdiagnew
import iplookup
import loginnew
from importlib import reload
import webbrowser

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
reload(normdiagnew)
reload(iplookup)
reload(loginnew)
# Now, pass the crt object to the imported module via this function
# so it can be used throughout the imported module code.
normdiagnew.Inject_crt_Object(crt)
iplookup.Inject_crt_Object(crt)
loginnew.Inject_crt_Object(crt)
# Inside our Main() function here, we'll be calling a function that
# is defined within the imported module: Test_crt_Object()
# This function displays a message, and returns a value. The returned
# value is then displayed in another message box.
# 
SCRIPT_TAB = crt.GetScriptTab()
SCRIPT_TAB.Screen.Synchronous = True


def main():
    crt.Screen.Synchronous = True

    # Check if login is required and login if so
    currentLine = crt.Screen.Get(crt.Screen.CurrentRow, 0, crt.Screen.CurrentRow, crt.Screen.CurrentColumn)
    if ("Username:" in currentLine) or ("Username: " in currentLine) or ("login:" in currentLine) or (
            "se's password: " in currentLine):
        loginnew.login()

        if crt.Screen.WaitForString("#", 1) != False and crt.Screen.WaitForString(">", 1) != False:
            crt.Dialog.MessageBox("Something went wrong dimwit")
    elif "@b3" in currentLine:
        loginnew.logger()
        if crt.Screen.WaitForString("#", 1) != False and crt.Screen.WaitForString(">", 1) != False:
            crt.Dialog.MessageBox("Something went wrong dimwit")
    # Choose which module to run.
    try:
        choice = crt.Dialog.Prompt("1: General Diagnosis\n2: Search For IP/MAC Address\n3: Help\n4: dBm Converter", "Choice Window")

        if choice != "1" and choice != "2" and choice != "3" and choice != "4":
            raise ValueError

    except ValueError:
        crt.Dialog.MessageBox("Not a valid number NERD")
    else:
        if choice == "1":
            normdiagnew.portchoice()
        elif choice == "2":
            iplookup.addresschoice()
        elif choice == "3":
            choice = crt.Dialog.Prompt("1: Commands\n2: Utility", "Choice Window")
            if choice != "1" and choice != "2":
                raise ValueError
            if choice == "1":
                choice = crt.Dialog.Prompt("1: Huawei\n2: DZS\n3: Ericsson", "Choice Window")
                if choice =="1":
                    url = "http://nrc.teliacompany.net/kommandon/hua.php"
                    webbrowser.open(url, new=2)
                if choice =="2":
                    url = "http://nrc.teliacompany.net/kommandon/dzs.php"
                    webbrowser.open(url, new=2)
                if choice == "3":
                    url = "http://nrc.teliacompany.net/kommandon/eri.php"
                    webbrowser.open(url, new=2)
        elif choice == "4":
            dBm = crt.Dialog.Prompt("Enter dBm value.", "Prompt Window")
            string = ((10 ** ((float(dBm) - 30) / 10)))/(0.001)
            crt.Dialog.MessageBox(str(string))
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
def SendExpect(send, expect):
    # Returns true if the text in 'send' was successfully sent and the
    # text in 'expect' was successfully found as a result.

    # If we're not connected, we can't possibly return true, or even
    # send/recv text
    if not SCRIPT_TAB.Session.Connected:
        return

    SCRIPT_TAB.Screen.Send(send + '\r')
    SCRIPT_TAB.Screen.WaitForString(expect)

    return True


# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
def CaptureOutputOfCommand(command, prompt):
    if not crt.Session.Connected:
        return "[ERROR: Not Connected.]"

    # First, send the command to the remote.
    SCRIPT_TAB.Screen.Send(command + '\r')

    # Second, wait for the carriage return to be echoed by the remote device.
    # This allows us to capture only the output of the command, not the line
    # on which the command was issued (which would include the prompt + cmd).
    # If you want to capture the command that was issued, simply comment out
    # the following line of code.
    SCRIPT_TAB.Screen.WaitForString('\r')

    # Now that the command has been sent, use Screen.ReadString to capture
    # all the data that is received up to the point at which the shell
    # prompt appears (the captured data does not include the shell prompt).
    return SCRIPT_TAB.Screen.ReadString(prompt)


main()
