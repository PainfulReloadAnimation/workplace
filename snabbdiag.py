# $language = "Python3"
# $interface = "1.0"

# Lab switches:
#	GLI-BF1-2
#	G-SGN-BF513-2


# Using GetScriptTab() will make this script 'tab safe' in that all of the
# script's functionality will be carried out on the correct tab. From here
# on out we'll use the SCRIPT_TAB object instead of the crt object.
SCRIPT_TAB = crt.GetScriptTab()
SCRIPT_TAB.Screen.Synchronous = True

def main():
	
	crt.Screen.Synchronous = True
	
	port = crt.Dialog.Prompt("Enter port to diagnose", "BF-diagnose")
	if port == "":
		crt.Dialog.MessageBox("Please rerun the script with a valid port")
		return
	#elif isinstance(port, int) == False:
	#	crt.Dialog.MessageBox("Please rerun the script with a valid port")
	#	return
	else:
		bf_type = crt.Screen.Get(crt.Screen.CurrentRow, 0, crt.Screen.CurrentRow, crt.Screen.CurrentColumn)
		#if bf_type.isupper() == False:
		#	ericsson(port)
		#else:
		if "<" in bf_type:
			huawei(port)
		elif "#" in bf_type:
			crt.Screen.Send("show version")
			crt.Screen.Send("\r")
			crt.Screen.WaitForString("Unexpected input:", 1)
			screenrow = crt.Screen.CurrentRow# - 1
			bf_type_cisco_ericcson = crt.Screen.Get(crt.Screen.CurrentRow, 0, crt.Screen.CurrentRow, crt.Screen.CurrentColumn)
			if "Unexpected input:" in bf_type_cisco_ericcson:
				ericsson(port)
			else:	
				cisco(port)
		elif " >" in bf_type:
			DZS(port)
		elif ">" in bf_type:
			SSAB_ZTE(port)
	
def huawei(port):
	#Ask for which port
	#port = crt.Dialog.Prompt("Enter port to diagnose", "BF-diagnose Huawei")
		
	node = crt.Screen.Get(crt.Screen.CurrentRow, 0, crt.Screen.CurrentRow, crt.Screen.CurrentColumn)
	
	if "<" in node:
		node = node.replace('<', '',1)
	if ">" in node:
		node = node.replace('>', '',1)
	
	data = "Node name: " + node + "\n"
	data += "Port: GigabitEthernet 0/0/" + port + "\n"
	#Check link and type of connection
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
		if 	"COMMON FIBER" in data_read:
			data += "COMMON FIBER\r"
            
			#Capture Rx and Tx
			crt.Screen.Send("display transceiver diagnosis interface GigabitEthernet 0/0/" + port)
			crt.Screen.Send("\r")
			
			#get Tx
			crt.Screen.WaitForString("RxPower(dBm)", 1)
			screenrow = crt.Screen.CurrentRow - 1 
			Tx = crt.Screen.Get(screenrow, 1, screenrow, 25)
			#Put Tx in data
			data += Tx + "\n"
			
			#get Rx
			crt.Screen.WaitForString("Current(mA)", 1)
			screenrow = crt.Screen.CurrentRow - 1
			Rx = crt.Screen.Get(screenrow, 1, screenrow, 25)
			#Put Rx in data
			data += Rx
			
		elif "COMBO AUTO" in data_read:
			data += "COMBO AUTO\r"
			
			#Capture Rx and Tx
			crt.Screen.Send("display transceiver diagnosis interface GigabitEthernet 0/0/" + port)
			crt.Screen.Send("\r")
			
			#get Tx
			crt.Screen.WaitForString("RxPower(dBm)", 1)
			screenrow = crt.Screen.CurrentRow - 1 
			Tx = crt.Screen.Get(screenrow, 1, screenrow, 25)
			#Put Tx in data
			data += Tx + "\n"
			
			#get Rx
			crt.Screen.WaitForString("Current(mA)", 1)
			screenrow = crt.Screen.CurrentRow - 1
			Rx = crt.Screen.Get(screenrow, 1, screenrow, 25)
			#Put Rx in data
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
			
			data += CaptureOutputOfCommand("\r" , "Info: The test result is only for reference.")
			crt.Screen.Send("q")
			crt.Screen.Send("\r")
			crt.Screen.Send("q")
			crt.Screen.Send("\r")
	
	#If link is up, check all other good stuff
	#data_read = None
	elif port_status == True:
		
		#Fails at G-SGN-BF513-2 port 5, needs further investigation
		crt.Screen.Send("display dhcp snooping user-bind interface GigabitEthernet 0/0/" + port)
		data_read_2 = CaptureOutputOfCommand("\r", "Total count")
		if "Info: The number of dhcp snooping bind-table is zero." in data_read_2:
			data += "No IP-adresses assigned to devices on port"	
			
			#data_read2 += CaptureOutputOfCommand("display mac-address GigabitEthernet 0/0/" + port, "<")
			#if "Total items displayed = 0" in data_read:
			#	data += "No MAC-adresses on port"
		#else:
		#	data += data_read
		#data += data_read_2
		
	crt.Dialog.MessageBox(data)
	
	crt.Clipboard.Format = "CF_TEXT"
	crt.Clipboard.Text = data

	
def cisco(port):
	#Ask for which port
	#port = crt.Dialog.Prompt("Enter port to diagnose", "BF-diagnose Cisco")
	node = crt.Screen.Get(crt.Screen.CurrentRow, 0, crt.Screen.CurrentRow, crt.Screen.CurrentColumn)
	
	if "#" in node:
		node = node.replace('#', '',1)
		
	data = "Node name: " + node + "\n"
	data += "Port: fastEthernet 0/" + port + "\n"		
	
	data_read = CaptureOutputOfCommand("show interfaces fastEthernet 0/" + port, "Last input")
	
	if "% Invalid input detected at '^' marker." in data_read:
		crt.Dialog.MessageBox("Please rerun the script with a valid port")
		return
	elif "connected" in data_read:
		data += "Port is UP\n"
		port_status = True
	elif "notconnect" in data_read:
		data += "Port is DOWN\n"
		port_status = False
	else:
		data += "Port is err-disabled - try restarting the port\n"
		port_status = False
		
	if port_status == False:
		if "100BaseTX" in data_read:
			data += "Copper interface\n"
			crt.Screen.Send("test cable-diagnostics tdr interface fastEthernet 0/" + port)
			crt.Screen.Send("\r")
			data_read = CaptureOutputOfCommand("show cable-diagnostics tdr interface fastEthernet 0/" + port , "Pair C")
			
		else:
			data += "Fiber, go fuck yourself"
	elif port_status == True:
		data_read = CaptureOutputOfCommand("show ip dhcp snooping binding interface fastEthernet 0/" + port, "Total number of bindings:")
		screenrow = crt.Screen.CurrentRow - 2
		binding_row = crt.Screen.Get(screenrow, 1, screenrow, 25)
		if binding_row == "Total number of bindings: 0":
			data += "No IP-adresses assigned to devices on port"
		#else:
		#	data += data_read
		
	crt.Dialog.MessageBox(data)
	
	crt.Clipboard.Format = "CF_TEXT"
	crt.Clipboard.Text = data	

def ericsson(port):

	crt.Screen.Send("\r")
	node = crt.Screen.Get(crt.Screen.CurrentRow, 0, crt.Screen.CurrentRow, crt.Screen.CurrentColumn)
	
	if "#" in node:
		node = node.replace('#', '',1)
		
	data = "Node name: " + node + "\n"
	data += "Port: " + port + "\n"		
	
	data_read = CaptureOutputOfCommand("get ethernet_port " + port, "sp")
	crt.Screen.Send("\r")
	
	if "Bad range" in data_read:
		crt.Dialog.MessageBox("Please rerun the script with a valid port")
		return
	elif "Unexpected input:" in data_read:
		crt.Dialog.MessageBox("Please rerun the script with a valid port")
		return
	elif "up" in data_read:
		data += "Port is UP\n"
		port_status = True
	elif "down" in data_read:
		data += "Port is DOWN\n"
		port_status = False		
	
	crt.Screen.WaitForString(node, 3)
	
	if port_status == True:
		data += "See IP info in session"
		data_read = CaptureOutputOfCommand("get connection vlan * ethernet_port " + port, "----MORE")
		#crt.Screen.Send("get connection vlan * ethernet_port " + port)
		crt.Screen.Send("\r")
		if (crt.Screen.WaitForString("----MORE: Press Enter to continue, Esc or Q to abort", 3)) == True:
			crt.Screen.Send("\r")
		#data_read = CaptureOutputOfCommand("get connection vlan * ethernet_port " + port, "----MORE")
		#data_read =+ CaptureOutputOfCommand("\r" + port, node)
	
	crt.Dialog.MessageBox(data)
	
	crt.Clipboard.Format = "CF_TEXT"
	crt.Clipboard.Text = data		

def DZS(port):

	node = crt.Screen.Get(crt.Screen.CurrentRow, 0, crt.Screen.CurrentRow, crt.Screen.CurrentColumn)
	
	if ">" in node:
		node = node.replace('>', '',1)
		
	data = "Node name: " + node + "\n"
	data += "Port: ethernet 0/" + port + "\n"	

	data_read = CaptureOutputOfCommand("show interface ethernet 0/" + port, "Port Mode is access")
	
	if "% Can't find interface" in data_read:
		crt.Dialog.MessageBox("Please rerun the script with a valid port")
		return		
	elif "is down, line" in data_read:
		data += "Port is down\n"
		port_status = False
	elif "is up, line" in data_read:
		data += "Port is up\n"
		port_status = True
	
	data_read = CaptureOutputOfCommand("show ip dhcp snooping binding ethernet 0/" + port, "Total dhcp snoop binding entry")
	
	data += data_read
	
	crt.Dialog.MessageBox(data)
	
	crt.Clipboard.Format = "CF_TEXT"
	crt.Clipboard.Text = data

def SSAB_ZTE(port):

	node = crt.Screen.Get(crt.Screen.CurrentRow, 0, crt.Screen.CurrentRow, crt.Screen.CurrentColumn)
	
	if ">" in node:
		node = node.replace('>', '',1)
		
	data = "Node name: " + node + "\n"
	data += "Port: ethernet 0/" + port + "\n"
	
	crt.Dialog.MessageBox(data)
	
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
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


#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
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