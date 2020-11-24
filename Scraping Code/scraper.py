import selenium
import pandas
import numpy as np
from selenium import webdriver
import time


#Main Code Fetching Courses and the links
DRIVERPATH="C:\Program Files (x86)\chromedriver.exe"
driver=webdriver.Chrome(DRIVERPATH)
driver.get('https://www.udemy.com/')

a='udlite-btn udlite-btn-large udlite-btn-ghost udlite-heading-md udlite-btn-icon udlite-btn-icon-large'
a=a.replace(' ','.')
a
time.sleep(5)
next_link='udlite-btn udlite-btn-medium udlite-btn-secondary udlite-btn-round udlite-heading-sm udlite-btn-icon udlite-btn-icon-medium udlite-btn-icon-round pagination--next--5NrLo'
next_link=next_link.replace(' ','.')
time.sleep(3)
e=driver.find_element_by_class_name('udlite-text-input.udlite-text-input-small.udlite-text-sm.udlite-search-form-autocomplete-input.js-header-search-field')
for s in 'Web Development':  # Change the string here for a different set of courses
    e.send_keys(s)
    time.sleep(0.3)
time.sleep(2)
driver.find_element_by_class_name(a).click()
time.sleep(10)
block_=driver.find_elements_by_class_name('course-card--container--3w8Zm.course-card--large--1BVxY')

time.sleep(3)

info=[]
for i in range(10):# The number of pages to scrape
    block_=driver.find_elements_by_class_name('popper--popper--19faV.popper--popper-hover--4YJ5J')
    for j in block_:
            content=[]
            try:
                title=j.find_element_by_class_name('udlite-focus-visible-target.udlite-heading-md.course-card--course-title--2f7tE')
                content.append(title.text)
            except:
                content.append('Not Available')
            try:
                tagline=j.find_element_by_class_name('udlite-text-sm.course-card--course-headline--yIrRk')
                content.append(tagline.text)
            except:
                content.append('Not Available')
            try:
                instructor=j.find_element_by_class_name('udlite-text-xs.course-card--instructor-list--lIA4f')
                content.append(instructor.text)
            except:
                content.append('Not Available')
            try:
                rating=j.find_element_by_class_name('udlite-heading-sm.star-rating--rating-number--3lVe8')
                content.append(rating.text)
            except:
                content.append('Not Available')
            try:
                bestseller=j.find_element_by_class_name('udlite-badge.udlite-heading-xs.udlite-badge-bestseller')
                content.append('Bestseller')
            except:
                content.append('Not Available')
            try:
                reviews=j.find_element_by_class_name('udlite-text-xs.course-card--reviews-text--12UpL')
                content.append(reviews.text)
            except:
                content.append('Not Available')
            try:
                otherinfo=j.find_element_by_class_name('udlite-text-xs.course-card--row--1OMjg.course-card--course-meta-info--1hHb3')
                content.append(otherinfo.text)
            except:
                content.append('Not Available')
            try:
                links=j.find_element_by_tag_name('a').get_attribute('href')
                content.append(links)
            except:
                content.append('Not Available')
            info.append(content)
    driver.execute_script("window.scrollTo(0,document.body.scrollHeight)")
    time.sleep(4)
    driver.find_element_by_class_name(next_link).click()
    time.sleep(10)
    
driver.quit()


###Forming pd table
import pandas as pd
Data=pd.DataFrame(info,columns=['Title','HeadLine','Instructors','Rating','Tags','Reviews','AddInfo','Links'])
##Cleaning the table
Data[Data['Title']=='Not Available'].index
Data.drop(Data[Data['Title']=='Not Available'].index,axis=0,inplace=True)
#Resetting index
Data.reset_index(inplace=True)
Data.drop('index',axis=1,inplace=True)



## Taking the links from dataset and taking each description
import selenium
import pandas
import numpy as np
from selenium import webdriver
import time
DRIVERPATH="chromedriver"
driver=webdriver.Chrome(executable_path=DRIVERPATH)

what_to_learn=[]
for i in list(Data.Links):
    print(i)
    driver.get(i)
    try:
        l=driver.find_element_by_class_name('unstyled-list.udlite-block-list.what-you-will-learn--objectives-list--2cWZN').text
        what_to_learn.append(l)
    except:
        what_to_learn.append('Not Available')
   
##Making the list into pd format

what=pd.Series(what_to_learn,name='Description')

##Appending the column to existing dataset
temp=pd.concat([Data,what],axis=1)
temp

##Saving File as xlsx
temp.to_csv('web_dev_fin.csv')