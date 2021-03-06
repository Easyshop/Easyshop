# Zope imports
from DateTime import DateTime

# zope imports
from zope.component import getMultiAdapter

# CMFCore imports
from Products.CMFCore.utils import getToolByName

# EasyShop imports 
from base import EasyShopTestCase
from Products.EasyShop.tests import utils
from Products.EasyShop.interfaces import ICategoryManagement

class TestProductCategoryManager(EasyShopTestCase):
    """
    """
    def afterSetUp(self):
        """
        """
        super(TestProductCategoryManager, self).afterSetUp()
        self.shop.products.invokeFactory(
            "Product", 
            id="product_3", 
            priceGross=19.0)        
            
        self.product_3 = self.shop.products.product_3
        
    def testHasCategories(self):
        """
        """
        cm = ICategoryManagement(self.product_1)
        self.assertEqual(cm.hasCategories(), True)

        cm = ICategoryManagement(self.product_3)
        self.assertEqual(cm.hasCategories(), False)

    def testHasParentCategory(self):
        """
        """
        cm = ICategoryManagement(self.product_1)
        self.assertEqual(cm.hasParentCategory(), False)
        
    def testGetCategories_1(self):
        """
        """
        cm = ICategoryManagement(self.product_1)

        ids = [c.getId() for c in cm.getCategories()]        
        self.assertEqual(ids, ["category_11"])

        # adding some more
        self.shop.categories.invokeFactory("Category", id="category_a")
        self.shop.categories.invokeFactory("Category", id="category_b")
        
        self.shop.categories.category_a.addReference(
            self.product_1, 
            "easyshopcategory_easyshopproduct")
        self.shop.categories.category_b.addReference(
            self.product_1, 
            "easyshopcategory_easyshopproduct")
                                        
        ids = [c.getId() for c in cm.getCategories()]
        for id in ["category_11", "category_a", "category_b"]:
            self.failUnless(id in ids)

    def testGetCategories_2(self):
        """No categories there
        """
        cm = ICategoryManagement(self.product_3)
        self.assertEqual(cm.getCategories(), [])

                                        
def test_suite():
    from unittest import TestSuite, makeSuite
    suite = TestSuite()
    suite.addTest(makeSuite(TestProductCategoryManager))
    return suite
                                               