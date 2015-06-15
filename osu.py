##################################
#### Osu Data Module
#### Author: kitokunx
#### Version: 1.1
#### Contact: kitokunxd@gmail.com
##################################

#####Required Imports

import urllib.request
import re
import sys

class OsuNews(object): #object containing recent news

  def __init__(self):
    self.url = "https://osu.ppy.sh"
    self.rawData = self.getRawData(self.url)
    self.dataArray = list()
    self.newsCounter = 0
    self.news = dict()
    self.procData(self.rawData)
    
  #get the raw data
  def getRawData(self, url):
    data = urllib.request.urlopen(url).read().decode()
    return data
  
  #process raw data
  def procData(self, data):
    x = data.split("<h2 class='ntitle'><a href='/p/news'>News</a></h2>")[1]
    y = x.split("<div class='hug-bottom'>")[0].replace("\n", "")
    self.dataArray = y.split('<div class="news-heading">')[1:]
    for i in self.dataArray:
      date = i.split("&nbsp;")[0]
      link = 'https://osu.ppy.sh' + i.split('&nbsp;<a href="')[1].split('"><b>osu!')[0]
      desc = i.split('<div class="news-text"><p>')[1].split('</p></div>')[0]
      self.news[self.newsCounter] = {"link":link, "date":date, "description":desc}
      self.newsCounter = self.newsCounter + 1


class OsuUser(object): #Osu User class

  def __init__(self, user):
    self.rawData = self.getRawData(user.lower())
    if self.userExists(self.rawData):
      self.location = self.userLoc(self.rawData)
      self.age = self.userAge(self.rawData)
      self.avatar = self.userAvatar(self.rawData)
      self.interests = self.userInterests(self.rawData)
      self.occupation = self.userOccupation(self.rawData)
      self.country = self.userCountry(self.rawData)
      self.consoles = self.userConsole(self.rawData)
      self.userId = None
      self.performancePoints = None
      self.ranks = dict()
      self.recent = dict()
    else:
      return None

  #####Function to get raw data

  def getRawData(self, name):
    name = name.lower()
    url = "http://osu.ppy.sh/u/"+name
    data = urllib.request.urlopen(url).read().decode()
    return data
        
  #####Boolean to check if the user exists or not
  def userExists(self, data):
    if "The user you are looking for was not found!" in data:
        return False
    else:
        return True


  #####Get Osu User Location
  def userLoc(self, data):
    try:
      location = re.compile(r"<div title='Location'><i class='icon-map-marker'></i><div>(.*?)</div>", re.IGNORECASE).search(data).group(1)
      return location  
    except AttributeError:
      return "Location was not submitted to osu database."

    
  #####Get Osu User Age
  def userAge(self, data):
    try:
      age = re.compile(r"<div title='Age'><i class='icon-user'></i><div>(.*?)</div>", re.IGNORECASE).search(data).group(1)
      return age
    except AttributeError:
      return "Age was not submitted to osu database."

  #####Get Osu User Avatar Url
  def userAvatar(self, data):
    try:
      avatar = re.compile(r'<div class="avatar-holder"><img src="(.*?)" alt="User avatar"/></div>', re.IGNORECASE).search(data).group(1)
      avatarUrl = "https:"+avatar
      return avatarUrl
    except AttributeError:
      return "User has no avatar/profile pic yet"


  #####Get Osu User Interests
  def userInterests(self, data):
    try:
      interests = re.compile(r"<div title='Interests'><i class='icon-heart-empty'></i><div>(.*?)</div>", re.IGNORECASE).search(data).group(1)
      return interests
    except AttributeError:
      return "User has not given interests information."

  #####Get Osu User Occupation
  def userOccupation(self, data):
    try:
      occupation = re.compile(r"<div title='Occupation'><i class='icon-pencil'></i><div>(.*?)</div>", re.IGNORECASE).search(data).group(1)
      return occupation
    except AttributeError:
      return "User has not given any occupation info."

  #####Get Osu User Country
  def userCountry(self, data):
    try:
      country = re.compile(r"<img class='flag' title='(.*?)' src", re.IGNORECASE).search(data).group(1)
      return country
    except Exception as e:
      return str(e)

  #####Get User Consoles
  def userConsole(self, data):
    try:
      consoles = list()
      if re.compile(r"<div class='playstyle mouse (.*?)'></div>", re.IGNORECASE).search(data).group(1) == "using":
        consoles.append("Mouse")
      if re.compile(r"<div class='playstyle keyboard (.*?)'></div>", re.IGNORECASE).search(data).group(1) == "using":
        consoles.append("Keyboard")
      if re.compile(r"<div class='playstyle tablet (.*?)'></div>", re.IGNORECASE).search(data).group(1) == "using":
        consoles.append("Tablet")
      if re.compile(r"<div class='playstyle touch (.*?)'></div>", re.IGNORECASE).search(data).group(1) == "using":
        consoles.append("Touch Screen")
      else:
        consoles.append("None Submitted")
      return consoles
    except Exception as e:
      print(str(e))

