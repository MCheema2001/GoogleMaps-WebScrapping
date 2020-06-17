from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys  import Keys
from selenium import webdriver
import unittest
import time
from multiprocessing import Process , Pool ,Lock
import threading as thr
from itertools import product
import os
from bs4 import BeautifulSoup as BS
import re
import datetime
from datetime import datetime as date
import pandas as pd
import pymongo
from pymongo import MongoClient
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


process_you_want=12
no_of_roads = 24

driver=[]

df = pd.read_csv("roads.csv")

End_Location        = df["D_L_N"]
Start_location      = df["S_L_N"]
End_Location_lats   = df["D_L_Lat"]
Start_location_lats = df["S_L_Lat"]
End_Location_long   = df["D_L_Long"]
Start_location_long = df["S_L_Long"]

store_data_local = True

Username="Musa"
Password='1234'

Online_Data_Base_URL='mongodb+srv://'+Username+':'+Password+'@cluster0-ifrbh.mongodb.net/DataPythonProject?retryWrites=true&w=majority'
Local_Data_Base_URL="mongodb://localhost:27017/?readPreference=primary&appname=MongoDB%20Compass&ssl=false"

def Open_Automation_tabs(process_you_want):
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    for i in range (process_you_want):
        Path="/Users/musadac/Desktop/chromedriver"
        driver.append(webdriver.Chrome(Path,options=chrome_options))
    driver.append(webdriver.Chrome(Path))

def Close_Automation_tabs(process_you_want):
    global driver
    for i in range (process_you_want):
        driver[i].quit()

def save_data(F_R, T_E, Dis, Tem, Con, D_T,D_T2,S_L,E_L,S_L_Lon,S_L_Lat,D_L_Lon,D_L_Lat, i):
    if(store_data_local==True):
       cluster =  MongoClient(Local_Data_Base_URL)
       db = cluster['DataPythonProject']
       coll = db['Test_Final']
    else:
       cluster =MongoClient(Online_Data_Base_URL)
       db = cluster['DataPythonProject']
       coll = db.Islamabad_Traffic_Data
    Day = date.today().strftime("%A")
    po = { "Start_Location": S_L,"End_location":E_L, "Start_Location_Lat":S_L_Lat, "Start_Location_Lon":S_L_Lon, "End_Location_Lat":D_L_Lat, "End_Location_Lon":D_L_Lon, "Fastest_Route": F_R, "Time_Estimated": T_E, "Distance": Dis,"Speed":(Dis/T_E), "Temperature": Tem, "Condition_Weather":Con,"Date":D_T,"Time":D_T2, "Day":Day }
    coll.insert_one(po)



def Startup_Google_Maps(i):
    global driver
#    Path="/Users/musadac/Desktop/chromedriver"
#    driver=webdriver.Chrome(Path)
    driver[i%process_you_want].get("https://www.google.com/maps/dir///@33.5675392,73.0988544,12z/data=!4m2!4m1!3e0")
    
    time.sleep(3)
    try:
      St = str(Start_location_lats[i])+","+str(Start_location_long[i])
      search_start_point = driver[i%process_you_want].find_element_by_xpath('//*[@id="sb_ifc50"]/input')
      search_start_point.send_keys(St)
      search_destination_point = driver[i%process_you_want].find_element_by_xpath('//*[@id="sb_ifc51"]/input')
      search_destination_point.send_keys(str(End_Location_lats[i])+","+str(End_Location_long[i]))
      search_destination_point.send_keys(Keys.RETURN)
      time.sleep(15)
      data=driver[i%process_you_want].page_source
     
      soup = BS(data, "lxml")


      Fastest_Route=soup.find_all(id="section-directions-trip-title-0")
      Fastest_Route=Fastest_Route[0].text
#      print(Fastest_Route)

      Time_Estimated=soup.find_all("div", {"class": "section-directions-trip-duration"})
      Time_Estimated=re.sub("\s\s+","", Time_Estimated[0].text)
      Time_Estimated=Time_Estimated.split(" ")
      if(Time_Estimated[2]=='mintypically'):
          Time_Estimated=(int(str(Time_Estimated[1]))*60)
      else:
          Time_Estimated=int(Time_Estimated[1])

      Distance=soup.find_all("div", {"class": "section-directions-trip-distance section-directions-trip-secondary-text"})
      Distance=Distance[0].text
      Distance=Distance.split(" ")
      len_Dis= len(Distance)
      if(Distance[len_Dis-2] =='m'):
         Distance=float(Distance[len_Dis-3])
#         print(Distance)
      else:
         Distance=float(str(Distance[len_Dis-3]))*1000
#         print(Distance)

      
      
     
      data=driver[process_you_want].page_source
      
      soup = BS(data, "lxml")

      Temp=soup.find_all("div", {"class": "temp"})
      Temp=re.sub("\s\s+","", Temp[0].text)
#      print(Temp)
                  
      Condition=soup.find_all("div", {"class": "cond"})
      Condition=re.sub("\s\s+","", Condition[0].text)
#      print(Condition)
      
      currentDT = datetime.datetime.now()
      currentDT=str(currentDT)
      currentDT=currentDT.split(".")
      currentDT=currentDT[0]
      currentDT=currentDT.split(" ")
#      print (currentDT)

      
      save_data(Fastest_Route, Time_Estimated, Distance, Temp, Condition, currentDT[0],currentDT[1],Start_location[i],End_Location[i],Start_location_long[i],Start_location_lats[i],End_Location_long[i],End_Location_lats[i], i)
          
    except:
      print("Sorry Something Went Wrong :(")
      print("Retrying..."+str(i))
      Startup_Google_Maps(i)
    

threads=[]
k=0
def multithreading(i):
    global process_you_want
    global k
    for i in range(process_you_want):
        p = thr.Thread(target=Startup_Google_Maps, args=([k%no_of_roads]))
        k+=1
        p.start()
        threads.append(p)
        
    for thread in threads:
        thread.join()
    
#s=[]


Open_Automation_tabs(process_you_want)
#if __name__ == '__main__':
for i in range (5000):
    driver[process_you_want].get("https://www.accuweather.com/en/pk/islamabad/258278/weather-forecast/258278")
    multithreading(i)
   
Close_Automation_tabs(process_you_want)
##print(s)

