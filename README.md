# Trumpania
Trumpania scrapes the latest tweets and latest tweets from Donald Trumps official twitter account and articles from cnn.com respectively. The highlight of this project is the sentiment
analysis which has been done on the articles and tweets. The overall sentiment is listed in the end of each tweet and each article.


# 1-Installation

This project is a Django project. 
The project can be cloned and Django 1.11 can be installed by using the command pip install django==1.11

# 2- How to use

When you run the command .\manage.py runserver in trumpcrawler directory.  This will start the Django server locally in your machine, once Django is installed correctly. 
Then navigate to http://localhost:8000/crawl/main url on your web browser. This will birng you to main page. You can choose to see the latest article or latest tweets on this page.
If you choose articles, this will navigate you to another page. At the left you will see the headlines of the articles. If you click on of the headlines you will see the content of the article on the left. 
If you choose to see the tweets, you will end up with a different page showing Trump's latest tweets. You can click the links on tweets.

# 3- Notes
The cool feature of Trumpania is the sentiment analysis of the article or the tweet. The polarity is listed in the end of the article once you click on the article or in the end of 
the tweet in either place it says - "The sentiment of the tweet is positive" for the tweets and "The overall sentiment of the article is positive" for the articles. The APIs are obtained from 
http://docs.aylien.com/docs/sentiment with the API key "f63147288b7d1b12215280223f00c315" and API ID as "336fb365" which is also mentioned inside the code
