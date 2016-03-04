import pycurl
import StringIO
import json

def curl_get(url,token=''):
     curl = pycurl.Curl()
     head = ['Content-Type:application/json','X-Token:'+str(token)]
     buf = StringIO.StringIO()
     curl.setopt(pycurl.WRITEFUNCTION,buf.write)
     curl.setopt(pycurl.HTTPHEADER,head)
     curl.setopt(pycurl.URL, url)
     try:
        curl.perform()
        http_code = curl.getinfo(pycurl.HTTP_CODE)
        data = buf.getvalue()
        #data = json.loads(data)
        buf.close()
        #assert if httpcode>=500, 'wrong'
        return http_code,data
     except Exception,e:
        print 'No data returns'

def curl_post(url,post_data,token=''):
     curl = pycurl.Curl()
     post_data = json.dumps(post_data)
     head = ['Content-Type:application/json','X-Token:'+token]
     buf = StringIO.StringIO()
     curl.setopt(pycurl.WRITEFUNCTION, buf.write)
     curl.setopt(pycurl.HTTPHEADER, head)
     curl.setopt(pycurl.POSTFIELDS, post_data)
     curl.setopt(pycurl.URL, url)
     curl.perform()
     #import pdb;pdb.set_trace()
     http_code = curl.getinfo(pycurl.HTTP_CODE)
     data = buf.getvalue()
     #assert if httpcode>=500, 'wrong'
     #data = json.loads(data)
     buf.close()
     return http_code, data

def curl_put(url, update_data, token=''):
    """update_data:dict
    """
    curl = pycurl.Curl()
    update_data = json.dumps(update_data)
    head = ['Content-Type:application/json','X-Token:'+token]
    buf = StringIO.StringIO()
    curl.setopt(pycurl.WRITEFUNCTION, buf.write)
    curl.setopt(pycurl.HTTPHEADER, head)
    crl.setopt(pycurl.CUSTOMREQUEST, 'PUT')
    curl.setopt(pycurl.POSTFIELDS, update_data)
    curl.setopt(pycurl.URL, url)
    curl.perform()
    http_code = curl.getinfo(pycurl.HTTP_CODE)
    data = buf.getvalue()
    #data = json.loads(data)
    buf.close()
    return http_code,data

def curl_delete(url, token=''):
    curl = pycurl.Curl()
    head = ['Content-Type:application/json','X-Token:'+token]
    buf = StringIO.StringIO()
    curl.setopt(pycurl.WRITEFUNCTION, buf.write)
    curl.setopt(pycurl.HTTPHEADER, head)
    curl.setopt(pycurl.CUSTOMREQUEST, 'DELETE')
    curl.setopt(pycurl.URL, url)
    curl.perform()
    http_code = curl.getinfo(pycurl.HTTP_CODE)
    #data = buf.getvalue()
    #data = json.loads(data)
    buf.close()
    return http_code



if __name__ == '__main__':
    url = 'http://172.17.128.80:5000/login'
    postdata = {"username" : "user","password" : "13"}
    httpcode, data = curl_post(url,postdata)
    print httpcode
    print data
    #post_data = {'name':'doc_3','parent_id':5,'path':'/doc_3'}
    #data = postdata(url, post_data)
    #data = getdata(url)
    #data_dic = json.loads(data)
    #import pdb;pdb.set_trace()
    #print data