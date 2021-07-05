'''
crt_Module.py
  Last Modified: 1 May, 2013
  
This example module is the companion to:

  ImaddressModuleWith_crt_Reference.py

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


def addresschoice():
    crt.Screen.Synchronous = True
    iptype = "NONE"
    address = crt.Dialog.Prompt("Enter IP/MAC address", "IP Lookup")

    if address == "":
        crt.Dialog.MessageBox("Please rerun the script with a valid address")
        return
    elif "." in address:
        iptype = "IP"
    elif "-" or ":" in address:
        iptype = "MAC"

    bf_type = crt.Screen.Get(crt.Screen.CurrentRow, 0, crt.Screen.CurrentRow, crt.Screen.CurrentColumn)
    if "<" in bf_type:
        huawei(address, iptype)
    elif "#" in bf_type:
        crt.Screen.Send("show version")
        crt.Screen.Send("\r")
        crt.Screen.WaitForString("Unexpected input:", 1)
        screenrow = crt.Screen.CurrentRow  # - 1
        bf_type_cisco_ericcson = crt.Screen.Get(crt.Screen.CurrentRow, 0, crt.Screen.CurrentRow,
                                                crt.Screen.CurrentColumn)
        if "Unexpected input:" in bf_type_cisco_ericcson:
            ericsson(address)
        else:
            cisco(address)
    elif " >" in bf_type:
        DZS(address)
    elif ">" in bf_type:
        SSAB_ZTE(address)


def huawei(address, iptype):
    # Ask for which address
    # address = crt.Dialog.Prompt("Enter address to diagnose", "BF-diagnose Huawei")

    node = crt.Screen.Get(crt.Screen.CurrentRow, 0, crt.Screen.CurrentRow, crt.Screen.CurrentColumn)

    if "<" in node:
        node = node.replace('<', '', 1)
    if ">" in node:
        node = node.replace('>', '', 1)

    data = "Node name: " + node + "\n"
    data += "Address: " + address + "\n"

    # Check Ip/Mac.
    crt.Screen.Send("display dhcp snooping user-bind all\r")


    # Write out the information found.
    if crt.Screen.WaitForString(address, 1):
        screenrow = crt.Screen.CurrentRow
        crt.Screen.WaitForString("DST", 1)
        port = crt.Screen.Get(screenrow, 56, screenrow, 56)
        vlan = crt.Screen.Get(screenrow, 34, screenrow, 36)
        data += iptype + " exists at port " + port + " with vlan " + vlan + "\n"
    else:
        data += "Can't find address specified\n"


    crt.Dialog.MessageBox(data)

    crt.Clipboard.Format = "CF_TEXT"
    crt.Clipboard.Text = data


def cisco(address):
    # Ask for which address
    # address = crt.Dialog.Prompt("Enter address to diagnose", "BF-diagnose Cisco")
    node = crt.Screen.Get(crt.Screen.CurrentRow, 0, crt.Screen.CurrentRow, crt.Screen.CurrentColumn)

    if "#" in node:
        node = node.replace('#', '', 1)

    data = "Node name: " + node + "\n"
    data += "address: fastEthernet 0/" + address + "\n"

    data_read = CaptureOutputOfCommand("show interfaces fastEthernet 0/" + address, "Last input")

    if "% Invalid input detected at '^' marker." in data_read:
        crt.Dialog.MessageBox("Please rerun the script with a valid address")
        return
    elif "connected" in data_read:
        data += "address is UP\n"
        address_status = True
    elif "notconnect" in data_read:
        data += "address is DOWN\n"
        address_status = False
    else:
        data += "address is err-disabled - try restarting the address\n"
        address_status = False

    if address_status == False:
        if "100BaseTX" in data_read:
            data += "Copper interface\n"
            crt.Screen.Send("test cable-diagnostics tdr interface fastEthernet 0/" + address)
            crt.Screen.Send("\r")
            data_read = CaptureOutputOfCommand("show cable-diagnostics tdr interface fastEthernet 0/" + address,
                                               "Pair C")

        else:
            data += "Fiber, go fuck yourself"
    elif address_status == True:
        data_read = CaptureOutputOfCommand("show ip dhcp snooping binding interface fastEthernet 0/" + address,
                                           "Total number of bindings:")
        screenrow = crt.Screen.CurrentRow - 2
        binding_row = crt.Screen.Get(screenrow, 1, screenrow, 25)
        if binding_row == "Total number of bindings: 0":
            data += "No IP-adresses assigned to devices on address"
    # else:
    #	data += data_read

    crt.Dialog.MessageBox(data)

    crt.Clipboard.Format = "CF_TEXT"
    crt.Clipboard.Text = data


def ericsson(address):
    crt.Screen.Send("\r")
    node = crt.Screen.Get(crt.Screen.CurrentRow, 0, crt.Screen.CurrentRow, crt.Screen.CurrentColumn)

    if "#" in node:
        node = node.replace('#', '', 1)

    data = "Node name: " + node + "\n"
    data += "address: " + address + "\n"

    data_read = CaptureOutputOfCommand("get ethernet_address " + address, "sp")
    crt.Screen.Send("\r")

    if "Bad range" in data_read:
        crt.Dialog.MessageBox("Please rerun the script with a valid address")
        return
    elif "Unexpected input:" in data_read:
        crt.Dialog.MessageBox("Please rerun the script with a valid address")
        return
    elif "up" in data_read:
        data += "address is UP\n"
        address_status = True
    elif "down" in data_read:
        data += "address is DOWN\n"
        address_status = False

    crt.Screen.WaitForString(node, 3)

    if address_status == True:
        data += "See IP info in session"
        data_read = CaptureOutputOfCommand("get connection vlan * ethernet_address " + address, "----MORE")
        # crt.Screen.Send("get connection vlan * ethernet_address " + address)
        crt.Screen.Send("\r")
        if (crt.Screen.WaitForString("----MORE: Press Enter to continue, Esc or Q to abort", 3)) == True:
            crt.Screen.Send("\r")

    crt.Dialog.MessageBox(data)

    crt.Clipboard.Format = "CF_TEXT"
    crt.Clipboard.Text = data


def DZS(address):
    node = crt.Screen.Get(crt.Screen.CurrentRow, 0, crt.Screen.CurrentRow, crt.Screen.CurrentColumn)

    if ">" in node:
        node = node.replace('>', '', 1)

    data = "Node name: " + node + "\n"
    data += "address: ethernet 0/" + address + "\n"

    data_read = CaptureOutputOfCommand("show interface ethernet 0/" + address, "address Mode is access")

    if "% Can't find interface" in data_read:
        crt.Dialog.MessageBox("Please rerun the script with a valid address")
        return
    elif "is down, line" in data_read:
        data += "address is down\n"
        address_status = False
    elif "is up, line" in data_read:
        data += "address is up\n"
        address_status = True

    data_read = CaptureOutputOfCommand("show ip dhcp snooping binding ethernet 0/" + address,
                                       "Total dhcp snoop binding entry")

    data += data_read

    crt.Dialog.MessageBox(data)

    crt.Clipboard.Format = "CF_TEXT"
    crt.Clipboard.Text = data


def SSAB_ZTE(address):
    node = crt.Screen.Get(crt.Screen.CurrentRow, 0, crt.Screen.CurrentRow, crt.Screen.CurrentColumn)

    if ">" in node:
        node = node.replace('>', '', 1)

    data = "Node name: " + node + "\n"
    data += "address: ethernet 0/" + address + "\n"

    crt.Dialog.MessageBox(data)


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
