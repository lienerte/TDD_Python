# -*- coding:utf-8 -*-
'''
Created on Jun 28, 2016
@author: el25453
'''
import sys
import locale
import pprint
from time import sleep
import re
import string
from TablePrinter import printTable, commaSeperator
import sys
import os
import datetime
import time
from BestBuyPortion import filterNonAscii, AccessBestBuy
from fuzzywuzzy import fuzz
from SchedulerMain import scheduleAMethod
from amazonproduct.contrib.cart import Item
try:
    from apscheduler.schedulers.blocking import BlockingScheduler
except:
    os.system("pip install apscheduler")
    from apscheduler.schedulers.blocking import BlockingScheduler
try:
    from EmailFunction import sendEmail
except:
    quickMake = open(("output" + datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d') + ".csv"), "w")
    from EmailFunction import sendEmail
    quickMake.close()


#to get 
try:
    from amazonproduct import API, errors
    from amazon.api import AmazonAPI
    from amazonproduct.errors import AWSError
    import win32com.client
    from win32com.client import Dispatch
except:
    os.system('pip install python-amazon-product-api')
    os.system('pip install python-amazon-simple-product-api')
    from amazonproduct import API, errors
    from amazon.api import AmazonAPI
    from amazonproduct.errors import AWSError
 

class TestDriver():
    
    def __init__(self):
        self.requestor = AmazonRequestor()
        self.bestbuy = AccessBestBuy()
    
    def testConnectsToAmazon(self):
        try:
            self.requestor.amazon.search_n(1, Keywords = "Disney", SearchIndex = "All")
        except:
            print "Enter correct API keys"
            sys.exit()
            
    def testSearchComplete(self):
        thisList = []
        self.requestor.checkAmazon("Disney", 8.99, thisList)
        assert len(thisList) != 0
    
    def testBestBuy(self):
        products = self.bestbuy.getSalesIntoDictionary(1,1)[0]
        assert len(products) != 0
        
    def testAll(self):
        self.testConnectsToAmazon()
        self.testSearchComplete()
        self.testBestBuy()
        print "KEYS"
        print self.requestor.KEY, self.requestor.SECRET_KEY, self.requestor.ACCESS_ID
        print "Everything passed"
        print ""

class FuzzyWuzzyError(Exception):
    def __init__(self, *args, **kwargs):
        Exception.__init__(self,*args,**kwargs)
        
    def toString(self):
        "FuzzyWuzzyError"
    
class AmazonRequestor():
    
    def __init__(self):
        self.api = API(locale='us')
        thisList = []
        with open ("AmazonConfig.txt" , "r") as lines:
            for line in lines:
                line = line.replace("\n", "")
                thisList.append(line)
        self.KEY = str(thisList[0])
        self.SECRET_KEY = str(thisList[1])
        self.ACCESS_ID = str(thisList[2])
        self.amazon = AmazonAPI(self.KEY, self.SECRET_KEY, self.ACCESS_ID)
    
    def checkAmazon(self, productName, productPrice, thisList):
        """
        @param productName: the name of the product being queried 
        @param productPrice: the price of the product being queried ($)
        @param thisList: the list in which product information is stored
        Checks Amazon for a given product with a given price and appends information to the supplied list
        """
        try:
            products = self.amazon.search_n(1, Keywords = productName, SearchIndex = "All")
            for amazonP in products:
                if (amazonP.price_and_currency[0] == None):
                    difference = "-9999"
                else:
                    difference = float(amazonP.price_and_currency[0]) - productPrice
                thisList.append([str(difference), productName, str(productPrice), amazonP.title, str(amazonP.price_and_currency[0])])
        except:
            print "No match found on Amazon.com for : " + productName
    
    def searchAmazon(self, bestBuyProducts, thisList, current_page):
        """
        @param bestBuyProducts: a list of BestBuy products via BestBuyPortion.getSalesIntoDictionary(PAGE_SIZE, PAGE_NUMBER)
        @param thisList: the list in which bestBuyProducts and Amazon query information are stored
        @param current_page: the current_page of the BestBuy URL
        @warning: -9999 in difference field indicates that Aamzon was unable to fetch the price, usually means the product is cheap and vendor does not want Amazon to show that
        @This function is the backbone of this project.  Retrieves information from BestBuy and then searches Amazon for the same item and prints associated information as follows:
            1. Prints each item that is being check and the parameters from BestBuy
            2. Prints any associated errors(will usually be an Amazon Search Error where Amazon is unable to find the item)
            3. Prints amount of time taken
            4. Prints Errors in relatively good format
            5. Lastly, if out of API calls will send a unique error and quit the program and send and Email
        """
        consecutiveErrors = 0;
        errorList = []
        initialTime = time.clock()
        countErrors = 0
        #manualInput = raw_input("Do you want to specify new search phrases? Y or N : ") uncomment if want to add functionality 
        manualInput = "F"
        #appends header to start of file
        if (not os.path.isfile("output" + datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d') + ".csv")):
            thisList.append(["DIFFERENCE", "MODEL_NUMBER", "UPC", "BESTBUY_NAME", "BESTBUY_PRICE", "AMAZON_NAME", "AMAZON_PRICE", "MANUFACTURER", "RISKY?"])
            
        for product in bestBuyProducts:
            #Tests if out of API calls
            if consecutiveErrors == 15:
                errorFile = open("APIEmail.txt", "w")
                errorFile.write("Ran out of API Calls : Ended on Page " + current_page)
                errorFile.close()
                print "You have run out of Amazon or BestBuy API calls for today on page : " + current_page
                sendEmail()
                sys.exit()
            pprint.pprint(product)
            modelNumber = str(product.split(" : " )[0])
            upc = str(product.split(" : " )[1])
            productPrice = float(product.split(" : " )[2])
            productName = str(product.split(" : " )[3])
            manufacturer = str(product.split(" : " )[4])
            bestSellingRank = str(product.split(" : " )[5])
            customerReviewNumber = str(product.split(" : " )[6])
            customerReviewAverage = str(product.split(" : " )[7])
            #Attempts to search Amazon via the modelNumber and manufacturer and then makes sure the resulting item 's name is relevant 
            try:
                print upc 
                theseItems = self.amazon.search_n(1, Keywords = upc, SearchIndex = "All", Condition = "New", MerchantID = "Amazon")
                for item in theseItems:
                    if (item.price_and_currency[0] == None):
                        #difference = float(item.list_price[0]) - float(productPrice)
                        difference = -9999
                    else:
                        difference = float(item.price_and_currency[0]) - float(productPrice)
                        
    
                    if fuzz.ratio(productName, filterNonAscii(item.title)) >= 40:
                        if (item.price_and_currency[0] != None):
                            thisList.append([str(difference), modelNumber, upc, productName, str(productPrice), filterNonAscii(item.title), str(item.price_and_currency[0]), manufacturer, "0"])
                        else:
                            thisList.append([str(difference), modelNumber, upc, productName, str(productPrice), filterNonAscii(item.title), str(item.list_price[0]), manufacturer, "1"])
                        consecutiveErrors = 0
                    else:
                        firstItemName = filterNonAscii(item.title)
                        raise Exception("FuzzyWuzzyError")
            except:
                sleep(1.1)
                #If modelNumber fails, then uses UPC (barcode) and manufacturer   
                  
                try:
                    print modelNumber 
                    theseItems = self.amazon.search_n(1, Keywords = modelNumber, SearchIndex = "All", Condition = "New", MerchantID = "Amazon")
                    for item in theseItems:
                        if (item.price_and_currency[0] == None):
                            #difference = float(item.list_price[0]) - float(productPrice)
                            difference = -9999
                        else:
                            difference = float(item.price_and_currency[0]) - float(productPrice)
                            
                            
                    if ((fuzz.ratio(productName, filterNonAscii(item.title)) >= 40) or (fuzz.ratio(filterNonAscii(item.title), firstItemName)) >= 80):
                        if (item.price_and_currency[0] != None):
                            thisList.append([str(difference), modelNumber, upc, productName, str(productPrice), filterNonAscii(item.title), str(item.price_and_currency[0]), manufacturer, "0"])
                        else:
                            thisList.append([str(difference), modelNumber, upc, productName, str(productPrice), filterNonAscii(item.title), str(item.list_price[0]), manufacturer, "1"])
                        consecutiveErrors = 0
                    else:
                        raise Exception("FuzzyWuzzyError")
                
                except:        
                    sleep(1.1) 
                    try:
                        print upc + " " + manufacturer
                        theseItems = self.amazon.search_n(1, Keywords = upc + " " + manufacturer, SearchIndex = "All", Condition = "New", MerchantID = "Amazon")
                        for item in theseItems:
                            if (item.price_and_currency[0] == None):
                                #difference = float(item.list_price[0]) - float(productPrice)
                                difference = -9999
                            else:
                                difference = float(item.price_and_currency[0]) - float(productPrice)
                                
                            
                            if fuzz.ratio(productName, filterNonAscii(item.title)) >= 40:
                                if (item.price_and_currency[0] != None):
                                    thisList.append([str(difference), modelNumber, upc, productName, str(productPrice), filterNonAscii(item.title), str(item.price_and_currency[0]), manufacturer, "0"])
                                else:
                                    thisList.append([str(difference), modelNumber, upc, productName, str(productPrice), filterNonAscii(item.title), str(item.list_price[0]), manufacturer, "1"])
                                consecutiveErrors = 0
                            else:
                                firstItemName = filterNonAscii(item.title)
                                raise Exception("FuzzyWuzzyError")
                    except:
                        sleep(1.1)
                        try:
                            print modelNumber + " " + manufacturer
                            theseItems = self.amazon.search_n(1, Keywords = modelNumber + " " + manufacturer, SearchIndex = "All", Condition = "New", MerchantID = "Amazon")
                            for item in theseItems:
                                if (item.price_and_currency[0] == None):
                                    #difference = float(item.list_price[0]) - float(productPrice)
                                    difference = -9999
                                else:
                                    difference = float(item.price_and_currency[0]) - float(productPrice)
                                    
                            
                            if ((fuzz.ratio(productName, filterNonAscii(item.title)) >= 40) or (fuzz.ratio(filterNonAscii(item.title), firstItemName)) >= 80):
                                if (item.price_and_currency[0] != None):
                                    thisList.append([str(difference), modelNumber, upc, productName, str(productPrice), filterNonAscii(item.title), str(item.price_and_currency[0]), manufacturer, "0"])
                                else:
                                    thisList.append([str(difference), modelNumber, upc, productName, str(productPrice), filterNonAscii(item.title), str(item.list_price[0]), manufacturer, "1"])
                                consecutiveErrors = 0
                            else:
                                raise Exception("FuzzyWuzzyError")
                        except:
                            sleep(1.1)
                            print productName
                            try:
                                theseItems = self.amazon.search_n(1, Keywords = productName, SearchIndex = "All", Condition = "New", MerchantID = "Amazon")
                                for item in theseItems:
                                    if (item.price_and_currency[0] == None):
                                        #difference = float(item.list_price[0]) - float(productPrice)
                                        difference = -9999
                                    else:
                                        difference = float(item.price_and_currency[0]) - float(productPrice)
                                        
                                
                                if ((fuzz.ratio(productName, filterNonAscii(item.title)) >= 40) or (fuzz.ratio(filterNonAscii(item.title), firstItemName)) >= 80):
                                    if (item.price_and_currency[0] != None):
                                        thisList.append([str(difference), modelNumber, upc, productName, str(productPrice), filterNonAscii(item.title), str(item.price_and_currency[0]), manufacturer, "1"])
                                    else:
                                        thisList.append([str(difference), modelNumber, upc, productName, str(productPrice), filterNonAscii(item.title), str(item.list_price[0]), manufacturer, "1"])
                                    consecutiveErrors = 0
                                else:
                                    raise Exception("FuzzyWuzzyError")
                            
                            except:
                                sleep(1.1)
                                splitName = productName.split(" ")
                                trimmedName = " ".join(splitName[:len(splitName)/2])
                                print trimmedName
                                try:
                                    theseItems = self.amazon.search_n(1, Keywords = trimmedName, SearchIndex = "All", Condition = "New", MerchantID = "Amazon")
                                    for item in theseItems:
                                        if (item.price_and_currency[0] == None):
                                            #difference = float(item.list_price[0]) - float(productPrice)
                                            difference = -9999
                                        else:
                                            difference = float(item.price_and_currency[0]) - float(productPrice)
                                            
                                    if ((fuzz.ratio(productName, filterNonAscii(item.title)) >= 40) or (fuzz.ratio(filterNonAscii(item.title), firstItemName)) >= 80):
                                        if (item.price_and_currency[0] != None):
                                            thisList.append([str(difference), modelNumber, upc, productName, str(productPrice), filterNonAscii(item.title), str(item.price_and_currency[0]), manufacturer, "1"])
                                        else:
                                            thisList.append([str(difference), modelNumber, upc, productName, str(productPrice), filterNonAscii(item.title), str(item.list_price[0]), manufacturer, "1"])
                                        consecutiveErrors = 0
                                    else:
                                        raise Exception("FuzzyWuzzyError")
            
                        #Tracks the error
                                except Exception as error:
                                    print ("------------------------------------------" + modelNumber + " : " + upc + " : " + productName + " did not have a match on Amazon.com " + repr(error) + "------------------------------------------")
                                    countErrors = countErrors + 1
                                    consecutiveErrors = consecutiveErrors + 1
                                    errorList.append([modelNumber + " : " + upc + " : " + productName + " : " + repr(error)])
                                    if manualInput.lower() == "y" or manualInput.lower() == "yes":
                                        newName = raw_input("Try removing some of the words from the string to search with a new term : ")
                                        self.checkAmazon(newName, productPrice, thisList)
            sleep(1.1)
            print ""
                
                    
        print ""
        print "ERRORS : " + str(countErrors)
        finalTime = time.clock()
        print "Searching for these 100 BestBuy products on Amazon took : " + str(finalTime - initialTime)
        print ""
        printTable(sys.stdout, errorList)
        
    def filterBlackList(self, inputList):
        blackListed = ["Beats by Dr. Dre", "Apple", "Bose", "NETGEAR"]
        filtered = []
        for item in inputList:
            if item[7] in blackListed:
                print "REMOVED", item
            else:
                filtered.append(item)
        print ""
        return filtered
    
    
    def fullExecute(self, doAllPages, PAGE_SIZE, WHICH_PAGE):
        """
        @param doAllPages - Pass in True or False (boolean) which tells the program to either test print one page or all of them usually will be True
        @param PAGE_SIZE - can range from 1 - 100 inclusive and tells BestBuy how many items are on each page of search results
        @This method ties together all the various python files to achieve the end goal: comparing Amazon to BestBuy and built-in error-handling
        """
        print ""    
        tester = TestDriver()
        tester.testAll()
        total_page = 2
        #Iterates for all pages
        if doAllPages:
            while WHICH_PAGE <= total_page:
                allItems = AccessBestBuy().getSalesIntoDictionary(PAGE_SIZE, str(WHICH_PAGE))
                saleProducts = allItems[0]
                WHICH_PAGE = allItems[1]
                total_page = allItems[2]
                print ""
                thisList = []
                aRequestor = AmazonRequestor()
                aRequestor.searchAmazon(saleProducts, thisList, WHICH_PAGE)
                print ""
                bestList = self.filterBlackList(thisList)
                printTable(sys.stdout, bestList)
                try:
                    fileName = commaSeperator("output", bestList)
                except IOError:
                    Dispatch("Excel.Application").Quit()
                    fileName = commaSeperator("output", bestList)
        #Just does the first page
        else:
            allItems = AccessBestBuy().getSalesIntoDictionary(PAGE_SIZE, str(WHICH_PAGE))
            WHICH_PAGE = allItems[1]
            saleProducts = allItems[0]
            print ""
            thisList = []
            aRequestor = AmazonRequestor()
            aRequestor.searchAmazon(saleProducts, thisList, WHICH_PAGE)
            print ""
            bestList = self.filterBlackList(thisList)
            printTable(sys.stdout, bestList)
            try:
                fileName = commaSeperator("output", bestList)
            except IOError:
                Dispatch("Excel.Application").Quit()
                fileName = commaSeperator("output", bestList)

if __name__ == "__main__":
    timeStamp = datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d : %H:%M:%S')
    print "It is now : " + timeStamp
    difference = datetime.timedelta(seconds = 0)
    runTime = datetime.datetime.fromtimestamp(time.time()) + difference
    print "Program will begin in 0 seconds"
    aRequestor = AmazonRequestor()
    scheduleAMethod(aRequestor.fullExecute, runTime, (False, 100, 1))
    dayDifference = datetime.timedelta(days = 1)
    print "Next run time will be at : " + str(runTime + dayDifference)
        
