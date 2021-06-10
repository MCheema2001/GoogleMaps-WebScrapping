"""
 Web data scraping and crawling aren’t illegal by themselves, but it is important to be ethical while doing it. Don’t tread onto other people’s sites without being considerate. Respect the rules of their site. Consider reading over their Terms of Service, read the robots.txt file. If you suspect a site is preventing you from crawling, consider contacting the webmaster and asking permission to crawl their site. Don’t burn out their bandwidth–try using a slower crawl rate (like 3 request per 10-15 seconds). Don’t publish any content you find that was not intended to be published.
 
 GoogleMaps Robots.txt File
        Allow: /maps?*output=classic*
        Allow: /maps?*file=
        Allow: /maps/d/
        Disallow: /maps?
        Disallow: /mapstt?
        Disallow: /mapslt?
        Disallow: /maps/stk/
        Disallow: /maps/br?
        Disallow: /mapabcpoi?
        Disallow: /maphp?
        Disallow: /mapprint?
        Disallow: /maps/api/js/
        Allow: /maps/api/js
        Disallow: /maps/api/place/js/
        Disallow: /maps/api/staticmap
        Disallow: /maps/api/streetview
        Disallow: /maps/_/sw/manifest.json
        Disallow: /mld?
        Disallow: /staticmap?
        Disallow: /maps/preview
        Disallow: /maps/place
        Disallow: /maps/timeline/
        Disallow: /help/maps/streetview/partners/welcome/
        Disallow: /help/maps/indoormaps/partners/
        
This Code is written In Accordance with the Google Terms and Condition and Data scrapped will only be used for research and Study Purposes .
 
"""
#**********************************************************
#**********************************************************

"""
Before You Start:

Make Sure you have Installed Following Libararies Python Version 3.6 or Greater

pip install selenium
pip install re
pip install bs4
pip install pandas
pip install pymongo
pip install pymongo[srv]            for online Database
pip install lxml

Make Sure that Road.csv and Google Chrome Web Driver is present in Same Directory as This Script If not then change Path Accordingly in
Functions Like Open_Automation_Tabs and In Dataframe

Download the Google WebDriver according to your Chrome version from

https://chromedriver.chromium.org

This Code is Highly Efficent and is made under Time Consideration and Other Factors Described Below

Internet Speed : Internet Speed is one Factor in Loading Websites If You Have 10 Mbps or Greater Speed then no need to Change
                 time.sleep() in Start_Google_Map Function If it is less then you should Accordingly to Load all Contents of Website
                 So You have to give it more time if Time is Less the Console will give Retrying this and also at same time Saving Data
                 of Which it was Able to Load and Gives Error for which it couldn't So Watch Out :)

Time : This Mines Data 2 to 3 Times in a Min Depending Upon the Internet Speed Not Exhausting Bandwidth and Following Rules and
       Regulations In Multithreading it can take 2 * Number_OF_Process CLicks For example if Number of Process are 12 then
       It will give us 24 Documnets in a Min As Google Maps get Updated After 5 mins so we can easily mine 24*5 120 Roads Data.
       Weather Data is not Loaded Again and Again but rather loaded in seprate tab as it is Updated after every 10 mins and This Code
       is meant for one City so Why is their need to Load Website in all Tabs but we can load it in one Seprate Tab :) Time Decreased in
       Loading Again and Again. :)
       
CPU / GPU / Memory : CPU is also Controlled By Use of Threading Instead of Processing As it Doesn't Occupy all the Cores of CPU
                     Allowing us to do Other Things Other then This
                     Maximum CPU ConSumption is 33% for 2.0GHz CPU
                     Average CPU Consumption is 15% for 2.0GHz CPU
                     Minimum CPU Consumption is 9 % for 2.0GHz CPU
                     
                     As Headless mode of Chrome is Used this Decrerses the Cpu and GPU use Signficantly from 90% Average CPu usage and
                     GPU usuage of 40 % to
                     15 % CPU and 2 % GPU
                     Memory is also Decreased  From 1GB * No Of Process to 520 MB * No Of Process
                     
This Code is GMT Locked That if you are Using a Cloud Machine or Cloud Computing Your Data and Time may vary Due to Time Differnece
In Place where Cloud Computers are So Consider Running this Script on Local Machine of Which Place Data you have to Mine If You are
Mining Data of Islamabad then Your Computer Should be in Pakistan not in Other Country If you are in Other Country Try Using DateTime
GMT Format or Change Your System Date Time Accordingly.

Road CSV is in Following Way

S_L_N                         D_L_N                         S_L_Lat      S_L_Long     D_L_Lat      D_L_Long

ZeroPoint                     Islamabad_Highway_LokVirsa    33.693425    73.065567    33.686649    73.070701
Islamabad_Highway_LokVirsa    Islamabad_Highway_ShakarParian    33.686649    73.070701    33.678471    73.076838
Islamabad_Highway_ShakarParian    Islamabad_Highway_Faizabad    33.678471    73.076838    33.665016    73.086818
Islamabad_Highway_Faizabad    Islamabad_Highway_GardenTown    33.665016    73.086818    33.635523    73.10895
Islamabad_Highway_GardenTown    Islamabad_Highway_GhouriTown    33.635523    73.10895    33.616455    73.123327

CopyRight @ MusaDAC 2020  mcheema2010@gmail.com
"""
#**********************************************************
#**********************************************************

"""
Libararies Used
"""
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys  import Keys
from selenium import webdriver
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
import os
"""
^^^^^^^^^^^^^^^
Libararies Used
"""

#--------------------------------------------------------
process_you_want= os.cpu_count() # Number of Process That you want in Parallel os.cpu_count is using all cores of cpu available
no_of_roads = 24                 # Number of Roads of which the data you are mining for
#--------------------------------------------------------
driver=[]                        # Driver array to Store all the Google Chrome Automation Instances :)

df = pd.read_csv("roads.csv")    # Reads the Data of Roads of Which Data has to Mined from Google Maps

End_Location        = df["D_L_N"]      # Reads the Destination Location Name from csv
Start_location      = df["S_L_N"]      # Reads the Starting Location Name from csv
End_Location_lats   = df["D_L_Lat"]    # Reads the Destination Latitude from csv
Start_location_lats = df["S_L_Lat"]    # Reads the Starting Latitude from csv
End_Location_long   = df["D_L_Long"]   # Reads the Destination Longitude from csv
Start_location_long = df["S_L_Long"]   # Reads the Starting Longitude from csv

store_data_local = True                # Variable Stroing Bool Value for Storing in Local MongoDB Database or Online MongoDB srvc

Username="Musa"          # Username for Online MongoDB
Password='1234'          # Password for Online MongoDB

"""
Url for Accessing DataBAse Online Local Both
"""

Online_Data_Base_URL='mongodb+srv://'+Username+':'+Password+'@cluster0-ifrbh.mongodb.net/DataPythonProject?retryWrites=true&w=majority'
Local_Data_Base_URL="mongodb://localhost:27017/?readPreference=primary&appname=MongoDB%20Compass&ssl=false"

"""
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
Url for Accessing DataBase Online Local Both
"""
#------------------------------------- Function For Opening Chrome  Automation Through which Data will be mined
def Open_Automation_tabs(process_you_want):
    chrome_options = Options()                     # To Use the Options of Chrome Used for Efficency Increase
    chrome_options.add_argument("--headless")      # This makes the Chrome run in Background
    """
    Note : The Headless mode of Chrome is not Supported by all the websites so check wheather that website supports it
    """
    for i in range (process_you_want):             # For loops that Open n Number of Tabs in Background
        Path="/Users/musadac/Desktop/chromedriver" # Path to Webdriver This should be Modified Accordingly to Your PC
        driver.append(webdriver.Chrome(Path,options=chrome_options)) # Opens tab and saves Information to an Array to Control
    driver.append(webdriver.Chrome(Path,options=chrome_options)) # n+1 Tab is Opened to mine Data of Weather Only Efficency Increase
#------------------------------------- Function For Opening Chrome  Automation Through which Data will be mined

#--------------------------Split a String
def split(word):
   return [char for char in word] # Returns the Array of Char
#--------------------------Split a String

#--------------------------Function for Closing Chrome Tabs
def Close_Automation_tabs(process_you_want):
    global driver
    for i in range (process_you_want+1):
        driver[i].quit() #Chrome Tab is Closed 1 is Added Because of Weather Tab
#--------------------------Function for Closing Chrome Tabs

#--------------------------Function to Save Data in DataBase (MongoDB)
def save_data(F_R, T_E, Dis, Tem, Con, D_T,D_T2,S_L,E_L,S_L_Lon,S_L_Lat,D_L_Lon,D_L_Lat, prediction_google, i):
    if(store_data_local==True):                      # If Store Data is Opted for Local Local Data is Accessed
       cluster =  MongoClient(Local_Data_Base_URL)   # Local DataBase is Accesed
       db = cluster['DataPythonProject']             # Local Cluster is Accessed Name Should be Changed Accordingly if Not Changed it will auto create new one with this name
       coll = db['Final_Tests']                      # Local Reposiory of Cluster is Accessed
    else:
       cluster =MongoClient(Online_Data_Base_URL)    # Online DataBase is Accesed
       db = cluster['DataPythonProject']             # Online Cluster is Accessed Name Should be Changed Accordingly if Not Changed it will auto create new one with this name
       coll = db.Islamabad_Traffic_Data              # Online Reposiory of Cluster is Accessed
    Day = date.today().strftime("%A")                # Day is Extracted From System
    po = { "Start_Location": S_L,"End_location":E_L, "Start_Location_Lat":S_L_Lat, "Start_Location_Lon":S_L_Lon, "End_Location_Lat":D_L_Lat, "End_Location_Lon":D_L_Lon, "Fastest_Route": F_R, "Time_Estimated": T_E, "Distance": Dis,"Speed":(Dis/T_E), "Temperature": Tem, "Condition_Weather":Con,"Date":D_T,"Time":D_T2, "Day":Day, "Pred_Google":prediction_google } # All Data is Organized into Dictionary
    pp = coll.insert_one(po)              # Data is Inserted in MongoDB
    print(pp)                             # Status is Printed Weather Addition was Succes
#--------------------------Function to Save Data in DataBase (MongoDB)

#--------------------------Function to Start DataMining
def Startup_Google_Maps(i):
    global driver        # Driver Array is Accessed in Function
    driver[i%process_you_want].get("https://www.google.com/maps/dir///@33.5675392,73.0988544,12z/data=!4m2!4m1!3e0") # Google Maps Website is Opened
    
    time.sleep(3)     # Must Read Before you Start at the Top
    try:              # Try Statement to try to Mine Data
      St = str(Start_location_lats[i])+","+str(Start_location_long[i])  # Start Location Coordinates are Join which are From Road.csv
      search_start_point = driver[i%process_you_want].find_element_by_xpath('//*[@id="sb_ifc50"]/input') #  Designated Area of Website for Entering Start Location is Found
      search_start_point.send_keys(St) # Inserted into Designated Ares
      search_destination_point = driver[i%process_you_want].find_element_by_xpath('//*[@id="sb_ifc51"]/input')#  Designated Area of Website for Entering End Location is Found
      search_destination_point.send_keys(str(End_Location_lats[i])+","+str(End_Location_long[i])) # Inserted into Designated Ares
      search_destination_point.send_keys(Keys.RETURN) # and Enter is hit to Get Traffic Data of that Segment of Road
      time.sleep(15)   # Must Read Before you Start at the Top
      data=driver[i%process_you_want].page_source # Page Data HTML is Stored in a Variable Data
      
      soup = BS(data, "lxml") # HTML Is Parsed into LXML to Extract Data More Easily
      visibility = driver[i%process_you_want].find_element_by_xpath("/html/body/jsl/div[3]/div[9]/div[8]/div/div[1]/div/div/div[5]/div/div[2]/div[1]/div[1]/div[1]") # Find the Colour which Indicated the Traffic Flow This allows us to Store Google Predicted Congestion
      attributeValue = visibility.value_of_css_property('color') #.get_attribute("style") Color of the Text
      if (attributeValue == "rgba(24, 128, 56, 1)"):
         prediction_google = "Smooth"               # If Color is Green Prediction is Smooth
      elif(attributeValue == "rgba(0, 0, 0, 0.87)"):
         prediction_google = "NaN"                  # If Color is Gray Prediction is None
      elif(attributeValue == "rgba(217, 48, 37, 1)"):
          prediction_google = "Highly_Congested"    # If Color is Red Prediction is Highly Congested
      elif(attributeValue == "rgba(227, 116, 0, 1)"):
          prediction_google = "Mild_Congestion"     # If Color is Orange Prediction is Mild Congestion
      else:
          prediction_google = "Blockage" # If Color is Dark_Red Prediction is Blockage
          
      Fastest_Route=soup.find_all(id="section-directions-trip-title-0") #Fastest Route is Extracted
      Fastest_Route=Fastest_Route[0].text  # It's Text is Stored in a Variable
      Time_Estimated=soup.find_all("div", {"class": "section-directions-trip-duration"}) # Estimated Time of Arrival is Extracted
      Time_Estimated=re.sub("\s\s+","", Time_Estimated[0].text) # All Spaces are removed so that we can get number
      Time_Estimated=Time_Estimated.split(" ") # Then Number is Seprated and Min or Second Label is Seprated
      if(Time_Estimated[2]=='mintypically'):
          Time_Estimated=(int(str(Time_Estimated[1]))*60) # If Time is mins it is Converted into Seconds
      else:
          Time_Estimated=int(Time_Estimated[1]) # Else it is saved as it is
      Distance=soup.find_all("div", {"class": "section-directions-trip-distance section-directions-trip-secondary-text"})
      # Distance is extracted and stored
      #------------------------------------------------------------
      Distance=Distance[0].text
      Distance=Distance.split(" ")
      len_Dis= len(Distance)
      """
      Distance is Split and len is Calculated as their was different types of String Formats Coming
      Some had km or m some had Additional Notes Written
      But all had a Pattern that Second last Word was of Distance
      km is converted in to m
      whereas m remians the same
      """
      if(Distance[len_Dis-2] =='m'):
         Distance=float(Distance[len_Dis-3])
      else:
         Distance=float(str(Distance[len_Dis-3]))*1000
      #--------------------------------------------------------- Weather Data Extraction from n+1 Tab
      data=driver[process_you_want].page_source         # Page HTML is Saved in a Variable
      soup = BS(data, "lxml")                           # HTML is Converted to LXML
      Temp = soup.find("div",{"class":'vk_bk sol-tmp'}) # Temperature Element is Extracted
      Temp = str(Temp.text)                             # Temperature Text is Saved
      Temp= split(Temp)                                 # Temperatue is split in order to get the Celcius 0 , 1 and Farhenhite are Stored in 2, 3
      Temp = float(Temp[0]+Temp[1])                     # Celcius Temperature is Taken Only
      Condition = soup.find_all("div",{"id":'wob_dcp'}) # Weather Condition element is Stored
      Condition = Condition[0].text                     # Weather Condition is Stroed in Variable
      #--------------------------------------------------------- Weather Data Extraction from n+1 Tab
      currentDT = datetime.datetime.now()               # Current Date time is Taken From System Read Flaws in Before you Start
      currentDT=str(currentDT)                          # Converted to String
      currentDT=currentDT.split(".")                    # To Split the Seconds and Microseconds in Time Section
      currentDT=currentDT[0]                            # First Part is taken MM/DD/YYYY HH:MM:SS
      currentDT=currentDT.split(" ")                    # Date and Time are Seprated in an array and Used Later
      save_data(Fastest_Route, Time_Estimated, Distance, Temp, Condition, currentDT[0],currentDT[1],Start_location[i],End_Location[i],Start_location_long[i],Start_location_lats[i],End_Location_long[i],End_Location_lats[i],prediction_google, i) # Function is Called to Store the Data in MongoDB
    except:
      print("Sorry Something Went Wrong :(")           # Tells Something Went Wrong in The Code When Trying To Extract Data
      print("Retrying..."+str(i))                      # Tells That it is Going to Retry to Mine Data and Tells which Road was it
      Startup_Google_Maps(i)                           # Recurision is Applied to remine if fails the First Time
#--------------------------Function to Start DataMining

threads=[]  # To Store the Parallel CPU Wprking Instances
k=0
def multithreading(i):
    global process_you_want
    global k
    for i in range(process_you_want):
        p = thr.Thread(target=Startup_Google_Maps, args=([k%no_of_roads])) # Starts the Process at Thread n and of Road t
        k+=1                # Keeps Track and Manages Number of Roads
        p.start()           # Thread is Started
        threads.append(p)   # Thread is Appended
        
    for thread in threads:  # Thread is Joined in a For loop so that all Completes and then Comes the Next
        thread.join()
    
#s=[]


Open_Automation_tabs(process_you_want) # Function is Calledd
#if __name__ == '__main__': # For Windows You Have to Use
for i in range (5000):
    driver[process_you_want].get("https://www.google.com/search?source=hp&ei=savqXo_nCb3lgwe-obfACg&q=islamabad+weather&oq=islamabad+weather&gs_lcp=CgZwc3ktYWIQA1DiDFj6DmCgD2gAcAB4AIABAIgBAJIBAJgBAKABAaoBB2d3cy13aXo&sclient=psy-ab&ved=0ahUKEwjPg8DShIrqAhW98uAKHb7QDagQ4dUDCAc&uact=5")  # Weather Data Website is Loaded in n+1 Driver Tab
    multithreading(i) # MultiTasking Function is Called 5000*processyouwant clicks will be Extracted

Close_Automation_tabs(process_you_want) # and Tabs are Closed


"""
Last Updated : June 18, 2020
"""
