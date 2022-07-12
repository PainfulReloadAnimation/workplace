'''
crt_Module.py
  Last Modified: 1 May, 2013
  
This example module is the companion to:

  ImportModuleWith_crt_Reference.py

This example module is based on information posted by saraza in the following
forum thread:

  http://forums.vandyke.com/showthread.php?t=10734

'''


# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
def Inject_crt_Object(obj_crt_API):
    # Make the crt variable global for use in multiple functions in the
    # module that might need access to the crt object.
    global crt
    global SCRIPT_TAB
    # Associate the crt variable with the crt object passed in from the
    # Main script.
    crt = obj_crt_API
    SCRIPT_TAB = crt.GetScriptTab()
    SCRIPT_TAB.Screen.Synchronous = True
    return


# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

def isInt(num):
    try:
        int(num)
        return True
    except ValueError:
        return False

def portchoice():
    crt.Screen.Synchronous = True

    port = crt.Dialog.Prompt("Enter a uplink port to diagnose", "bfDiag")

    if isInt(port) == False:
        crt.Dialog.MessageBox("Please rerun the script with a valid port")
        return
    elif isInt(port) == True:
        bfType = ""
        bfType = crt.Screen.Get(crt.Screen.CurrentRow, 0, crt.Screen.CurrentRow, crt.Screen.CurrentColumn)
        ##Valid port
        if "<" in bfType:
            # crt.Dialog.MessageBox("Huawei")
            huaweiDiag(port)
        else:
            crt.Screen.Send("show version")
            crt.Screen.Send("\r")
            crt.Screen.WaitForString("NOS version", 1)
            screenrow = crt.Screen.CurrentRow
            bfType = crt.Screen.Get(crt.Screen.CurrentRow - 2, 0, crt.Screen.CurrentRow - 2, crt.Screen.CurrentColumn)
            if "Configur" in bfType:
                # crt.Dialog.MessageBox("Cisco")
                ciscoDiag(port)
            elif "#s" in bfType:
                # crt.Dialog.MessageBox("Ericsson")
                ericssonDiag(port)
            else:
                # crt.Dialog.MessageBox("DZS")
                dzsDiag(port)


def huawei(port):
    # Ask for which port
    # port = crt.Dialog.Prompt("Enter port to diagnose", "BF-diagnose Huawei")

    node = crt.Screen.Get(crt.Screen.CurrentRow, 0, crt.Screen.CurrentRow, crt.Screen.CurrentColumn)

    if "<" in node:
        node = node.replace('<', '', 1)
    if ">" in node:
        node = node.replace('>', '', 1)

    data = "Node name: " + node + "\n"
    data += "Port: GigabitEthernet 0/0/" + port + "\n"
    # Check link and type of connection
    crt.Screen.Send("display interface GigabitEthernet 0/0/" + port)
    data_read = CaptureOutputOfCommand("\r", "Speed :")

    crt.Screen.Send("\r ")

    if "current state : UP" in data_read:
        data += "Port is UP\n"
        port_status = True
    else:
        data += "Port is DOWN\n"
        port_status = False

    if port_status == False:
        if "COMMON FIBER" in data_read:
            data += "COMMON FIBER\r"

            # Capture Rx and Tx
            crt.Screen.Send("display transceiver diagnosis interface GigabitEthernet 0/0/" + port)
            crt.Screen.Send("\r")

            # get Tx
            crt.Screen.WaitForString("RxPower(dBm)", 1)
            screenrow = crt.Screen.CurrentRow - 1
            Tx = crt.Screen.Get(screenrow, 1, screenrow, 25)
            # Put Tx in data
            data += Tx + "\n"

            # get Rx
            crt.Screen.WaitForString("Current(mA)", 1)
            screenrow = crt.Screen.CurrentRow - 1
            Rx = crt.Screen.Get(screenrow, 1, screenrow, 25)
            # Put Rx in data
            data += Rx

        elif "COMBO AUTO" in data_read:
            data += "COMBO AUTO\r"

            # Capture Rx and Tx
            crt.Screen.Send("display transceiver diagnosis interface GigabitEthernet 0/0/" + port)
            crt.Screen.Send("\r")

            # get Tx
            crt.Screen.WaitForString("RxPower(dBm)", 1)
            screenrow = crt.Screen.CurrentRow - 1
            Tx = crt.Screen.Get(screenrow, 1, screenrow, 25)
            # Put Tx in data
            data += Tx + "\n"

            # get Rx
            crt.Screen.WaitForString("Current(mA)", 1)
            screenrow = crt.Screen.CurrentRow - 1
            Rx = crt.Screen.Get(screenrow, 1, screenrow, 25)
            # Put Rx in data
            data += Rx

        elif "COMMON COPPER" in data_read:
            data += "COMMON COPPER\r"
            crt.Screen.Send("system-view")
            crt.Screen.Send("\r")
            crt.Screen.WaitForString("Enter system view, return user view with Ctrl+Z.", 1)
            crt.Screen.Send("interface GigabitEthernet 0/0/" + port)
            crt.Screen.Send("\r")
            crt.Screen.Send("vir")
            crt.Screen.Send("\r")
            crt.Screen.WaitForString("Warning: The command will stop service for a while. Continue? [Y/N]:", 1)
            crt.Screen.Send("y")

            data += CaptureOutputOfCommand("\r", "Info: The test result is only for reference.")
            crt.Screen.Send("q")
            crt.Screen.Send("\r")
            crt.Screen.Send("q")
            crt.Screen.Send("\r")

    # If link is up, check all other good stuff
    # data_read = None
    elif port_status == True:

        # Fails at G-SGN-BF513-2 port 5, needs further investigation
        crt.Screen.Send("display dhcp snooping user-bind interface GigabitEthernet 0/0/" + port)
        data_read_2 = CaptureOutputOfCommand("\r", "Total count")
        if "Info: The number of dhcp snooping bind-table is zero." in data_read_2:
            data += "No IP-adresses assigned to devices on port"

    crt.Dialog.MessageBox(data)

    crt.Clipboard.Format = "CF_TEXT"
    crt.Clipboard.Text = data


def huaweiDiag(port):
    crt.Screen.Send("display interface GigabitEthernet 0/0/" + port)
    sessionData = CaptureOutputOfCommand("\r", "Speed :")
    # send a blankspace instead of "q", fixes a glitch
    crt.Screen.Send(" ")

    if "current state : UP" in sessionData:
        linkStatus = True
    else:
        linkStatus = False

    if linkStatus == False:
        if ("COMMON FIBER" or "COMBOT AUTO") in sessionData:
            crt.Screen.Send("display transceiver diagnosis interface GigabitEthernet 0/0/" + port)
            crt.Screen.Send("\r")
        elif "COMMON COPPER" in sessionData:
            crt.Screen.Send("system-view")
            crt.Screen.Send("\r")
            crt.Screen.WaitForString("Enter system view, return user view with Ctrl+Z.", 1)
            crt.Screen.Send("interface GigabitEthernet 0/0/" + port + "\r")
            crt.Screen.Send("vir\r")
            crt.Screen.WaitForString("Warning: The command will stop service for a while. Continue? [Y/N]:", 1)
            crt.Screen.Send("y")
            crt.Screen.Send("q\r")
            crt.Screen.Send("q\r")
            crt.Screen.Send("q\r")
    elif linkStatus == True:
        crt.Screen.Send("display dhcp snooping user-bind interface GigabitEthernet 0/0/" + port)
        crt.Screen.Send("\r")
        crt.Screen.Send("display mac-address GigabitEthernet 0/0/" + port + "\r")
        crt.Screen.Send("\r")
        if ("COMMON FIBER" or "COMBOT AUTO") in sessionData:
            crt.Screen.Send("display transceiver diagnosis interface GigabitEthernet 0/0/" + port + "\r")


def dzsDiag(port):
    crt.Screen.Send("enable")
    crt.Screen.Send("\r")
    crt.Screen.Send("show interface ethernet 0/" + port)
    sessionData = CaptureOutputOfCommand("\r", "Transmitted Packets")

    if "is up," in sessionData:
        linkStatus = True
    else:
        linkStatus = False

    if linkStatus == False:
        crt.Screen.Send("show interface module-info ethernet 0/" + port + "\r")
        crt.Screen.WaitForString("Uninstalled", 1)
        screenrow = crt.Screen.CurrentRow
        sfp = crt.Screen.Get(crt.Screen.CurrentRow, 0, crt.Screen.CurrentRow, crt.Screen.CurrentColumn)
        if "Uninstalled" in sfp:
            crt.Screen.Send("show interface cable-diagnostic interface ethernet 0/" + port + "\r")
            crt.Screen.Send("y\r")
    elif linkStatus == True:
        crt.Screen.Send("show ip dhcp snooping binding ethernet 0/" + port + "\r")
        crt.Screen.Send("show mac address-table interface ethernet 0/" + port + "\r")
        crt.Screen.Send("show interface module-info ethernet 0/" + port + "\r")


def ciscoDiag(port):
    sessionData = CaptureOutputOfCommand("show interfaces fastEthernet 0/" + port, "Last input")

    if "connected" in sessionData:
        linkStatus = True
    elif "notconnect" in sessionData:
        linkStatus = False
    elif "err-disabled":
        linkStatus = False

    if linkStatus == False:
        if "100BaseTX" in sessionData:
            sessionData = CaptureOutputOfCommand("test cable-diagnostics tdr interface fastEthernet 0/" + port,
                                                 "Use 'show cable-diagnostics tdr' to read the TDR results.")
            # time.wait(2)
            crt.Screen.Send("show cable-diagnostics tdr interface fastEthernet 0/" + port + "\r")
    elif linkStatus == True:
        crt.Screen.Send("show ip dhcp snooping binding interface fastEthernet 0/" + port + "\r")
        crt.Screen.Send("show mac address-table interface fastEthernet 0/" + port + "\r")


def ericssonDiag(port):
    crt.Screen.Send("\r")
    node = crt.Screen.Get(crt.Screen.CurrentRow, 0, crt.Screen.CurrentRow, crt.Screen.CurrentColumn)

    if "#" in node:
        node = node.replace('#', '', 1)

    sessionData = CaptureOutputOfCommand("get ethernet_port " + port, "sp")
    crt.Screen.Send("\r")

    if "up" in sessionData:
        linkStatus = True
    elif "down" in sessionData:
        linkStatus = False

    crt.Screen.WaitForString(node, 3)

    if linkStatus == True:
        crt.Screen.Send("get connection vlan * ethernet_port " + port + "\r")
        # rt.Screen.Send("\r")
        if (crt.Screen.WaitForString("----MORE: Press Enter to continue, Esc or Q to abort", 5)) == True:
            crt.Screen.Send("\r")


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
