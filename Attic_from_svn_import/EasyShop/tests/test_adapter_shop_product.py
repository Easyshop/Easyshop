# Zope imports
from DateTime import DateTime

# zope imports
from zope.component import getMultiAdapter

# CMFCore imports
from Products.CMFCore.utils import getToolByName

# EasyShop imports 
from base import EasyShopTestCase
from Products.EasyShop.tests import utils
from Products.EasyShop.interfaces import IProductManagement

class TestShopProductManagement(EasyShopTestCase):
    """
    """
    def testGetAllProducts(self):
        """
        """
        pm = IProductManagement(self.shop)
        self.assertRaises(Exception, pm.getAllProducts)
        
    def testGetAmountOfProducts(self):
        """
        """        
        pm = IProductManagement(self.shop)
        self.assertRaises(Exception, pm.getAmountOfProducts)

    def testGetProducts(self):
        """
        """
        pm = IProductManagement(self.shop)
        self.assertRaises(Exception, pm.getProducts)

    def testGetTotalAmountOfProducts(self):
        """
        """
        pm = IProductManagement(self.shop)
        self.assertRaises(Exception, pm.getTotalAmountOfProducts)
        
def test_suite():
    from unittest import TestSuite, makeSuite
    suite = TestSuite()
    suite.addTest(makeSuite(TestShopProductManagement))
    return suite