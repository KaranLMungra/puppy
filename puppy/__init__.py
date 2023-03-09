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
				self.arguments[n]['value'] = arg
				n = -1
			for i, argument in enumerate(self.arguments):
				if arg == argument['short_name'] or arg == argument['long_name']:
					n = i

	def args(self):
		args = []
		for arg in self.arguments:
			if(arg['value']):
				x = arg['value']
				if(arg['types'] == type(1)):
					x = int(arg['value'])
				args.append([arg['long_name'][2:], x])
		return args


	def add_argument(self, callback, about, short_name, long_name):
		argument = {
			'callback': callback,
			'about': about,
			'short_name': short_name,
			'long_name': long_name,
			'types': callback.__annotations__['return'],
			'value': None
		}
		self.arguments.append(argument)

	def help(self):
		if self.about: print(self.about, end='\n\n')
		if self.version: print(self.version)
		if self.author: print(self.author)
		print(self.usage, end='\n\n')
		print('Options:')
		for arg in self.arguments:
			about = arg['about']
			short_name = arg['short_name']
			long_name = arg['long_name']
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
	def decorate(c):
		p.author = author
		p.version = version
		p.about = c.__doc__
		attributes = getMethods(c)
		
		for attr in attributes:
			name = attr[0]
			call = attr[1]
			short_name, long_name = '', ''
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