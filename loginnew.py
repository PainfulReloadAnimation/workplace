# $language = "Python"
# $interface = "1.0"

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
def Inject_crt_Object(obj_crt_API):
    # Make the crt variable global for use in multiple functions in the
    # module that might need access to the crt object.
    global crt
    # Associate the crt variable with the crt object passed in from the
    # Main script.
    crt = obj_crt_API
    return

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


def logger():
	crt.Screen.Synchronous = True

	user = "NA"

	sshTelnet(user)


def sshTelnet(user):
	dzsString = ""

	node = crt.Dialog.Prompt("Enter node", "Enter node")
	if " " in node:
		node = node.replace(" ", "")
	if "10." in node:
		crt.Screen.Send("telnet " + node + "\r")
		dzsString = "Connected to " + node + "."
	elif ".k" in node:
		crt.Screen.Send("telnet " + node + "\r")
		dzsString = "Connected to " + node + "."
	else:
		crt.Screen.Send("telnet " + node + ".k.se.telia.net\r")
		dzsString = "Connected to " + node + ".k.se.telia.net."

	# DZS login check
	if ((crt.Screen.WaitForString(dzsString, 1) == False)):
		preLine = crt.Screen.Get(crt.Screen.CurrentRow - 2, 0, crt.Screen.CurrentRow - 2, crt.Screen.CurrentColumn)
		currentLine = crt.Screen.Get(crt.Screen.CurrentRow, 0, crt.Screen.CurrentRow, crt.Screen.CurrentColumn)

		crt.Screen.Send(chr(3))
		crt.Screen.Send("\r")
		if "10." in node:
			crt.Screen.Send("ssh " + user + "@" + node + "\r")
		elif ".k" in node:
			crt.Screen.Send("telnet " + user + "@" + node + "\r")
		else:
			crt.Screen.Send("ssh " + user + "@" + node + ".k.se.telia.net\r")
		currentLine = crt.Screen.Get(crt.Screen.CurrentRow, 0, crt.Screen.CurrentRow, crt.Screen.CurrentColumn)
		if (
		(crt.Screen.WaitForString("Are you sure you want to continue connecting (yes/no/[fingerprint])?", 2) == True)):
			crt.Screen.Send("yes\r")
		elif ((crt.Screen.WaitForString("Are you sure you want to continue connecting (yes/no)?", 2) == True)):
			crt.Screen.Send("yes\r")
	# Not DZS
	else:
		login()


def login():
	crt.Screen.WaitForString("Username:", 1)
	crt.Screen.WaitForString("login:", 1)

	preLine = crt.Screen.Get(crt.Screen.CurrentRow - 2, 0, crt.Screen.CurrentRow - 2, crt.Screen.CurrentColumn)
	currentLine = crt.Screen.Get(crt.Screen.CurrentRow, 0, crt.Screen.CurrentRow, crt.Screen.CurrentColumn)

	if ("Username:" in currentLine) and ("User Access" not in preLine):
		huawei()
	elif ("Username: " in currentLine) and ("User Access" in preLine):
		cisco()
	elif "login:" in currentLine:
		ericsson()


def huawei():
	crt.Screen.Send("na@local\r")
	if (crt.Screen.WaitForString("assword:")):
		crt.Screen.Send("tN58sLM238Kp\r")


def cisco():
	crt.Screen.Send("f-netadmin\r")
	if (crt.Screen.WaitForString("assword:")):
		crt.Screen.Send("mkgTOa5MHfb1qJh\r")


def ericsson():
	crt.Screen.Send("admin\r")
	if (crt.Screen.WaitForString("assword: ")):
		crt.Screen.Send("qwerty\r")


def dzs(node):
	if ((crt.Screen.WaitForString("A@" + node + ".k.se.telia.net's password: ", 2) == True)):
		crt.Screen.Send("tN58sLM238Kp\r")
	else:
		crt.Screen.Send("tN58sLM238Kp\r")
		
