import scrapy
import os
import json
import requests

class CollectionSpider(scrapy.Spider):

    name = 'collectionSpider'

    def start_requests(self):
        url = 'https://quotefancy.com/'
        tag = getattr(self, 'collection', None)
        self.log(self.collection)
        if self.collection is not None:
            url += self.collection
        yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        self.log(response.url)
        directory = response.url.split('/')[-1]
        self.log(directory)
        os.mkdir(directory)
        imgs = response.css('div.wallpaper.scrollable>div.frame>a>img')
        texts = imgs.css('img::attr(alt)').extract()
        wpids = imgs.css('img::attr(data-wallpaper-id)').extract()
        
        os.mkdir(directory+'/images')
        imgfolder = directory + '/images/'
        logfile = directory + '/log.txt'
        count = 0
        for text, wpid in zip(texts, wpids):
            count += 1
            # text = str(text)
            # quote = self.getQuote(text) 
            # author = self.getAuthor(text)
            # self.log('Text: ' + str(type(text)))
            # self.log('Quote: ' + quote)
            # self.log('Author: ' + author)
            # line = "#{0} {1} {2} {3}\n".format(count,wpid, quote, author)
            line = "#{0} {1} {2}\n".format(count, wpid, text)
            self.log('Data: ' + line)
            self.writetofile(logfile, line)
            self.log('Data writen to log file successfully.')
            self.getImage(imgfolder, wpid)

    def getQuote(self, text):
        qstart = text.find('"')
        qend = text.rfind('"')
        return text[qstart+1 : qend]
    
    def getAuthor(self, text):
        start = text.rfind('-') + 2
        return text[start:]

    def writetofile(self, path, content):
        with open(path, 'a') as file:
            file.write(content)

    def getImage(self, path, id):
        url = 'https://quotefancy.com/download/%s/original/wallpaper.jpg' % id
        file_path = path + '%s.jpg'%id
        self.log('Fetching the wallpaper #{0}.'.format(id))
        response = requests.get(url)
        with open(file_path, 'wb') as f:
            f.write(response.content)
        self.log('Wallpaper fetch successfull.')
        
