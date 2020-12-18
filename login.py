from termcolor import colored
import encrypt as crypto
import ast
import os
from shutil import copyfile

commands = ("new","rem","see","all","bye","hlp","rst")
cmd = ""
dict_of_database = dict()

def rst():
	# restoredatabase
	filename = db_name[1]
	os.rename('b_'+ filename, 'e_'+ filename )
	print "database restored"
	execute()

def execute():
	'''
	Evaluates the input and runs the command acordingly. cmd() can be any command listed.
	'''
	cmd = raw_input(colored("cmd_: ", 'cyan'))
	while cmd not in commands:
		print colored("Error:",'red'),("[ %s ] command not found." % cmd)
		cmd = raw_input(colored("cmd_: ", 'cyan'))
	cmd = eval(cmd) #converts string to object
	cmd()

def new():
	'''
	Creates a new entry for a password.
	'''
	os.system("clear")
	print("creating entry: \n")
	Account = raw_input(colored("Account:  ", "yellow"))
	App = raw_input("App:      ")
	Mail = raw_input("Mail:     ")
	Password = raw_input("Password: ")
	Phone = raw_input("Phone:    ")
	Source = raw_input("Source:   ")	
	Type = raw_input(colored("Type:     ", "yellow"))
	Entry = dict(
			Account=Account,
			App=App,
			Source=Source,
			Password=Password,
			Mail=Mail,
			Phone=Phone,
			Type=Type,	
			)
	print("")
	print "Code #   :", int(last_code()) + 1
	print("")
	for i, v in sorted(Entry.iteritems()):
		print ("{0:8} : {1:30}").format(i,v)
	print("")
	with open(db_name[1], 'a') as f:
		line = str(int(last_code()) + 1) + " = " + str(Entry) + '\n'
		f.write(line)
		print colored("entry saved", "green")
	execute()

def rem():
	rem_code = raw_input("Type the code to remove: ")
	os.system("clear")
	#Same as see() command but removes instead
	if rem_code in dict_of_database:
		print "removing entry: "
		print rem_code, dict_of_database[rem_code]
		f = open(db_name[1], 'r')
		masterkey = f.readline()
		lines = f.readlines()
		f.close()
		f = open(db_name[1], 'w')
		f.write(masterkey)
		for line in lines:
			if line != rem_code +" "+ dict_of_database[rem_code]+'\n':
				f.write(line)
		f.close()
		del dict_of_database[rem_code]
	else:
		print colored("Error:",'red'),("[ %s ] code not found." % rem_code)
	execute()

def see():
	code = raw_input("Type the code to see: ")
	os.system("clear")
	#Find the inputed code, 
	#if it is found, then display the entry of that code, 
	#if not, display message, "code not found"
	if code in dict_data():
		print("displaying entry: ")
		Entry = str(dict_of_database[code][2:])
		newentry = eval(Entry)
		print("")
		print "Code #   :", code
		print("")
		for i, v in sorted(newentry.iteritems()):
			print ("{0:8} : {1:30}").format(i,v)
		# print code, dict_of_database[code]
	else:
		print colored("code not found", "red")
	execute()

def all():
	os.system("clear")
	print("displaying all entries: ")
	for code in sorted(dict_data()):
		#print str(dict_of_database[code])[2:]
		instance = ast.literal_eval(dict_of_database[code][2:])
		print code, '__' , colored(instance['Account'],'yellow'), '__' , colored(instance['Source'],'cyan')
	execute()

def encrypt():
	filename = db_name[1]
	password = db_name[0]
	crypto.encrypt(crypto.getKey(password), filename)
	print("Done.")
	os.remove(filename)
	copyfile("e_"+filename, "b_"+filename) #Backup of database.

def bye():
	encrypt()
	os.system("clear")
	print("see you soon")
	exit()

def hlp():
	os.system("clear")
	print("hlp = displays list of commands available")
	print("new = creates a new entry")
	print("rem = removes an entry")
	print("see = see an specific entry")
	print("all = see all entries saved")
	print("bye = exit and encrypts database")
	print("rst = restores last saved database")
	execute()

#CORE functions that returns values

def open_file():
	"""
	Takes an input to search the file of the database.
	If it is found, then open it, read the key.
	Returns a list of the information.
	[0] = masterkey
	[1] = db_name
	[2] = db_rows
	[3] = dict_of_database
	"""
	while True:
		try:
			db_name = raw_input("Find database name: ")
			with open(db_name, 'r') as f:
				masterkey = f.readline()[12:16]
				db_rows = f.readlines()
				for items in db_rows:
					code = items[:5]
					info = items[6:-1]
					dict_of_database[code] = str(info)
				f.close()
			break
		except IOError as e:
			print colored("Error:","red"),("[ %s ] database not found." % db_name)
	return masterkey, db_name, db_rows, dict_of_database

def last_code():
	with open(db_name[1], 'r') as f:
		db_rows = f.readlines()
		for item in db_rows:
			code = item[:5]
	last_code = code
	return last_code

def dict_data():
	with open(db_name[1], 'r') as f:
		masterkey = f.readline()
		db_rows = f.readlines()
		for item in db_rows:
			code = item[:5]
			info = item[6:-1]
			dict_of_database[code] = str(info)
	return dict_of_database

def login():
	if raw_input("Please input masterkey: ") == db_name[0]:
		os.system('clear')
	else:
		print("Go away!")
		quit()

def decrypt():
	#format for file naming is: ["e_" + ##]
	filename = "e_" + raw_input("File to decrypt: ")
	password = raw_input("Password: ")
	crypto.decrypt(crypto.getKey(password), filename)
	print("Done.")
	os.remove(filename)

decrypt()
db_name = open_file()
login()

#if masterkey is correct, then decrypt the file.
print "Opening:", db_name[1]
#encrypt database when using bye function, it is more secure.

#after login success then opens the command li ne
print("hlp = displays list of commands available")
execute()
