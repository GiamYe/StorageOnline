import urlparse

class URL(object):
    """docstring for URL"""
    def __init__(self, url):
        self.url = urlparse.urlparse(url)

    def setUrl(self, path, query=''):
        urlpath = path
        #urlquery = 'user='+ str(user_id)
        return urlparse.urlunparse((self.url.scheme,self.url.netloc,urlpath,'',query,''))


if __name__ == '__main__':
    url = 'http://172.16.17.90:5000/folder?user=5'
    aurl = URL(url)
    print aurl.setUrl('/document', 3)


        