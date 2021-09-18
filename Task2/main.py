from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time

#If you want the testcases to go slower/faster, please change this number (# of seconds between steps. Suggested: 3)
speed=1


driver = webdriver.Chrome('chromedriver')
driver.get('https://www.dentrix.com/products/eservices/eclaims/payor-search')
time.sleep(5)

def SearchTestCase(value):
    search_box = driver.find_element_by_name('keyword')
    search_box.send_keys(value)
    search_box.submit()
    search_box = driver.find_element_by_name('keyword')
    search_box.send_keys(Keys.CONTROL + "a")
    search_box.send_keys(Keys.DELETE)
    
def WaitBetweenSteps(value):
    time.sleep(value)

def TestCases():

    Testcase_result=[]

    #TestCase 1: Tests the search button and if the url returns the correct keyword that is entered by the user
    #Purpose: If user types in a keyword, due to the current implementation of the search function, the keyword is appended to the url. This test will ensure that the keyword and url argument always match
    def Case1(value):
        SearchTestCase(value)
        url_result=driver.current_url
        url_keyword= url_result.split('?')[-1]
        print("URL result= ",url_result)
        print("URL keyword= ",url_keyword)
        if url_keyword=="keyword="+value:
            Testcase_result.append(f"Passed TestCase 1 with value: {value}")
        else:
            Testcase_result.append(f"Failed TestCase 1 with value: {value}")

    #TestCase 2: Checks if case sensitive keywords returns the same results
    #Purpose: If user types a keyword in upper or lower case, both should yeild the same result
    def Case2(value):
        upper=value.upper()
        lower=value.lower()

        SearchTestCase(upper)
        upper_result=driver.find_element_by_xpath("//td[contains(text(),'"+upper+"')]").text
        print("UpperCase result= ",upper_result)
        SearchTestCase(lower)
        lower_result=driver.find_element_by_xpath("//td[contains(text(),'"+upper+"')]").text
        print("LowerCase result= ",lower_result)
        if upper_result==lower_result:
            Testcase_result.append(f"Passed TestCase 2 with value: {value}")
        else:
            Testcase_result.append(f"Failed TestCase 2 with value: {value}")


    #TestCase 3: Test to check if Special chars return the correct results
    #Purpose: There are some special chars in the payor name that could be used for searching by customers. This test ensures that special characters return the correct result
    #TO Improve: This test case only looks for the first result. Improvements could be done by looking at more/all results
    def Case3(value):
        SearchTestCase(value)
        #gets first result
        case_result= driver.find_element_by_xpath("//table[@id='payorResults']/tbody/tr[2]/td[2]").text
        print("Result= ",case_result)
        
        if value in case_result:
            Testcase_result.append(f"Passed TestCase 3 with value: {value}")
            print("Index of special char: ",case_result.find(value))
        else:
            Testcase_result.append(f"Failed TestCase 3 with value: {value}")
            
    #TestCase 4: Checks if searching for payor id returns the correct results
    #Purpose: The payor id needs to match the result in the table
    #To improve: This test case only looks for the first result. Improvements could be done by looking at more/all results
    def Case4(value):
        SearchTestCase(value)
        payorID_result= driver.find_element_by_xpath("//a[contains(text(),'"+value+"')]").text
        print("Payor ID: ",payorID_result)
        if payorID_result ==value:
            Testcase_result.append(f"Passed TestCase 4 with value: {value}")
        else:
            Testcase_result.append(f"Failed TestCase 4 with value: {value}")
            
    
    #TestCase 1
    Case1("BC")
    WaitBetweenSteps(speed)
    Case1("WA")
    WaitBetweenSteps(speed)
    Case1("001")
    WaitBetweenSteps(speed)
    #TestCase 2
    Case2("ridd")
    WaitBetweenSteps(speed)
    Case2("DDIL")
    WaitBetweenSteps(speed)
    Case2("VT DD")
    WaitBetweenSteps(speed)
    Case2("DD ME")
    WaitBetweenSteps(speed)
    #TestCase 3
    Case3("(")
    WaitBetweenSteps(speed)
    Case3(")")
    WaitBetweenSteps(speed)
    Case3("*")
    WaitBetweenSteps(speed)
    Case3("/")
    WaitBetweenSteps(speed)
    Case3("-")
    WaitBetweenSteps(speed)
    Case3(",")
    WaitBetweenSteps(speed)
    #TestCase 4
    Case4("00580")
    WaitBetweenSteps(speed)
    Case4("47009")
    WaitBetweenSteps(speed)
    Case4("ARGUS")
    WaitBetweenSteps(speed)

    #prints all the testcase results. 
    #To Improve: Need to count how many test cases passed or failed and show that to user in a formatted output
    #To Improve: Could implement error expection catching with a try catch.
    print(Testcase_result)


#main function that is called
TestCases()

time.sleep(10)
driver.quit()