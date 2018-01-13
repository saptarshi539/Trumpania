from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from urllib import urlopen
import re
import json
import requests


def get_home(request):
    '''
    Home page
    '''
    return render(request, 'crawl/main.html', {})


def get_tweets(request):
    JSON_HEADER = {'Accept': '*/*', 'X-AYLIEN-TextAPI-Application-Key': 'f63147288b7d1b12215280223f00c315','X-AYLIEN-TextAPI-Application-ID': '336fb365','accept-encoding': 'gzip, deflate'}
    '''
    Gets the latest tweets from Trumps official account
    '''
    #Write the tweets to a temp file
    html = urlopen('https://twitter.com/realDonaldTrump')
    fw = open('source_file', 'w')
    fw.write(str(html.read()))
    fw.close()

    #Read tweets from the temp file
    fr = open('source_file', 'r')
    lines = fr.readlines()
    fr.close()
    trump_tweets = []
	
	
    for line in lines:
		#obtain the class from the html in order to find the tweet match and store it in a list
        matches = re.findall(
            r'<p class="TweetTextSize TweetTextSize--normal js-tweet-text tweet-text" lang="en" data-aria-label-part="0">.*?</p>', line, re.M | re.I)
        for match in matches:
            match = re.sub(
                '<p class="TweetTextSize TweetTextSize--normal js-tweet-text tweet-text" lang="en" data-aria-label-part="0">', '', match)
            #Finds the atual text under the html div
            match = re.sub('</p>', '', match)
            mention_hrefs = re.findall(r'<a href=".*?" class', match)
            for mention_href in mention_hrefs:
				#find if there are any links present, if there are then show it as a link
				mention = re.findall(r'".*?"', mention_href)[0]
				if 'http' in mention:
					continue
				match = re.sub(
					mention, '\"https://twitter.com' + mention[1:], match)
					
			#An additional feature is added to this page where the sentiment analysis is done using the APIs from this website http://docs.aylien.com/docs/sentiment 
            params = (('text' , str(match)), ('mode', 'tweet'))
            response = requests.get("https://api.aylien.com/api/v1/sentiment?", params = params, headers=JSON_HEADER).json()
            trump_tweets.append(match + "      The overall sentiment of the tweet is - "+str(response["polarity"]))
			#Check if the number of tweets are greater than equal to 25 otherwise break
            if len(trump_tweets) >= 25:
			    break
    return render(request, 'crawl/tweets.html', {'tweets': trump_tweets})


def get_articles(request):
    '''
    Gets the latest Trump articles from cnn.com
    '''
    JSON_HEADER = {'Accept': '*/*', 'X-AYLIEN-TextAPI-Application-Key': 'f63147288b7d1b12215280223f00c315','X-AYLIEN-TextAPI-Application-ID': '336fb365','accept-encoding': 'gzip, deflate'}
	#Write articles to a temp file
    html = urlopen('http://edition.cnn.com/')
    fw = open('source_file', 'w')
    fw.write(str(html.read()))
    fw.close()

    #Read articles from the temp file
    fr = open('source_file', 'r')
    lines = fr.readlines()
    fr.close()
    trump_news = []

    for line in lines:
        matches = re.findall(r'{\"uri.*?}', line, re.M | re.I)
        for match in matches:
            if 'trump' in match.lower():
                trump_news.append(match)

    headlines = []
    descriptions = []
    uris = []
    thumbnails = []
    head_indices = []
    for news in trump_news:
        article_json = json.loads(news.replace(
            "\\'", "'").replace('\\\\"', "'"),  strict=False)
        headlines.append(article_json['headline'])
        head_indices.append(trump_news.index(news))
        descriptions.append(article_json['description'])
        thumbnails.append(str(article_json['thumbnail']))
        uris.append(str(article_json['uri']))

    titles = []
    authors = []
    datetimes = []
    contents = []
    sentiments = []
    
    #The actual URL of the CNN article is obtained
    for uri in uris:
        print uri
        html = urlopen('http://edition.cnn.com' + uri)
        fw = open('source_file_2', 'w')
        fw.write(str(html.read()))
        fw.close()
        fr = open('source_file_2', 'r')
        lines = fr.readlines()
        content = ''
        title = ''
        author = ''
        datetime = ''
        for line in lines:
            matches = \
                re.findall(r'class=\"zn-body__paragraph.*?\">.*?<\/div>'
                           , line, re.M | re.I)
            for match in matches:
                content += match
            matches = re.findall(r'<h1 class="pg-headline">.*?<\/h1>',
                                 line)
            for match in matches:
                title += match
            matches = \
                re.findall(r'<span class="metadata__byline__author">.*?<\/span>'
                           , line)
            for match in matches:
                auth_hrefs = re.findall(r'<a href=".*?" class', match)
                for auth_href in auth_hrefs:

                    auth_link = re.findall(r'".*?"', auth_href)[0]
                    if 'http' in auth_link:
                        continue
                    match = re.sub(auth_link, '"https://cnn.com'
                                   + auth_link[1:], match)
                author += match
            matches = re.findall(r'<p class="update-time">.*?<\/span',
                                 line)
            for match in matches:
                datetime += match
        content = re.sub(r'class=\"zn-body__paragraph.*?\">', '',
                         content)
        content = re.sub('</div>', '<br>', content)

        title = re.sub(r'<h1 class="pg-headline">', '', title)
        title = re.sub('<\/h1>', '', title)

        author = re.sub(r'<span class="metadata__byline__author">', '',
                        author)
        author = re.sub('<\/span>', '', author)

        datetime = re.sub(r'<p class="update-time">', '', datetime)
        datetime = re.sub('<\/span', '', datetime)
		
		#An additional feature is added to this page where the sentiment analysis is done using the APIs from this website http://docs.aylien.com/docs/sentiment
        params = (('text', str(match)), ('mode', 'tweet'))
        response = \
            requests.get('https://api.aylien.com/api/v1/sentiment?',
                         params=params, headers=JSON_HEADER).json()
        contents.append(content
                        + 'The overall sentiment of the article is '
                        + str(response['polarity']))
        titles.append(title)
        authors.append(author)
        datetimes.append(datetime)
        if len(uris) >= 25:
		    break

			
    print len(uris)
        
    headlines_zipped = zip(head_indices, headlines)
    return render(request, 'crawl/cnn.html', {'headlines_zipped': headlines_zipped, 'descriptions': descriptions,
                                              'uris': uris, 'thumbnails': thumbnails, 'contents': contents, 'titles': titles, 'authors': authors, 'datetimes': datetimes, 'sentiments': sentiments})
