# zope imports
from zope.interface import implements
from zope.component import adapts

# easyshop imports
from iqpp.easyshop.interfaces import ICustomerManagement
from iqpp.easyshop.interfaces import IPaymentMethodManagement
from iqpp.easyshop.interfaces import IPaymentMethodCriteria
from iqpp.easyshop.interfaces import IValidity
from iqpp.easyshop.interfaces import IShopManagement

class PaymentMethodCriteriaValidity:
    """Adapter which provides IValidity for weight criteria content objects.
    """
    implements(IValidity)
    adapts(IPaymentMethodCriteria)

    def __init__(self, context):
        """
        """
        self.context = context
        
    def isValid(self, product=None):
        """Returns True if the selected payment method of the current customer 
        is within the selected payment methods of the criterion.
        """
        shop = IShopManagement(self.context).getShop()
        
        customer = ICustomerManagement(shop).getAuthenticatedCustomer()        
        customer_payment_method = customer.selected_payment_method
        
        if customer_payment_method in self.context.getPaymentMethods():
            return True
        else:
            return False