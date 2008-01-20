# zope imports
from zope.interface import implements
from zope.component import adapts

# easyshop imports
from easyshop.core.interfaces import IProductVariants
from easyshop.core.interfaces import IProductVariantsManagement

class ProductVariantsManagement:
    """Provides IProductVariantsManagement for product content objects.
    """
    implements(IProductVariantsManagement)
    adapts(IProductVariants)

    def __init__(self, context):
        """
        """
        self.context = context

    def addVariants(self, properties, title="", article_id=""):
        """
        """
        article_id = article_id.replace("%A", self.context.getArticleId())
        article_id = article_id.replace("%T", self.context.Title())        

        title = title.replace("%A", self.context.getArticleId())
        title = title.replace("%T", self.context.Title())
        
        i=0
        for properties in self._cartesian_product(*properties):
            
            if self.hasVariant(properties):
                continue
            
            # format string
            i += 1
            new_article_id = article_id.replace("%n", str(i))
            new_title = title.replace("%n", str(i))
            
            new_id = self.context.generateUniqueId("ProductVariant")
            self.context.invokeFactory(
                "ProductVariant", 
                id=new_id, 
                title=new_title, 
                articleId=new_article_id,
                forProperties=properties)

    def deleteVariants(self, ids):
        """Deletes variants with given ids.
        """
        if not isinstance(ids, (list, tuple)):
            ids = (ids,)
        
        self.context.manage_delObjects(ids)
                
    def getDefaultVariant(self):
        """
        """
        try:        
            return self.getVariants()[0]
        except IndexError:
            return None
                
    def getVariants(self):
        """
        """
        return self.context.objectValues("ProductVariant")

    def getSelectedVariant(self, selected_properties=None):
        """
        """
        if selected_properties is None:
            selected_properties = {}
            for name, value in self.context.REQUEST.items():
                if name.startswith("property"):
                    selected_properties[name[9:]] = value

        result = []
        for key, value in selected_properties.items():
            result.append("%s:%s" % (key, value))
            
        result.sort()
        result = "|".join(result)
        
        for variant in self.context.objectValues("ProductVariant"):
            for_properties = list(variant.getForProperties())
            for_properties.sort()
            for_properties = "|".join(for_properties)
            
            if result.lower() == for_properties.lower():
                return variant

        return self.getDefaultVariant()
        
    def hasVariant(self, properties):
        """
        """
        properties.sort()
        for variant in self.getVariants():
            for_properties = list(variant.getForProperties())
            for_properties.sort()
            if properties == for_properties:
                return True
        return False
        
    def _cartesian_product(self, *seqin):
        """Calculates the cartesian product of given lists.
        """
        # Found in ASPN Cookbook
        def rloop(seqin, comb):
            if seqin:
                for item in seqin[0]:
                    newcomb = comb + [item]
                    for item in rloop(seqin[1:], newcomb):
                        yield item
            else:
                yield comb
        
        return rloop(seqin, [])