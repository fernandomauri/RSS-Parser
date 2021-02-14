import requests
from bs4 import BeautifulSoup
from socket import error as SocketError
import errno
import feedparser
import os

'''
RSS files follow the structure:

<channel>
    <title>
    <description>
    <link>
    <item>
</channel>

Function parseXML traverses through RSS files in the local filesystem, extracts <link>, and places it in a list of links. In main() the links are fetched one by one.

'''

def parseXML():
    # Read extracted XML files from directory in file system
    base_dir = "/base/directory/where/file/is/"
    # Concatenate a new filepath for each file in the XML directory
    files = [os.path.join(base_dir, i) for i in os.listdir("/directory/where/file/is")]

    story_links = list()
    # Traverse through each file in the directory
    for file in files:
        NewsFeed = feedparser.parse(file)
        stories = NewsFeed.entries
        for story in stories:
            for key in story:
                if key == 'link':
                    story_links.append(story[key])
    story_links.sort()
    return story_links

def main() :
    rssFeeds = parseXML()
    article_count = 1
    for i in range(len(rssFeeds)):
        f = open('/path/to/xml/files/rssArticleNo{}.txt'.format(str(article_count)), 'w', encoding='utf-8')       
        try:
            page = requests.get(rssFeeds[i])
            # Print the status code of the request
            print(page.status_code)
            # Create BeautifulSoup object, take HTML content as input, use appropriate parser
            soup = BeautifulSoup(page.content, 'html.parser')
            # Find main content of the website
            paragraphs = soup.find('body')
            # Write story article body to the output file
            if paragraphs != None and page.status_code == 200:
                pText = paragraphs.getText().replace('\n','')
                f.write(pText + '\n')
                print(pText)
            else:
                continue

            f.close()
            print("Article {} saved".format(article_count))
        
        '''
Sometimes RSS feeds are unavailable. Reasons for this can include making too many requests in a short period of time, or the RSS feed does not like web scrapers. Prepare to move onto the next article if a SocketError occurs.
        '''
        except SocketError as e:
            if e.errno == errno.ECONNRESET:
                print("Connection to article reset")
                continue
        
        article_count += 1

main()

