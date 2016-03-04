from lib import curl
from lib.url import URL
from django.conf import settings

def createFolder(request):
    if request.method == 'POST':
        data = {}
        folderName = request.POST.get('folderName')
        path = request.session.get('path','')
        token = request.session.get('token')
        data['name'] = folderName
        data['parent_id'] = request.session.get('parent_id')
        data['path'] = path + '/' + folderName
        url = URL(settings.API_URL)
        aurl = url.setUrl('/folder')
        return curl.curl_post(aurl,data,token)

def showFolder(request, path):
    url = URL(settings.API_URL)
    aurl = url.setUrl('/folder'+path)
    token = request.session.get('token')
    return curl.curl_get(aurl, token)

def deleteFolder(request, folder_id):
    url = URL(settings.API_URL)
    aurl = url.setUrl('/folder'+'/'+folder_id)
    token = request.session.get('token')
    return curl.curl_delete(aurl, token)
    # currentPath = request.session.get('path','')
    # if currentPath == '':
    #     return '/'
    # else:
    #     return currentPath[:1]+'%2F'+currentPath[1:]+'/'
def showSharedFolder(request, path, user=''):
    url = URL(settings.API_URL)
    if path == '':
        query = ''
    else:
        query = 'user='+user
    aurl = url.setUrl('/shared'+path, query)
    #import pdb;pdb.set_trace()
    token = request.session.get('token')
    return curl.curl_get(aurl, token)

def shareFolder(request, data):
    url = URL(settings.API_URL)
    aurl = url.setUrl('/shared/folder')
    token = request.session.get('token')
    return curl.curl_post(aurl, data, token)

def createFile(request, name, content):
    url = URL(settings.API_URL)
    aurl = url.setUrl('/file')
    data = {}
    data['folder_id'] = request.session.get('parent_id')
    data['name'] = name
    data['content'] = content
    token = request.session.get('token')
    return curl.curl_post(aurl, data, token)

def getFile(request, file_id):
    url = URL(settings.API_URL)
    aurl = url.setUrl('/file'+'/'+file_id)
    token = request.session.get('token')
    return curl.curl_get(aurl, token)

def deleteFile(request, file_id):
    url = URL(settings.API_URL)
    aurl = url.setUrl('/file'+'/'+file_id)
    token = request.session.get('token')
    return curl.curl_delete(aurl, token)

def shareFile(request, data):
    url = URL(settings.API_URL)
    aurl = url.setUrl('/shared/file')
    token = request.session.get('token')
    return curl.curl_post(aurl, data, token)

def deleteTrashFolder(request, folder_id):
    url = URL(settings.API_URL)
    aurl = url.setUrl('/trash/folder'+'/'+folder_id)
    token = request.session.get('token')
    return curl.curl_delete(aurl, token)

def deleteTrashFile(request, file_id):
    url = URL(settings.API_URL)
    aurl = url.setUrl('/trash/file'+ '/' + file_id)
    token = request.session.get('token')
    return curl.curl_delete(aurl, token)

def getUsers(request):
    url = URL(settings.API_URL)
    aurl = url.setUrl('/users')
    token = request.session.get('token')
    #import pdb;pdb.set_trace()
    return curl.curl_get(aurl, token)

def deleteUser(request, user_id):
    url = URL(settings.API_URL)
    aurl = url.setUrl('/user' + '/' + user_id)
    token = request.session.get('token')
    return curl.curl_delete(aurl, token)

def getGroups(request):
    url = URL(settings.API_URL)
    aurl = url.setUrl('/group')
    token = request.session.get('token')
    return curl.curl_get(aurl, token)

def createGroup(request):
    url = URL(settings.API_URL)
    aurl = url.setUrl('/group')
    data = {}
    data['name'] = request.POST.get('groupName')
    token = request.session.get('token')
    return curl.curl_post(aurl, data, token)

def getaGroup(request):
    group_id = request.POST.get('group_id')
    url = URL(settings.API_URL)
    aurl = url.setUrl('/group' + '/' + group_id)
    token = request.session.get('token')
    return curl.curl_get(aurl, token)

def deleteGroup(request, group_id):
    url = URL(settings.API_URL)
    aurl = url.setUrl('/group' + '/' + group_id)
    token = request.session.get('token')
    return curl.curl_delete(aurl, token)

def addMs(request, data):
    url = URL(settings.API_URL)
    aurl = url.setUrl('/membership')
    token = request.session.get('token')
    return curl.curl_post(aurl, data, token)

def register(request):
    data={}
    data['username']=request.POST.get('signup_username')
    data['password']=request.POST.get('signup_password')
    data['email']=request.POST.get('email')
    url = URL(settings.API_URL)
    aurl = url.setUrl('register')
    return curl.curl_post(aurl,data)

def login(request):
    data={}
    data['username']=request.POST.get('signin_username')
    data['password']=request.POST.get('signin_password')
    #data['email']=request.POST.get('email')
    url = URL(settings.API_URL)
    aurl = url.setUrl('/login')
    return curl.curl_post(aurl, data)

