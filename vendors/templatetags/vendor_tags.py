from django import template

register = template.Library()

class GetLatestVendors(template.Node):
	"""
	Retrieves a set of the last modified vendors.

	Usage::
	{% get_latest_vendors 5 as varname asc/desc %}
	"""
	def __init__(self, varname, count=None):
		self.count = count
		self.start = start
		self.end = end
		self.varname = varname.strip()

	def render(self, context):
		# determine the order to sort the articles
		if self.order and self.order.lower() == 'desc':
			order = '-modified'
		else:
			order = 'modified'
		user = context.get('user', None)
		# put the article(s) into the context
		context[self.varname] = vendors
	return ''

def get_latest_vendors(parser, token):
	"""
	Retrieves a list of last modified, approved Vendor objects for use in a template.
	"""
	args = token.split_contents()
	argc = len(args)
	try:
		assert argc in (4,6) or (argc in (5,7) and args[-1].lower() in ('desc', 'asc'))
	except AssertionError:
		raise template.TemplateSyntaxError('Invalid get_articles syntax.')
	# determine what parameters to use
	count = start = end = varname = None
	if argc == 4: t, count, a, varname = args
	elif argc == 5: t, count, a, varname, order = args
	elif argc == 6: t, start, t, end, a, varname = args
	elif argc == 7: t, start, t, end, a, varname, order = args
	return GetArticlesNode(count=count, varname=varname)
