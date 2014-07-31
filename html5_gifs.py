import praw
import urllib2
import urllib
import json
import requests
import string
import random
 
class Post:
   _registry = []
 
   def __init__(self, title, gfylink, subreddit, giflink, gifsize, webmsize):
      self.title = title
      self.gfylink = gfylink
      self.subreddit = subreddit
      self.giflink = giflink
      self.gifsize = gifsize
      self.webmsize = webmsize
      self._registry.append(self)
     
def sizeof(num):
        for x in ['bytes','KB','MB','GB']:
            if num < 1024.0 and num > -1024.0:
                return "%3.1f%s" % (num, x)
            num /= 1024.0
        return "%3.1f%s" % (num, 'TB')
       
r = praw.Reddit(user_agent='/u/html5_gifs by /u/illredditthat - Reposts large GIFs as Gfycats')
r.login('html5_gifs', '#REDACTED#')
 
subreddits = ['perfectloops', 'HighQualityGifs', 'funny', 'gifs']
number = 25
target = 'webm'
limit = 3
 
for subreddit in subreddits:
    #submissions = r.get_subreddit(subreddit).get_hot(limit=number)
    submissions = r.get_subreddit(subreddit).get_top_from_day(limit=number)
 
    for x in submissions:
        if not x.url.endswith('.gif'): continue
        encodedURL = urllib.quote_plus(x.url) #Encode the GIF URL
       
        url = urllib2.urlopen('http://gfycat.com/cajax/checkUrl/' + encodedURL) # Checks if already a gfycat
        data = json.loads(url.read())
       
        if data['urlKnown'] == 'true':
            gfy = data['gfyUrl']
 
        else:
            random_id = ''.join(random.choice(string.ascii_letters + string.digits) for _ in xrange(10))
            url = urllib2.urlopen('http://upload.gfycat.com/transcode/' + random_id + '?fetchUrl=' + encodedURL) # Makes new gfycat
            data = json.loads(url.read())
            gfy = 'http://gfycat.com/' + data['gfyname']
           
        gfyname = gfy.replace('http://gfycat.com/','')
        url = urllib2.urlopen('http://gfycat.com/cajax/get/' + gfyname)
        data = json.loads(url.read())
 
        gifsize = data['gfyItem']['gifSize']
        webmsize = data['gfyItem']['webmSize']
        gfyname = Post(x.title, gfy, subreddit, x.short_link, gifsize, webmsize)
 
posts = sorted(Post._registry, key=lambda x: x.gifsize, reverse=True)
posted = 0
postnum = 0
while (posted < limit):
    post = posts[postnum]
    comment = '[Comments and original .gif from /r/' + post.subreddit + ' here.](' + post.giflink + ')\n\n^(Gif Size: ' + sizeof(post.gifsize) + ' Webm Size: ' + sizeof(post.webmsize) + ' || )[^(Feedback/Why)](http://redd.it/29itck) ^|| [^(Contact me)](http://www.reddit.com/message/compose?to=%2Fr%2Fhtml5_gifs)'
    print 'Submitted ' + post.gfylink + ' ' + post.title + ' to ' + target + ' original at: ' + post.giflink
    try:
        r.submit(target, post.title, url=post.gfylink).add_comment(comment)
        posted += 1
    except Exception, e:
          print e
    postnum += 1