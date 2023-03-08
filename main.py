from puppy import Parser, Args, Attr

parser = Parser()

@Args(parser, author='dev<dev@gmail.com>', version='1.0.0')
class App:
	'''This is a simple demo app'''

	@Attr(short_name=True)
	@classmethod
	def message(msg: str):
		'''The message to be displayed.'''
		pass

	@Attr(short_name=True)
	@classmethod
	def count(c: int):
		'''Number of times the message needed to be displayed'''
		pass


parser.parse()
args = parser.args()
if len(args):
	print(args)
