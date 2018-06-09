import requests
import csv
#Requests is a Python module that you can use to send all kinds of HTTP requests
from bs4 import BeautifulSoup
import json


#import re
#Beautiful Soup is a Python library for pulling data out of HTML and XML files

def get_links(url, class_name):
    agent = {"User-Agent":'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:59.0) Gecko/20100101 Firefox/59.0'}
    page = requests.get(url, headers=agent)
    soup =BeautifulSoup(page.text,'html.parser')
    list_of_links = soup.find_all(class_= class_name)
    link_url= list()

    for x in list_of_links: 
        print('all_links',x.find_all('a'))
        #for loop to find all a tags from city_list
        for y in (x.find_all('a')):#The strip() method returns a copy of the string with both leading and trailing characters removed
            link_url.append('https://health.usnews.com'+y.get('href'))
            #print (y.get('href'))
            print ('list_of_links',link_url)
    return link_url

def get_doctorlinks(url):
    agent = {"User-Agent":'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:59.0) Gecko/20100101 Firefox/59.0'}
    page = requests.get(url, headers=agent)
    soup =BeautifulSoup(page.text,'html.parser')
    list_of_links = soup.find_all('a',class_= "search-result-link bar-tighter")
    link_url= list()
    for x in list_of_links:
        link_url.append('https://health.usnews.com'+x.get('href'))
    print len(link_url)
    return link_url

def doctor_details(url,city_name):
    agent1 = {"User-Agent":'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:59.0) Gecko/20100101 Firefox/59.0'}
    page1 = requests.get(url, headers=agent1)
    soup1 =BeautifulSoup(page1.text,'html.parser')
    overview_list=soup1.find_all(class_= "profile-overview block-loosest")
    overview = list()
    for x in overview_list:
      for y in (x.find_all('p')):
        overview= y.contents[0].strip()
        print (overview)
    overview = overview.strip()    
    fullName_flexMedia=soup1.find_all(class_= "flex-media-content")
    for x1 in fullName_flexMedia:
        for y1 in (x1.find_all('h1')):
            fullName= y1.contents[0].strip()
            print (fullName)
    fullName =fullName.strip()        

    phone_label= soup1.find(lambda tag:tag.name=="span" and "Phone Number" in tag.text)
    phoneNumber=''
    if(phone_label):
        phoneNumber = phone_label.parent.find_all('span')[2].text.strip()
        print (phoneNumber)
    phoneNumber =phoneNumber.strip()
    years_in_practise_label= soup1.find(lambda tag:tag.name=="span" and "Years in Practice" in tag.text)
    years_in_practise=''
    if(years_in_practise_label):
        years_in_practise = years_in_practise_label.parent.find_all('span')[2].text.strip()
        years_in_practise=years_in_practise.strip()
        if years_in_practise.find('+'):
           years_in_practise=years_in_practise.split("+")[0]
        if years_in_practise.find('-'):
           years_in_practise=years_in_practise.split("-")[-1]
        print (years_in_practise)
        years_in_practise = int(years_in_practise)

    languages_label= soup1.find(lambda tag:tag.name=="span" and "Languages" in tag.text)
    languages=''
    if(languages_label):
        languages = languages_label.parent.find_all('span')[2].text.strip()
        print (languages)

        
    office_location = soup1.find(attrs={"data-js-id": "doctor-address"}).text
    office_location =office_location.strip()
    if(office_location):
        zipcode= office_location[-5:]
    else:
        zipcode=''
        office_location=''   
    print(office_location)

    hospital_affiliation=[]
    hospital_affiliation_label= soup1.find(lambda tag:tag.name=="h2" and "Hospital Affiliation" in tag.text)
    if(hospital_affiliation_label):
        for x in hospital_affiliation_label.parent.find_all('div',class_="flex-small-12 padding-flush"):
            hospital_affiliation_name = x.find('h4').text.strip()
            hospital_affiliation_dscr = x.find('p').text.strip()
            print (hospital_affiliation_name,hospital_affiliation_dscr)
            hospital_affiliation.append(hospital_affiliation_name)
            
    
    specialities =[]
    Sub_specialities=[]
    specialities_label= soup1.find(lambda tag:tag.name=="h3" and "Specialties" in tag.text)
    if(specialities_label):
        for x in specialities_label.parent.find_all('a'):
            speciality_name = x.text.strip()
            print (speciality_name)
            specialities.append(speciality_name)
        for x in specialities_label.parent.find_all('p', class_='text-large block-tight'):
            sub_speciality_name = x.text.strip()
            Sub_specialities.append(sub_speciality_name)
            print (sub_speciality_name)


    education_label= soup1.find(lambda tag:tag.name=="h2" and "Education & Medical Training" in tag.text)
    education =[]
    if(education_label):
        for x in education_label.parent.find_all('li'):
            edu_name = x.contents[0].strip()
            print (edu_name)
            education.append(edu_name)

    certification_label= soup1.find(lambda tag:tag.name=="h2" and "Certifications & Licensure" in tag.text)
    certifications = []
    if(certification_label):
        for x in certification_label.parent.find_all('li'):
            certification_name = x.contents[0].strip()
            print (certification_name)
            certifications.append(certification_name)
    

    doctor_details_json = {"overview_list":overview,"fullName":fullName,"phoneNumber":phoneNumber,
                      "years_in_practise":years_in_practise,"languages":languages,
                      "office_location":office_location,"hospital_affiliation":hospital_affiliation,
                      "speciality_name":specialities,
                      "sub_speciality_name":Sub_specialities,"eductaion":education,
                      "certification_name":certifications,"city_name":city_name,
                      "zipcode":zipcode}  

    return doctor_details_json
input_state = raw_input('Enter state name: ')
state_name = ((input_state.strip()).replace(" ","-")).lower()
print input_state
url = 'https://health.usnews.com/doctors/city-index/'+state_name
#print url
list_of_cities =list()
list_of_specl =list()
list_of_doctors =list()

list_of_cities_set =list()
list_of_specl_set =list()
list_of_doctors_set =list()

#to check for all the ciities an all specialities
#list_of_cities_set=get_links(url,'index-item')
#list_of_cities=list(list_of_cities_set)

#for i in list_of_cities:
#    list_of_specl_set=get_links(i,'index-item')
list_of_specl_set =list()
list_of_specl_set.append('https://health.usnews.com/doctors/dermatologists/new-jersey/absecon')
list_of_specl_set.append('https://health.usnews.com/doctors/allergist-immunologists/new-jersey/allentown')
list_of_specl= set(list_of_specl_set)     
with open("alldoctors.json", 'w') as outfile:
    for i in list_of_specl:
         list_of_doctors=get_doctorlinks(i)
         city_name = i.split("/")[-1]
         print('city:',city_name)
         for doctor in list_of_doctors:
            doctor_details_json=doctor_details(doctor,city_name)
            json.dump(doctor_details_json, outfile)
            outfile.write('\n')
