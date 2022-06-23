# GoogleMaps-WebScrapping

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
