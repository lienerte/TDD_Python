'''
Created on Jun 28, 2016

@author: el25453
'''
from amazonproduct import API
from amazon.api import AmazonAPI

api = API(locale='us')

KEY = ""
SECRET_KEY = ""
ACCESS_ID = ""

#Needs to fetch the value
amazon = AmazonAPI(KEY, SECRET_KEY, ACCESS_ID)

#url = "http://webservices.amazon.com/onca/xml? Service=AWSECommerceService& AWSAccessKeyId=[AKIAJZNK5MS4LOJN4LBQ]& AssociateTag=[lienerte-20]& Operation=ItemSearch& Keywords=the%20hunger%20games& SearchIndex=Books &Timestamp=[YYYY-MM-DDThh:mm:ssZ] &Signature=[<oQMHJML0pWoaU9hwb90AJzpCzYzHrBPEi0gdWDnV>]"
print amazon.lookup(ItemId = "B00KC6I06S").title
products = amazon.search(Keywords = "007: The Roger Moore Collection - Vol 1 (DVD)", SearchIndex = "All")
for i, product in enumerate(products):
    print "{0}. '{1}'".format(i, product.title)
    print product.price_and_currency
#items = api.item_search('Books', Publisher = "O'Reilly")
#print items

# get all books from result set and
# print author and title
#for book in api.item_search('Books', Publisher='Galileo Press'):
 #   print '%s: "%s"' % (book.ItemAttributes.Author,
  #                      book.ItemAttributes.Title)