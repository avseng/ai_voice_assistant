import weathercom
import json
from bs4 import BeautifulSoup
import lxml
import requests
from googletrans import Translator
import wikipedia
import urllib.request
import subprocess
import logging


logger = logging.getLogger('voice assistant')

"""
Getting weather report from weather.com
"""
def weatherReport(city): 
    weatherDetails = weathercom.getCityWeatherDetails(city) 
    humidity =json.loads(weatherDetails)["vt1observation"]["humidity"] 
    temp = json.loads(weatherDetails)["vt1observation"]["temperature"] 
    phrase = json.loads(weatherDetails)["vt1observation"]["phrase"]
    return humidity, temp, phrase


"""
Perform search operation
if the content reffer any person or group, the it will check in wikipedia
otherwise it will search in google.
"""
def google_search(search_text):
    translator = Translator()
    result = ''
    search_data = search_text
    logger.info("google_search : "+search_data)
    if "who is" in search_data or "who are" in search_data:
        search_data = search_data.split(" ")[2:]
        search_data = " ".join(search_data)
        try:
            result = wikipedia.summary(search_data, sentences=2)
        except Exception as e:
            pass
    else:
        url = "https://www.google.co.in/search?q="+search_data
        logger.info("google_search : URL : "+url)
        try:
            search_result = requests.get(url).text
            soup = BeautifulSoup(search_result, 'html.parser')

            result_div = soup.find_all('div', class_='BNeawe s3v9rd AP7Wnd')

            if "born" in search_data:
                for i in result_div:
                    s = translator.translate(dest='en', text = i.text)
                    a = str(s).split("=")[3].split(",")
                    b = a[:len(a)-1]
                    b = " ".join(b)

                    if "Born" in b:
                        result = b.split(":")[1:].__str__().replace("[' ","").replace("']","")
                        #print(result)
                        break

            else:
                for i in result_div:
                    s = translator.translate(dest='en', text=i.text)
                    a = str(s).split("=")[3].split(",")
                    b = a[:len(a) - 1]
                    result = " ".join(b)
                    #print(result)
                    break
        except Exception as e:
            pass 
    logger.info("google_search : Search Result ::"+result)
    return result



"""
get the current date and time.
"""
def current_datetime(type):
    
    returndata = ''
    timeData = urllib.request.urlopen("http://worldtimeapi.org/api/ip").read()
    datetime = json.loads(timeData)["datetime"]
    date = datetime.split("T")[0]
    time = datetime.split("T")[1]
    
    if type == "time":    
        time = time.split(".")[0]
    
        hr = int(time.split(":")[0])
        min = time.split(":")[1]
        suffix = ''
        if hr >12:
            hr = hr - 12
            suffix="PM"
        else:
            suffix="AM"
    
        if hr == 0:
            hr=12
            suffix="AM"
    
        final_time = str(hr)+":"+min+" "+suffix
        logger.info("current_datetime : current time : "+final_time)
        returndata = final_time
    
    if type == "date":
        year = date.split("-")[0]
        month_int=int(date.split("-")[1])
        day = date.split("-")[2]
    
        month = ''
    
        if month_int == 1:
            month = 'Janiary'
        elif  month_int == 2:
            month = "February"
        elif month_int == 3:
            month = "March"
        elif month_int == 4:
            month = "April"
        elif month_int == 5:
            month = "May"
        elif month_int == 6:
            month = "June"
        elif month_int == 7:
            month = "July"
        elif month_int == 8:
            month = "August"
        elif month_int == 9:
            month = "September"
        elif month_int == 10:
            month = "October"
        elif month_int == 11:
            month = "Novenber"
        elif month_int == 12:
            month = "December"
        
        logger.info("current_datetime : today's date : "+month+" " +day+", "+year)
        returndata = month+" " +day+", "+year
    
    return returndata


"""
Reboot raspberry pi.
"""
def reboot_server():
    command = "/usr/bin/sudo /sbin/shutdown -r now"
    process = subprocess.Popen(command.split(), stdout=subprocess.PIPE)

