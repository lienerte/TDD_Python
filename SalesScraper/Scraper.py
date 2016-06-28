'''
Created on Jun 28, 2016

@author: el25453
'''
import json
import pprint
import urllib2
import unittest

KEY = ""

class TestDriver():
    
    def __init__(self):
        pass
    
    def getsURL(self):
        url = "https://api.bestbuy.com/v1/products(onSale=true)?apiKey=" + KEY + "&callback=JSON_CALLBACK&format=json"
        myFile = urllib2.urlopen(url)
        assert myFile != None
        
    def convertsToDict(self):
        url = "https://api.bestbuy.com/v1/products(onSale=true)?apiKey=" + KEY + "&callback=JSON_CALLBACK&format=json"
        myFile = urllib2.urlopen(url)
        jsonFile = myFile.read()
        #Formats the json by stripping non JSON elements
        jsonFile = jsonFile[14:] #JSON_CALLBACK(
        jsonFile = jsonFile[:-1] #)
        listJson = json.loads(jsonFile)
        assert isinstance(listJson, dict)
        
    def runTests(self):
        self.getsURL()
        self.convertsToDict()
        print("Everything passed")


#thisTest = TestDriver()
#thisTest.runTests()

url = "https://api.bestbuy.com/v1/products(onSale=true)?apiKey=" + KEY + "&callback=JSON_CALLBACK&format=json"
myFile = urllib2.urlopen(url)
jsonFile = myFile.read()
jsonFile = jsonFile[14:] #JSON_CALLBACK(
jsonFile = jsonFile[:-1] #)
listJson = json.loads(jsonFile)
#pprint.pprint(listJson["products"])
products = listJson["products"]
for item in products:
    print(item["name"] + " : " + str(item["salePrice"]))
    
