
class Profile:
	'''
	Example:
	my =Profile('Kraiyosw')
	my.company = 'EnkeiThai.co.th'
	my.hobby = ['Programer','Movie','Reading',]
	print(my.name)
	my.show_email()
	my.show_myart()
	my.show_hobby()
	'''

	def __init__(self,name):
		self.name = name
		self.company = ''
		self.hobby = []
		self.art = '''
				 /\_/\  (
 				( ^.^ ) _)
   				  \^/  (
                ( | | )
               (__d b__)
		''' 

	def show_email(self):
		if self.company != '':
			print('{}@{}'.format(self.name.lower(),self.company))
		else:
			print('{}@gmail.com'.format(self.name.lower()))

	def show_myart(self):
		print(self.art)
		

	def show_hobby(self):  
		if len(self.hobby)!=0:
			print('---------My Hobby--------')
			for i,h in enumerate (self.hobby,start=1):
				print(i,h)
				print('-------------------------')
		else:
			print('No Hobby')
