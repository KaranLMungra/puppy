import sys
def getMethods(MyClass):
	attributes = []
	for attribute in MyClass.__dict__.keys():
		if attribute[:2] != '__':
			value = getattr(MyClass, attribute)
			if callable(value):
				attributes.append((attribute, value))
	return attributes

class Parser:
	def __init__(self):
		self.author: str
		self.version:str		
		self.about:str
		self.usage = f'Usage: {sys.argv[0]} [OPTIONS]' 
		self.arguments = []


	def parse(self):
		args = sys.argv[1:]
		if(len(args) == 0):
			self.help()
			# print(self.usage, end='\n\n')
			# print('Try passing option -h or  --help for more help.')
		n = -1
		for arg in args:
			if n != -1:
				self.arguments[n][5] = arg
				n = -1
				continue
			for i, argument in enumerate(self.arguments):
				if arg == argument[2] or arg == argument[3]:
					n = i

	def args(self):
		args = []
		for arg in self.arguments:
			if(arg[5]):
				x = arg[5]
				if(arg[4] == type(1)):
					x = int(arg[5])
				args.append([arg[3][2:], x])
		return args


	def add_argument(self, callback, about, short_name, long_name):
		for x in callback.__annotations__.keys():
			types = callback.__annotations__[x]
		self.arguments.append([callback, about, short_name, long_name, types, ''])

	def help(self):
		if self.about: print(self.about, end='\n\n')
		if self.version: print(self.version)
		if self.author: print(self.author)
		print(self.usage, end='\n\n')
		print('Options:')
		for arg in self.arguments:
			about = arg[1]
			short_name = arg[2]
			long_name = arg[3]
			hstr = '  '
			if short_name:
				hstr += short_name
			if short_name and long_name: hstr += ', '
			if long_name:
				hstr += long_name
			hstr += f' <{long_name[2:].upper()}>'
			if about:
				hstr += f'  {about}'
			print(hstr)

def Args(p, author = '', version = ''):
	p.author = author
	p.version = version
	def decorate(c):
		p.about = c.__doc__
		attributes = getMethods(c)
		for attr in attributes:
			name = attr[0]
			call = attr[1]
			if call.short_name: short_name = f'-{name[0].lower()}'
			if call.long_name: long_name = f'--{name.lower()}'
			p.add_argument(call, call.__doc__, short_name, long_name)
		return c
	return decorate

def Attr(short_name=False, long_name=True):
	def decorate(fn):
		func = fn.__func__ 
		func.short_name=short_name
		func.long_name=long_name
		return fn
	return decorate 