from __future__ import print_function
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, TimeoutException
import sys
import itertools
from string import printable
import time
import boto3
import json
import decimal
from boto3.dynamodb.conditions import Key, Attr


#Get data is supposed to pull data from dynamodb users TO DO!!
def getdata():
    #dynamodb = boto3.resource('dynamodb', region_name='us-west-2', endpoint_url="https://n3zle2fjz8.execute-api.us-west-2.amazonaws.com/prod/Answers")
    #table = dynamodb.Table('CUSTOMER_LIST')
    #ky = Key('CUSTOMER_ID').begins_with("us")

    #response = table.scan(FilterExpression=ky)
    response ='{"cusInfo": {"yearsofexperience": "5", "Lname": "Lumberjack", "noncompete": "No", "Fname": "Geeky", "timezone": "Central", "education": [{"yearsincollege": "1", "collegename": "Western", "collegemajor": "Software Development", "gpa": "3"}], "createdAt": "1546017247342L", "city": "Nashville", "desiredsalary": "90000", "veteran": "Yes", "desiredjob": ["Software Engineer"], "state": "TN", "relocate": "Yes", "desiredlocation": ["Austin, TX"], "startdate": "ASAP", "govemployee": "NO", "address": "1204 Royal Crest Dr", "unique": "Vegan", "certifications": ["SEC +"], "hearaboutus": "I made it", "gender": "male", "phonenum": "5125521027", "relevantwebsites": ["OverApply.com"], "experience": [{"jobreponsibilities": "Design,build,market,create OverApply", "startDate": "Nov 2017", "endDate": "Still Working", "jobtitle": "CEO/Founder"}], "skills": [{"Title":"Talking","Years": "5"}], "prefcontact": "email", "race": "Caucsian/White", "uscitizen": "Yes", "sponsorship":"No", "applicationcontact": "Yes", "drugtest": "Yes"}, "CUSTOMER_ID": "ID"}'
    data = json.loads(response)
    return data
    

jobsites = ["indeed.com", "monster.com", "ziprecruiter.com", "linkedin.com"]
manapp = []
tofillout = ["Phone", "experience", "Are you in", "education", "relocate", "sponsorship", "authorized to work"]
driver = webdriver.Chrome('C:\Python27\chromedriver.exe')
def indeedlogin(url):
    loginurl = "https://secure.indeed.com/account/login?service=my&hl=en_US&co=US"
    driver.get(loginurl)
    while newpag(url) == False:
        time.sleep(1)
    nnurl = driver.current_url
    namefield = driver.find_element_by_id("login-email-input")
    passfield = driver.find_element_by_id("login-password-input")
    subbutton = driver.find_element_by_id("login-submit-button")
    namefield.send_keys("John")
    passfield.send_keys("Doe")
    subbutton.click()
    while newpag(nnurl) == False:
        time.sleep(1)
    driver.get(url)


#creating the proper url sequence for linkedin, ziprecruiter, and indeed
def linzipwhat(what):
   #print(what)
    newquery = ""
    tempwh = what.split(" ")
    
    for wh in tempwh:
        if wh.index > len(tempwh):
            newquery = newquery + wh + "+"
        else:
            newquery = newquery + wh
    return newquery

def linzipwhere(where):
    #print(where)
    newquery = ""
    tempwh = where.split(",")
    #print(tempwh)
    for wh in tempwh:
        if wh.index > len(tempwh):
            newquery = newquery + wh.strip() + "+"
        else:
            newquery = newquery + wh.strip()
    return newquery

#creating the proper url sequence for monster

def monsterwhat(what):
    #print(what)
    newquery = ""
    tempwh = what.split(" ")
    #print(tempwh)
    for wh in tempwh:
                newquery = newquery + wh + "-"
    return newquery

def monsterwhere(where):
    #print(where)
    newquery = ""
    tempwh = where.split(",")
    #print(tempwh)
    for wh in tempwh:
        if tempwh.index(wh) < len(tempwh) - 2:
                newquery = newquery + wh.strip() + "-"
        elif tempwh.index(wh) < len(tempwh) - 1:
            newquery = newquery + wh.strip() + "__2C-"
        else:
            newquery = newquery + wh.strip()
    return newquery

def parenttext(weblist, location):
    try:
        patext = weblist[location].text
        chi = weblist[location].find_elements_by_xpath("/descendant::*")
        for ch in chi:
            patext.replace(ch.text, "")
        #print(patext)
        return patext
    except:
        print("parenttext failed")


#function to configure url based on websites url configuration and return the new url
def consite(site, what, where):

    if "indeed" in site:
        return "https://www.indeed.com/jobs?q=" + linzipwhat(what) + "&l=" + linzipwhere(where) + "&start=0"
    if "monster" in site:
        return "https://www.monster.com/jobs/search/?q=" + monsterwhat(what) + "&where=" + monsterwhere(where)
    if "ziprecruiter" in site:
        return "https://www.ziprecruiter.com/candidate/search?search=" + linzipwhat(what) + "&location=" + linzipwhere(where)
    if "linkedin" in site:
        return "https://www.linkedin.com/jobs/search?keywords=" + linzipwhat(what) + "&location=" + linzipwhere(where) + "&start=0"

#function to determine if page has changed, not sure if it actually helps.
def newpag(oldurl):
    if oldurl in driver.current_url:
        return False
    else:
        return True

#function to configure url and navigate to url and return url for use in other functions
def gnjob(what, where):
    url = consite(s,what,where)
    print(url)
    oldurl = driver.current_url
    driver.get(url) 
    while newpag(oldurl) == False:
        time.sleep(1)
    return url
     
#function to take previous start position off of url	 
def confurl(url, coun):
    xurl = url[:-1]#len(str(coun)) * 
    return xurl
    
#function to add new start position to url	
def newurl(url, coun):
	return url + str(coun)

def switchtotab(tab):
    whandles = driver.window_handles
    driver.switch_to_window(whandles[tab])

def closetab(tab):
    whandles = driver.window_handles
    switchtotab(tab)
    driver.close()

def clickapplybutton(innertext):
    try:
        tempeles = driver.find_elements_by_tag_name("button")
        for inner in innertext:
            for tempele in tempeles:
                #print(tempele.get_attribute("innerText").encode("utf-8"))
                if tempele.get_attribute("innerText").startswith(innertext):
                    tempeles[tempeles.index(tempele)].click()
                    return "Found and clicked"

    except:
        print("first break")
    try:    
        print("in try 2")
        tempeles = driver.find_elements_by_xpath("//a")
        print("got past the tempeles")
        for tempele in tempeles:
        # print(tempele.get_attribute("innerText").encode("utf-8"))
            if tempele.get_attribute("innerText").startswith(innertext):
                try:
                    print("bout to clikc")
                    tempeles[tempeles.index(tempele)].click()
                    print("clicked")
                    return "Found and clicked"
                except:
                    pass
    except:
        print("second break")
        return "Not found"

def formelement(findtext):
    fi = driver.find_elements_by_xpath("form[1]/descendant::*")
    spot = 0
    while spot < len(fi):
        if fi[spot].get_attribute("innerText") is not None:
            if findtext in fi[spot].get_attribute("innerText"):
                if findtext not in fi[spot + 1].get_attribute("innerText"):
                    spot1 = spot
                    #while spot1 < len(fi):
                    #    if "INUPT" in fi[spot1 + 1].tag_name:
                    return spot1
                    #    spot1 = spot1 + 1
            spot = spot + 1
            return "Not found"

def findelement(weblist, findtext):
    fi = driver.find_elements_by_xpath("html/descendant::*")
    spot = 0
    fiit = False
    #while spot < len(fi):
    for f in fi:
        if f.get_attribute("innerText") is not None:
            #print(f.get_attribute("innerText").encode("utf-8"))
            if findtext in f.get_attribute("innerText"):
                print(f.get_attribute("innerText"))
                fiit = True
            if fiit == True:
                if findtext not in f.get_attribute("innerText"):
                    return fi.index(f) - 1
            spot = spot + 1
    return "Not found"

def findtag(tag, innertext):
    spot = 0
    tempeles = driver.find_elements_by_xpath("//" + tag)
    while spot < len(tempeles):
        if tempeles[spot].get_attribute("innerText") is not None:
            if innertext in tempeles[spot].get_attribute("innerText"):
                return spot
            spot = spot + 1
    return "Not found"

def fillanswers(weblist, olocation, ques):
    if ques is "Phone":
        return usda["cusInfo"]["phonenum"]
    elif ques is "experience":
        exty = webslist[olocation].get_attribute("innerText")
        skili = usda["cusInfo"]["skills"]
        for ski in skili:
            if ski["Title"] in exty:
                return ski["Years"]
        return "0"
    elif ques is "Are you in":
        return usda["cusInfo"]["city"] + "," + usda["cusInfo"]["state"]
    elif ques is "education":
        return usda["cusInfo"]["education"]
    elif ques is "relocate":
        return usda["cusInfo"]["relocate"]
    elif ques is "sponsorship":
        return usda["cusInfo"]["sponsorship"]

def fillininput(weblist, location, olocation, tofill):
    try:
        answ = fillanswers(weblist, olocation, tofill)
        print(answ)
    except:
        print("fillanswers failed")
    try:
        weblist[location].send_keys(answ)
    except:
        print("fillininput send keys failed")

def fillinselect(weblist, location, olocation, tofill):
    try:
        answ = fillanswers(weblist, olocation, tofill)
    except:
        print("fillinselect answ failed")
    try:
        while "option" in weblist[location].tag_name:
            if answ in weblist[location]:
                weblist[location].click()
            location = location + 1
    except:
        print("fillinselect selecting answer failed")

def fillinradio(weblist, location, olocation, tofill):
    try:
        answ = fillanswers(weblist, olocation, tofill)
    except:
        print("fillinradio answ failed")
    try:
        parent = driver.find_elements_by_xpath("input[type='radio']/..")
        radio = driver.find_elements_by_xpath("input[type='radio']")
        for par in parent:
            if tofill in par.get_attribute("innerText"):
                radio[parent.index(par)].click()
    except:
        print("fillinradio selecting radio button failed")

def highlight(element):
    """Highlights (blinks) a Selenium Webdriver element"""
    driver = element._parent
    def apply_style(s):
        driver.execute_script("arguments[0].setAttribute('style', arguments[1]);",
                              element, s)
    original_style = element.get_attribute('style')
    apply_style("background: yellow; border: 2px solid red;")
    time.sleep(.3)
    apply_style(original_style)

def filloutform():
    print("in filloutform")
    try:
    
        fin = driver.find_element_by_xpath("//form")
        fi = fin.find_elements_by_xpath("./descendant::*")
        
    except:
        print("filloutform fi failed")
    spot = 0
    #print(fi.get_attribute("innerText"))
    #print(driver.find_element_by_id("label-input-applicant.phoneNumber").get_attribute("innerText"))
    breakit = False
    while spot < len(fi):
        #print('1')
        #print(fi[spot].tag_name)
        #highlight(fi[spot])
        if fi[spot].get_attribute("innerText") is not None:
            #print('2')
            for fill in tofillout:
                #print(fi[spot].get_attribute("innerText"))
                if fill in fi[spot].get_attribute("innerText"):
                    #print('3')
                    if fill in parenttext(fi, spot):
                        #print('4')
                        if fill not in fi[spot + 1].get_attribute("innerText"):
                            #print('5')
                            spot1 = spot
                            while spot1 < len(fi):
                                #print('6')
                                if "input" in fi[spot1].tag_name:
                                    print('7')
                                    if "radio" in fi[spot1].get_attribute("type"):
                                        try:
                                            fillinradio(fi, spot1, spot, fill)
                                        except:
                                            print("fillinradio failed")
                                    else:
                                        try:
                                            if fi[spot1].get_attribute('value') is None:
                                                fillininput(fi, spot1, spot, fill)
                                        except:
                                            print("fillininput failed")
                                    breakit = True
                                    break
                                elif "select" in fi[spot1].tag_name:
                                    print('9')
                                    try:
                                        fillinselect(fi, spot1, spot, fill)
                                    except:
                                        print("fillinselect failed")
                                    breakit = True
                                    break
                                spot1 = spot1 + 1
        if breakit == True:
            breakit = False
            break
        spot = spot + 1
                #return "Not found"

def triagepage():
    try:
        pggg = driver.find_element_by_tag_name("body").get_attribute("innerHTML")
    except:
        print("getting body content failed")
    #print(pg.get_attribute("innerText"))
    if "Apply" in pggg:
        if "upload" not in pggg:
            return "Startpage"
    elif "Password" in pggg:
        return "Loginpage"
    elif "upload your resume" and "Next" in pggg:
        return "resume page"
    elif "Upload Resume" and "Submit":
        "single page application" 
    else:
        return "Finished applying"


def handlepage(stage):
    if "Startpage" in stage:
        try:
            appoption = ["Apply", "APPLY"]
            for app in appoption:
                tapp = clickapplybutton(app)
                #print(tapp)
                if "Found and clicked" in tapp:
                    return "Finished Startpage"
        except:
            return "clicking apply in startpage failed"
    elif "Loginpage" in stage:
        chkiframe = ""
        try:
            chkiframe = driver.find_elements_by_tag_name("iframe")
            return "Loginpage has iframe."
        except:
            pass
        return "handling login"
    elif "single page application" in stage:
        return "filled out form"
    else:
        return "page not handled."

def indeedeasyapply(weblist, findtext):
    print("easy apply")
    orl = driver.current_url
    time.sleep(5)
    weblist.find_element_by_xpath("a").click()
    switchtotab(1)
    #while newpag(orl) == False:
    time.sleep(5)
    finbut = findtag("button", "Apply Now")
    #print(finbut)
    elelist = driver.find_elements_by_tag_name("button")
    #print(len(elelist))
    try:
        elelist[finbut].click()
    except:
        print("click apply button failed")
    try:
        time.sleep(20)
        findframe = driver.find_elements_by_tag_name("iframe")
        if len(findframe) > 1:
            ifframe = driver.find_element_by_id("indeedapply-modal-preload-iframe")
            driver.switch_to_frame(ifframe)
        else:
            ifframe = driver.find_element_by_tag_name("iframe")
            driver.switch_to_frame(ifframe)
    except:
        print("Iframe failed")
    try:
        time.sleep(20)
        ifframe = driver.find_element_by_tag_name("iframe")
        driver.switch_to_frame(ifframe)
    except:
        print("Iframe2 failed")
    try:
        fi = driver.find_element_by_id("ia_success")
        driver.switch_to_default_content()
        closetab(1)
        switchtotab(0)
        return "already applied"
    except:
        pass
    continuebutton = driver.find_element_by_xpath("html")
    while "Continue" in continuebutton.text:
        if "required" in continuebutton.text:
            driver.switch_to_default_content()
            closetab(1)
            switchtotab(0)
            print("question unable to be answered.")
            break
        print("about to filloutform")
        try:
            filloutform()
        except:
            print("filloutform failed")
        try:
            #finbut = findtag("button", "Continue")
            elelist = driver.find_elements_by_tag_name("button")
            breakit = False
            for ele in elelist:
                if ele.get_attribute("innerText") is not None:
                    if ele.get_attribute("innerText").startswith("Continue"):
                        ele.click()
                        breakit = True
                        break
                if breakit == True:
                    breakit = False
                    break
        except:
            print("clicking continue failed")
        continuebutton = driver.find_element_by_xpath("html")
    if "Apply" in continuebutton.text:
        #print(continuebutton.text)
        try:
            roboblocker = driver.find_element_by_tag_name("iframe")
            driver.switch_to_default_content()
            closetab(1)
            switchtotab(0)
            return "CAPTCHA protected"
            time.sleep(2)
        except:
            pass
        try:
            elelist = driver.find_elements_by_tag_name("button")
            for ele in elelist:
                if ele.get_attribute("innerText") is not None:
                    if ele.get_attribute("innerText").startswith("Apply"):
                        ele.click()
                        break
        except:
            print("clicking apply failed")

#def cliklink(component):
 #   if "<a>" in component.get_attribute("innerHTML")
def sortjobs(url):
    print(url)
    if "indeed" in url:
        #indeedlogin(url)
        while newpag(url) == False:
            time.sleep(3)
        #find and close popup for indeed
        try:
            popup = driver.find_element_by_id("popover-close-link")
            #popup.click()
            driver.refresh()
        except NoSuchElementException:
            pass
    
        totjob = driver.find_element_by_id("searchCount").get_attribute("textContent")
        if "," in totjob:
            totjob = totjob.split(",")
            numjob = int(totjob[0][-1] * 1000) + int(totjob[1][0:2])
        curcount = 0
        while curcount < numjob:
            try:
                popup = driver.find_element_by_id("popover-close-link")
                driver.refresh()
            except NoSuchElementException:
                pass
            avajobs = driver.find_elements_by_xpath("//*[@class='jobsearch-SerpJobCard row result clickcard']")
            print(len(avajobs))
            aurl = str(confurl(url, curcount))
            for ava in avajobs:
                numero = avajobs.index(ava)
                try:
                    if "Easily apply" in ava.get_attribute("innerText"):
                        try:
                            itx = []
                            #print(indeedeasyapply(ava, "Apply Now"))
                        except:
                            print("easy 1 skiped")
                    elif "Apply easily with Indeed" in ava.get_attribute("innerText"):
                        try:
                            itx = []
                            #print(indeedeasyapply(ava, "Apply Now"))
                        except:
                            print("easy 2 skiped")
                    elif "Apply with your Indeed Resume" in ava.get_attribute("innerText"):
                        try:
                            itx = []
                            #print(indeedeasyapply(ava, "Apply Now"))
                        except:
                            print("easy 3 skiped")
                    else:
                        try:
                            applink = ava.find_element_by_tag_name("a")
                            applink.click()
                        except:
                            print("click applink failed")
                        time.sleep(3)
                        switchtotab(1)
                        if "primejobs.indeed" in driver.current_url:
                            closetab(1)
                            switchtotab(0)
                        else:
                            try:
                                driver.set_page_load_timeout(15)                            
                                clickapplybutton("Apply Now")
                            except:
                                driver.refresh()
                            time.sleep(5)
                            if driver.title == "Untitled":
                                driver.refresh()
                            switchtotab(0)
                            wh = driver.window_handles
                            if len(wh) < 3:
                                closetab(1)
                                switchtotab(0)
                            #print("after click")
                            while newpag(aurl) == False:
                                time.sleep(1)
                            switchtotab(2)
                            print(driver.current_url)
                            manapp.append(driver.current_url)
                            triaged = ""
                            while "Finished applying" not in triaged:
                                try:
                                    triaged = triagepage()
                                    print(triaged)
                                except:
                                    print("triage failed")
                                    break
                                try:
                                    hdpg = handlepage(triaged)
                                    if "iframe" in hdpg:
                                        break
                                except:
                                    print("handlepage failed")
                                    break
                                time.sleep(3)
                            closetab(2)
                            closetab(1)
                            switchtotab(0)
                except:
                    pass
            print(aurl)
            curcount = curcount + 10
            murl = newurl(aurl, curcount)
            print(murl)
            driver.get(murl)
            time.sleep(5)
            while newpag(aurl) == False:
                time.sleep(1)
    if "linkedin" in url:
        totjob = driver.find_elements_by_xpath('//*[@class="results-context-header__job-total"]').get_attribute("textContent")
        if "," in totjob:
            totjob = totjob.split(",")
            numjob = int(totjob[0] * 1000) + int(totjob[1][0:2])
        curcount = 0
        while curcount < numjob:
            avajobs = driver.find_elements_by_xpath('//*[@class="listed-job-posting__content jobs-search-result-item__content"]')
            for ava in avajobs:
                if "Easy Apply" in ava.getAttribute("innerText"):
                    print("easy apply")
                else:
                    ava.click
                    compsite = driver.find_element_by_css_selector(".apply-button")
                    compsite.click
                    manapp.append(driver.current_url)
            aurl = str(confurl(url, curcount))
            curcount = curcount + 25
            murl = newurl(aurl, curcount)
            driver.get(murl)
            time.sleep(5)
            while newpag(aurl) == False:
                time.sleep(1)


usda = getdata()
#print(usda['cusInfo']['desiredjob'])
what = usda['cusInfo']['desiredjob']
where = usda['cusInfo']['desiredlocation']
print(what)
print(where)
#print(what)
#print(where)
'''for wha in what:
    for whe in where:
        for s in jobsites:
            nurl = gnjob(wha,whe)
            sortjobs(nurl)'''

#appsites = ["https://cpaglobal.wd3.myworkdayjobs.com/en-US/CPA_External/job/US-TX-Austin/Software-Support-Engineer_REQ1362","http://kingsisle.catsone.com/careers/index.php?m=portal&a=details&jobOrderID=11505551&ref=Indeed","https://www.schwabjobs.com/ShowJob/Id/1974212/Jr.%20%20%20Associate%20Software%20Developer"]            
appsites = ["http://kingsisle.catsone.com/careers/index.php?m=portal&a=apply&jobOrderID=11505551&portalID=68536&ref=Indeed"]
for app in appsites:
    driver.get(app)
    tt = ""
    while "Finished applying" not in tt:
        try:
            tri = triagepage()
            print(tri)
        except:
            print("triage failed")
            break
        try:
            hdpag = handlepage(tri)
            #if "iframe" in hdpag:
             #   break
        except:
            print("handlepage failed")
            break
        time.sleep(3)
