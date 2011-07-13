from django import template
from vendors.models import Vendor

register = template.Library()

class GetLatestVendors(template.Node):
    """
    Retrieves a set of the last modified vendors.

    Usage::
    {% get_latest_vendors 5 as varname %}
    """

    def __init__(self, varname, count=None):
        self.count = count
        self.varname = varname.strip()

    def render(self, context):
        if self.count == 'all':
            vendors = Vendor.public_objects.all()
        elif self.count > 0:
            vendors = Vendor.public_objects.all()[:self.count]
        else:
            vendors = None
        context[self.varname]=vendors
        return ''

def get_latest_vendors(parser, token):
	"""
	Retrieves a list of last modified, approved Vendor objects for use in a template.

    Tag example:

    {% get_latest_vendors 5 as vendors %}
	"""
	args = token.split_contents()
	argc = len(args)
	try:
		assert argc == 4 
	except AssertionError:
		raise template.TemplateSyntaxError('Invalid get_articles syntax.')
	# determine what parameters to use
	count = varname = None
	if argc == 4: t, count, a, varname = args
	return GetLatestVendors(count=count, varname=varname)

register.tag(get_latest_vendors)
