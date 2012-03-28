from zc.relation.interfaces import ICatalog
from z3c.relationfield.index import RelationCatalog
from zope.app.intid.interfaces import IIntIds as app_IIntIds
from zope.intid.interfaces import IIntIds
from five.intid.site import addUtility
from five.intid.intid import IntIds
from zope.component import getUtility

from plone.app.relationfield.relation import convert
from z3c.relationfield.event import updateRelations

def add_relations(context):
    addUtility(context, ICatalog, RelationCatalog, ofs_name='relations',
               findroot=False)

def add_intids(context):
    # We need to explicilty use the zope.intids interface and
    # the zope.app.intids one
    addUtility(context, IIntIds, IntIds, ofs_name='intids',
               findroot=False)
    addUtility(context, app_IIntIds, IntIds, ofs_name='intids',
               findroot=False)

def installRelations(context):
    if context.readDataFile('install_relations.txt') is None:
        return
    portal = context.getSite()
    add_relations(portal)
    return "Added relations utility."

def upgradeRelations(context):
    if context.readDataFile('install_relations.txt') is None:
        return
    portal = context.getSite()
    catalog = getUtility(ICatalog)
    relations = [relation for relation in catalog.findRelations()]
    objects = set()
    for relation in relations:
        catalog.unindex(relation)
        convert(relation)
    for obj in objects:
        updateRelations(obj, None)
        
        
