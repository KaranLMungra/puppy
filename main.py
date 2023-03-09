from puppy import Parser, Args, Attr

parser = Parser()

@Args(parser, author='dev<dev@gmail.com>', version='1.0.0')
class App:
	'''This is a simple demo app'''

	@Attr(short_name=True)
	@classmethod
	def message() -> str:
		'''The message to be displayed.'''
		pass

	@Attr(short_name=True)
	@classmethod
	def count() -> int:
		'''Number of times the message needed to be displayed'''
		pass

	@Attr()
	@classmethod
	def sep() -> str:
		'''The separator between each message displayed'''
		pass


parser.parse()
args = parser.args()
if len(args):
	print(args)

'''
# Output
- ```python main.py```

This is a simple demo app

> 1.0.0
> dev<dev@gmail.com>
> Usage: main.py [OPTIONS]
>
> Options:
>   -m, --message <MESSAGE>  The message to be displayed.
>   -c, --count <COUNT>  Number of times the message needed to be displayed

- ```python main.py -m 'World!' --count 98```

> [['message', 'World!'], ['count', 98]]
'''