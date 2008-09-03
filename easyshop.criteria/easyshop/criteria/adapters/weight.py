# zope imports
from zope.interface import implements
from zope.component import adapts

# easyshop imports
from iqpp.easyshop.interfaces import IValidity
from iqpp.easyshop.interfaces import ICartManagement
from iqpp.easyshop.interfaces import IItemManagement
from iqpp.easyshop.interfaces import IWeightCriteria
from iqpp.easyshop.interfaces import IShopManagement

class WeightCriteriaValidity:
    """Adapter which provides IValidity for weight criteria content objects.
    """
    implements(IValidity)
    adapts(IWeightCriteria)

    def __init__(self, context):
        """
        """
        self.context = context
        
    def isValid(self, product=None):
        """Returns True, if the total weight of the cart is greater than the
        entered criteria weight.
        """
        shop = IShopManagement(self.context).getShop()
        cart = ICartManagement(shop).getCart()
                
        if cart is None:
            cart_weight = 0
        else:
            cart_weight = 0
            for item in IItemManagement(cart).getItems():
                cart_weight += (item.getProduct().getWeight() * item.getAmount())
            
        if cart_weight > self.context.getWeight():
            return True
        return False        
