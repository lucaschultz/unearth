import subprocess

################################################################################
#																			   #
#				Written by Luca Schultz for unearth from Joseph				   #
#				Chilcote. Returns a dictonary containing Users of			   #
#				a Mac and Info about them. Can by invoked using				   #
#				Exvacate.													   #
#																			   #
################################################################################



#===============================================================================	
def parse_dscl_output(stdout):
	'''
	Parses DSCL output into a dictonary.
	'''
	
	li = list(stdout.split())
	names = list([li[index] for index in range(0, len(li), 2)])
	ids = list([li[index] for index in range(1, len(li), 2)])
	tup = zip(names,ids)
	dic = dict(tup)
	return dic
	
	
#===============================================================================	
def get_user_dic():
	'''
	Returns a dictonary containing non system users and their IDs. 
	'''
	# use subprocess to run dscl command
	try:
		proc = subprocess.Popen(
				['dscl', '.', 'list', '/Users', 'UniqueID'],
				stdout=subprocess.PIPE,
				stderr=subprocess.PIPE
				)
		stdout, _ = proc.communicate()
	except (IOError, OSError):
		stdout = None

	# if no error occured
	if stdout:
		dic = parse_dscl_output(stdout)
	
	# remove all system users
	for key in dic.keys():
		if int(dic[key]) < 500:
			dic.pop(key)
			
	for key in dic.keys():
		dic[key] = {'id': dic[key]}
	
	# return dic of users with ids
	return dic



#===============================================================================	
def add_admin_info(dic):
	'''
	Adds info wether user is admin to user dictonary  
	'''
	# for every user in dictonary
	for key in dic.keys():
		
		# use subprocess to ask dseditgroup wether user is admin
		try:
				proc = subprocess.Popen(
						['dseditgroup', '-o', 'checkmember', '-m', key, 'admin'],
						stdout=subprocess.PIPE,
						stderr=subprocess.PIPE
						)
				stdout, _ = proc.communicate()
		except (IOError, OSError):
				stdout = None
		
		# if output exists	
		if stdout:
				answer = str(stdout)
		
		# if output not contains positive answer
		if answer.find("yes") == -1:
			# user is no admin
			dic[key]['admin'] = False
		else:
			# user is admin
			dic[key]['admin'] = True
			
	return dic
	

	
#===============================================================================	
def add_local_info(dic):
	'''
	Adds info wether user is local to user dictonary  
	'''
	for key in dic.keys():
		
		path = '/Users/' + key
			
		# use subprocess to ask dseditgroup wether user is admin
		try:
				proc = subprocess.Popen(
						['dscl', '.', 'read', path, \
						'OriginalAuthenticationAuthority', '2>/dev/null'],
						stdout=subprocess.PIPE,
						stderr=subprocess.PIPE
						)
				stdout, _ = proc.communicate()
		except (IOError, OSError):
				stdout = None
		
		# if output exists	
		if stdout:
			dic[key]['local'] = False
		else:
			dic[key]['local'] = True

	return dic



#===============================================================================	
factoid = 'user_info'
def fact():
	'''
	Returns a dictonary containing all non-system users and info about them.
	Written for use with https://github.com/chilcote/unearth.
	'''
	
	result = get_user_dic()
	result = add_local_info(result)
	result = add_admin_info(result)
	
	return {factoid: result}



#===============================================================================	
if __name__ == '__main__':
	print '<result>%s</result>' % fact()[factoid]
	
	

		
	