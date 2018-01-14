# Trumpania
Trumpania scrapes the latest tweets and latest tweets from Donald Trumps official twitter account and articles from cnn.com respectively. The highlight of this project is the sentiment
analysis which has been done on the articles and tweets. The overall sentiment is listed in the end of each tweet and each article in bold. 


# Installation

This project is a python Django project. If you do not have python install please install python 2.7.13 from https://www.python.org/downloads/ 
The project can be cloned and Django 1.11 can be installed by using the command pip install django==1.11

# How to use

When you run the command .\manage.py runserver in trumpcrawler directory.  This will start the Django server locally in your machine, once Django is installed correctly. 
Then navigate to http://localhost:8000/crawl/main url on your web browser. This will birng you to main page. One can choose to see the latest article or latest tweets on this page.
If you choose articles, this will navigate you to another page. At the left you will see the headlines of the articles. If you click on of the headlines you will see the content of the article on the left. 
If you choose to see the tweets, you will end up with a different page showing Trump's latest tweets. You can click the links on tweets.

This app is deployed in heroku which is an open-source portal for publishing applications in different languages. Here is the link to the app - https://trumpania.herokuapp.com/crawl/main
The sentiment analysis urls can be accessed 1000 times a day. The heroku app can be viewed anytime for 30 minutes continuously.

# Feature
The cool feature of Trumpania is the sentiment analysis of the article or the tweet. The polarity is listed in the end of the article once you click on the article or in the end of 
the tweet in either place it says - "The sentiment of the tweet is positive" for the tweets and "The overall sentiment of the article is positive" for the articles. The APIs are obtained from 
http://docs.aylien.com/docs/sentiment with the API key "f63147288b7d1b12215280223f00c315" and API ID as "336fb365" which is also mentioned inside the code. The sentiments are listed
in bold in the tweets as well as in the articles
