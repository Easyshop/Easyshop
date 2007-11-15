# zope imports
from zope.interface import implements
from zope.component import adapts

# CMFCore imports
from Products.CMFCore.utils import getToolByName

# easyshop imports
from easyshop.core.interfaces import IAddress
from easyshop.core.interfaces import IAddressManagement
from easyshop.core.interfaces import ICopyManagement
from easyshop.core.interfaces import ICustomer
from easyshop.core.interfaces import IDirectDebit
from easyshop.core.interfaces import IPaymentManagement

from easyshop.customers.content import Address
from easyshop.customers.content import Customer
from easyshop.payment.content import DirectDebit

class CustomerCopyManagement:
    """
    """
    implements(ICopyManagement)
    adapts(ICustomer)

    def __init__(self, context):
        """
        """
        self.context = context                  

    def copyTo(self, target=None, new_id=None):
        """
        """
        if target is None:
            target = self.context.aq_inner.aq_parent

        if new_id is None:
            new_id = self.context.id

        wftool = getToolByName(self.context, "portal_workflow")
        
        new_customer = Customer(new_id)
        for field in ICustomer.names():
            setattr(new_customer, field, getattr(self.context, field))

        # Set object
        target._setObject(new_id, new_customer)
        new_customer = target[new_id]

        # Copy addresses    
        session_addresses = IAddressManagement(self.context).getAddresses()
        for session_address in session_addresses:
            new_address = Address(session_address.id)
            for field in IAddress.names():
                setattr(new_address, field, getattr(session_address, field))
            new_customer._setObject(new_address.id, new_address)
            new_address = new_customer[new_address.id]
            wftool.notifyCreated(new_address)

        # Copy customer payment methods.
        pm = IPaymentManagement(self.context)
        for session_direct_debit in pm.getPaymentMethods(IDirectDebit):
            new_direct_debit = DirectDebit(session_direct_debit.id)
            for field in IDirectDebit.names():
                setattr(new_direct_debit, field, getattr(session_direct_debit, field))
            new_customer._setObject(new_direct_debit.id, new_direct_debit)
            new_direct_debit = new_customer[new_direct_debit.id]
            wftool.notifyCreated(new_direct_debit)
        
        new_customer.reindexObject()
        wftool.notifyCreated(new_customer)
        
        return new_customer