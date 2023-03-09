import sys
def getMethods(MyClass):
	attributes = []
	for attribute in MyClass.__dict__.keys():
		if attribute[:2] != '__':
			value = getattr(MyClass, attribute)
			if callable(value):
				attributes.append((attribute, value))
	return attributes

def into_type(x, t):
	if t == int:
		return int(x)
	return x

class Parser:
	author = ''
	version = ''
	about = ''
	usage = f'Usage: {sys.argv[0]} [OPTIONS]'
	arguments = []
	__help = False
	@staticmethod
	def parse():
		args = sys.argv[1:]			
		n = -1
		for arg in args:
			if n != -1:
				arg = into_type(arg, Parser.arguments[n]['dtype'])
				Parser.arguments[n]['value'] = arg
				Parser.arguments[n]['callback'].__func__.value = arg
				n = -1
			for i, argument in enumerate(Parser.arguments):
				if arg == '-h' or arg == '--help':
					Parser.arguments[i]['value'] = True
					Parser.__help = True
					continue
				if arg == argument['short_name'] or arg == argument['long_name']:
					n = i
	@staticmethod
	def has_help():
		return Parser.__help
	
	@staticmethod
	def n_args():
		return len([arg for arg in Parser.arguments if arg['value']])

	@staticmethod
	def add_argument(callback, about, short_name, long_name):
		argument = {
			'callback': callback,
			'about': about,
			'short_name': short_name,
			'long_name': long_name,
			'dtype': callback.__annotations__['return'],
			'value': None
		}
		Parser.arguments.append(argument)

	@staticmethod
	def help() -> None:
		if Parser.about: print(Parser.about, end='\n\n')
		if Parser.version: print(Parser.version)
		if Parser.author: print(Parser.author)
		print(Parser.usage, end='\n\n')
		print('Options:')
		for arg in Parser.arguments:
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

def Args(author = '', version = ''):
	def decorate(c):
		Parser.author = author
		Parser.version = version
		Parser.about = c.__doc__
		attributes = getMethods(c)
		for attr in attributes:
			name = attr[0]
			call = attr[1]
			short_name, long_name = '', ''
			if call.short_name: short_name = f'-{name[0].lower()}'
			if call.long_name: long_name = f'--{name.lower()}'
			c.add_argument(call, call.__doc__, short_name, long_name)
		c.add_argument(Parser.help, 'Prints Help', '-h', '--help')
		return c
	return decorate

def Attr(short_name=False, long_name=True, default_value=None):
	def decorate(fn):
		func = fn.__func__ 
		func.short_name=short_name
		func.long_name=long_name
		func.value = default_value
		return fn
	return decorate 