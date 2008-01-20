# zope imports
from zope.interface import implements

# Archetypes imports
from Products.Archetypes.atapi import *

# easyshop imports
from easyshop.core.config import PROJECTNAME
from easyshop.core.interfaces import IProperty

class ProductProperty(OrderedBaseFolder):
    """Product properties hold selectable options.
    """
    implements(IProperty)    

    def getOptions(self):
        """
        """
        result = []
        for option in self.objectValues():
            # image
            if len(option.getImage()) > 0:
                image_url = option.absolute_url() + "/image_listing"
            else:
                image_url = None
                
            result.append({
                "id"        : option.getId(),
                "name"      : option.Title(),                
                "url"       : option.absolute_url(),
                "path"      : "/".join(option.getPhysicalPath()),
                "image_url" : image_url,
                "price"     : str(option.getPrice()),
             })
        
        return result
            
registerType(ProductProperty, PROJECTNAME)