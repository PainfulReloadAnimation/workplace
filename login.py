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
	
	preLine = crt.Screen.Get(crt.Screen.CurrentRow -2, 0, crt.Screen.CurrentRow -2, crt.Screen.CurrentColumn)
	currentLine = crt.Screen.Get(crt.Screen.CurrentRow, 0, crt.Screen.CurrentRow, crt.Screen.CurrentColumn)	
	
	if ("Username:" in currentLine) and ("User Access" not in preLine):
		huawei()
	elif ("Username: " in currentLine) and ("User Access" in preLine):
		cisco()
	elif "login:" in currentLine:
		ericsson()
	elif "se's password: " in currentLine:
		dzs()
	
def huawei():
	crt.Screen.Send("na@local\r")
	if(crt.Screen.WaitForString("assword:")):
		crt.Screen.Send("tN58sLM238Kp\r")

def cisco():
	crt.Screen.Send("netadmin2\r")
	if(crt.Screen.WaitForString("assword:")):
		crt.Screen.Send("xoo3uzahPh\r")
		
def ericsson():
	crt.Screen.Send("admin\r")
	if(crt.Screen.WaitForString("assword: ")):
		crt.Screen.Send("qwerty\r")
	
def dzs():
		crt.Screen.Send("tN58sLM238Kp\r")
		
