import frappe
from . import utils

def get_context(context):
    utils.get_common_context(context)
    print(context.members[0].bio)
