# Python imports
import re
import urllib

# Five imports
from Products.Five.browser import BrowserView

# CMFCore imports
from Products.CMFCore.utils import getToolByName

# plone imports
from plone.memoize.instance import memoize

# easyshop imports
from easyshop.core.interfaces import IAddressManagement
from easyshop.core.interfaces import ICartManagement
from easyshop.core.interfaces import IOrderManagement
from easyshop.core.interfaces import IShopManagement

class CustomersContainerView(BrowserView):
    """
    """
    def getAddresses(self):
        """
        """
        customer = self._getCustomer()
        if customer is None:
            return None
            
        goto  = self.context.absolute_url()
        goto += "?letter=%s" % self.request.get("letter")
        goto += "&uid=%s" % customer.UID()
        goto  = urllib.quote(goto)
        
        am = IAddressManagement(customer)
        
        addresses = []
        for address in am.getAddresses():
            
            # create name 
            name = address.getFirstname() + " " + address.getLastname()
            
            # create address 1
            address1 = address.getAddress1()
            if address.getAddress2():
                address1 += " / "
                address1 += address.getAddress2()

            # create address 2
            address2 = address.getZipCode()  + " " + \
                       address.getCity()     + " - " + \
                       address.getCountry()
            
            addresses.append({
                "name"     : name,
                "address1" : address1,
                "address2" : address2,                             
                "phone"    : address.getPhone(),
                "url"      : address.absolute_url() + "/@@edit?goto=" + goto
            })

        return addresses
            
    def getCart(self):
        """
        """
        customer = self._getCustomer()
        if customer is None:
            return None
            
        shop = IShopManagement(self.context).getShop()
        cart = ICartManagement(shop).getCartById(customer.getId())
        
        if cart is None:
            return None
        else:
            return {
                "url" : cart.absolute_url()
            }
        
    def getCustomer(self):
        """
        """
        customer = self._getCustomer()
        if customer is None:
            return None
        
        goto  = self.context.absolute_url()
        goto += "?letter=%s" % self.request.get("letter")
        goto += "&uid=%s" % customer.UID()
        goto  = urllib.quote(goto)
            
        return {
            "name"  : customer.Title(),
            "email" : customer.getEmail(),
            "url"   : customer.absolute_url() + "/@@edit?goto=" + goto,
            "uid"   : customer.UID(),
            "id"    : customer.getId(),
        }
                
    def getCustomers(self):
        """
        """
        catalog = getToolByName(self.context, "portal_catalog")
        letter = self.request.get("letter", "")
        result = []
                            
        searchable_text = self.request.get("searchable_text", "")
        if searchable_text != "":
            result = catalog.searchResults(
                path = "/".join(self.context.getPhysicalPath()),
                portal_type = "Customer",
                SearchableText = searchable_text,
                sort_on = "sortable_title",
            )
                    
        elif letter == "":
            return []
        
        elif letter == "All":
            result = catalog.searchResults(
                path = "/".join(self.context.getPhysicalPath()),
                portal_type = "Customer",
                sort_on = "sortable_title",
            )
            
        elif letter == "0-9":
            brains = catalog.searchResults(
                path = "/".join(self.context.getPhysicalPath()),
                portal_type = "Customer",
                sort_on = "sortable_title",
            )
                    
            for brain in brains:
                if re.match("\d", brain.Title):
                    result.append(brain)
        else:
            result = catalog.searchResults(
                path = "/".join(self.context.getPhysicalPath()),
                portal_type = "Customer",
                lastname = "%s*" % letter,
                sort_on = "sortable_lastname",
            )
            
        temp = []
        for customer in result:

            temp.append({
                "name" : customer.Title,
                "uid"  : customer.UID,
                "url"  : customer.getURL(),
            })
        
        return temp
        
    def getLetters(self):
        """
        """
        return  ("All", "0-9", "A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", 
                 "L", "M", "N", "O", "P", "Q", "R", "S", "T", "U", "V", "W",
                 "X", "Y", "Z")

    def getOrders(self):
        """
        """
        ttool = getToolByName(self.context, 'translation_service')
        wftool = getToolByName(self.context, "portal_workflow")

        customer = self._getCustomer()
        if customer is  None:
            return []
            
        shop = IShopManagement(self.context).getShop()
        om = IOrderManagement(shop)
        
        orders = []                
        for order in om.getOrdersForCustomer(customer.getId()):
            
            # get fullname
            fullname = "There is no customer."
            customer = order.getCustomer()
            if customer is not None:
                am = IAddressManagement(customer)
                address = am.getInvoiceAddress()
                if address is not None:
                    fullname = address.getName(reverse=True)
                                
            # created
            created = ttool.ulocalized_time(order.created(), long_format=True)
            
            orders.append({
                "id"            : order.getId(),
                "url"           : order.absolute_url(),
                "created"       : created,
                "customer_name" : fullname,
                "review_state"  : wftool.getInfoFor(order, "review_state")
            })
            
        return orders   
        
    @memoize
    def _getCustomer(self):
        """
        """
        uid = self.request.get("uid")
        catalog = getToolByName(self.context, "portal_catalog")
        brains = catalog.searchResults(
            UID = uid
        )
        
        try:
            return brains[0].getObject()
        except:
            return None