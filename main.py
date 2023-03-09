from puppy import Parser, Args, Attr

@Args(author='dev<dev@gmail.com>', version='1.0.0')
class App(Parser):
	'''This is a simple demo app'''

	@Attr(short_name=True)
	@classmethod
	def message() -> str:
		'''The message to be displayed.'''
		pass

	@Attr(short_name=True, default_value=1)
	@classmethod
	def count() -> int:
		'''Number of times the message needed to be displayed'''
		pass

	@Attr(default_value='\n')
	@classmethod
	def sep() -> str:
		'''The separator between each message displayed'''
		pass


App.parse()
if(len(App.args()) == 0):
	App.help()
else:
	if(App.message.value):
		for i in range(App.count.value):
			print(App.message.value, end=App.sep.value)