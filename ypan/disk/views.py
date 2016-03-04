from django.shortcuts import render, RequestContext, render_to_response
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.models import User
from django.contrib.sessions.models import Session
from django.contrib import auth
from django.contrib.auth.decorators import login_required
from django.conf import settings
from lib import curl
from lib.url import URL
from lib import api
import json

TEST={
        'files':[
                {'name':'file1', 'id':1},
                {'name':'file2', 'id':2}
                ],
        'folders':
                [
                {'name':'doc2', 'id':1, 'path':'/folder1/test/doc2'},
                {'name':'doc1', 'id':2, 'path':'/folder1/test/doc1'}
                ]
    }

# def login_required(request):
#     def decorator(func):
#         def wrapper(*args, **kwargs):
#             #import pdb;pdb.set_trace()
#             if not request.session.get('is_login'):
#                 return HttpResponseRedirect('/signin')
#             return func(*args, **kwargs)
#         return wrapper
#     return decorator 

def set_user(request):
    user = {}
    user['username'] = request.COOKIES.get('username','')
    user['is_authenticated'] = request.session.get('is_authenticated')
    user['is_admin'] = request.session.get('is_admin')
    return user

def set_map(path, id=None):
    dire = path.split('/')
    dires = []
    for i in range(1,len(dire)):
        dic = {}
        dic['name']=dire[i]
        dic['path']='/'.join(dire[0:i+1])
        dires.append(dic)
    return dires

# def new_set_map(dires, name, id)
#     dire = {}
#     dire['name'] = name
#     dire['id'] = id
#     dires.append(dire)
#     return dires

#@login_required(request)
def index_view(request, path='', template_name="dashboard/index.html"):
    #import pdb;pdb.set_trace()
    http_code,context = api.showFolder(request,path)
    if http_code>=400:
        return HttpResponseRedirect('/signin')
    context = json.loads(context)
    context['map'] = set_map(path)
    context['user'] = set_user(request)
    #set session for create folder
    request.session['path'] = path
    request.session['parent_id'] = context['folder'].get('id')
    return render_to_response(template_name, context, context_instance=RequestContext(request))

# def shared_view(request, path='/shared', template_name="dashboard/shared.html"):
#     #user = request.GET.get('user')
#     http_code, data = api.showFolder(request, path)
#     #import pdb; pdb.set_trace()
#     if http_code>=400:
#         return HttpResponseRedirect('/signin')
#     context = json.loads(data)
#     context['map'] = set_map(path)
#     context['user'] = set_user(request)
#     request.session['path'] = path

#     return render_to_response(template_name, context, context_instance=RequestContext(request))

def trash_view(request, path='/trash', template_name="dashboard/trash.html"):
    http_code, data = api.showFolder(request, path)
    #import pdb; pdb.set_trace()
    if http_code>=400:
        return HttpResponseRedirect('/signin')
    context = json.loads(data)
    context['map'] = set_map(path)
    context['user'] = set_user(request)
    request.session['path'] = path

    return render_to_response(template_name, context, context_instance=RequestContext(request))

def users_view(request, template_name="dashboard/users.html"):
    ghttp_code, gdata = api.getGroups(request)
    uhttp_code, udata = api.getUsers(request)
    if ghttp_code>=400 and uhttp_code>=400:
        return HttpResponseRedirect('/signin')
    gdata = json.loads(gdata)
    udata = json.loads(udata)
    context = {}
    context['groups'] = gdata['groups']
    context['users'] = udata['users']
    context['user'] = set_user(request)

    return render_to_response(template_name, context, context_instance=RequestContext(request))

#@login_required(request)
def createFolder_view(request, template_name="dashboard/index.html"):
    #import pdb;pdb.set_trace()
    http_code, data = api.createFolder(request)
    if http_code>=400:
        return HttpResponseRedirect('/signin')
    path = request.session.get('path','')
    if path == '':
        rePath = '/'
    else:
        rePath = path[:1]+'%2F'+path[1:]+'/'
    return HttpResponseRedirect(rePath)

def deleteFolder_view(request, folder_id):
    #import pdb;pdb.set_trace()
    #if request.method == 'POST':
    http_code = api.deleteFolder(request, folder_id)
    if http_code>=400:
        return HttpResponseRedirect('/signin')
    currentPath = request.session.get('path','')
    #import pdb;pdb.set_trace()
    if currentPath=='':
        rePath='/'
    else:
        rePath = currentPath[:1]+'%2F'+currentPath[1:]+'/'
    return HttpResponseRedirect(rePath)

def shareFolder_view(request):
    if request.method == 'POST':
        #import pdb;pdb.set_trace()
        user_ids = request.POST.get('user_ids').split(',')[:-1]
        folder_id = request.POST.get('folder_id')
        for user in user_ids:
            share_item = {}
            share_item['to_user']=user
            share_item['folder_id']=folder_id
            http_code, data = api.shareFolder(request, share_item)
        return HttpResponse("")
   
#@login_required(request)
def upload_view(request, template_name="dashboard/index.html"):
    if request.method == 'POST':
        f = request.FILES.get('file', None)
        #import pdb;pdb.set_trace()
        file_data =unicode(f.read(),"ISO-8859-1")
        http_code, data = api.createFile(request, f.name, file_data)
        if http_code>=400:
            return HttpResponseRedirect('/signin')
        path = request.session.get('path','')
        if path == '':
            rePath = '/'
        else:
            rePath = path[:1]+'%2F'+path[1:]+'/'
        return HttpResponseRedirect(rePath)

def download_view(request, file_id):
    http_code, data=api.getFile(request, file_id)
    if http_code>=400:
        return HttpResponseRedirect('/signin')
    file = json.loads(data)
    filename = file['name']
    file_data = file['content'].encode("ISO-8859-1")
    response = HttpResponse(file_data,content_type='application/octet-stream')
    response['Content-Disposition'] = 'attachment; filename=%s' % filename
    return response

def deleteFile_view(request, file_id):
    http_code = api.deleteFile(request, file_id)
    if http_code>=400:
        return HttpResponseRedirect('/signin')
    currentPath = request.session.get('path','')
    if currentPath=='':
        rePath='/'
    else:
        rePath = currentPath[:1]+'%2F'+currentPath[1:]+'/'
    return HttpResponseRedirect(rePath)

def shareFile_view(request):
    if request.method == 'POST':
        #import pdb;pdb.set_trace()
        user_ids = request.POST.get('user_ids').split(',')[:-1]
        file_id = request.POST.get('file_id')
        for user in user_ids:
            share_item = {}
            share_item['to_user']=user
            share_item['file_id']=file_id
            http_code, data = api.shareFile(request, share_item)
        return HttpResponse("")

#delete folder in Trash
def deleteTrashFolder_view(request, folder_id):
    #import pdb;pdb.set_trace()
    http_code = api.deleteTrashFolder(request, folder_id)
    if http_code>=400:
        return HttpResponseRedirect('/signin')
    currentPath = request.session.get('path','')
    #import pdb;pdb.set_trace()
    if currentPath=='/trash':
        rePath='/trash'
    else:
        rePath = '/trash/'+currentPath+'/'
    return HttpResponseRedirect(rePath)

def deleteTrashFile_view(request, file_id):
    http_code = api.deleteTrashFile(request, file_id)
    if http_code>=400:
        return HttpResponseRedirect('/signin')
    currentPath = request.session.get('path','')
    rePath = currentPath[:1]+'%2F'+currentPath[1:]+'/'
    return HttpResponseRedirect(rePath)

def userList_view(request, group_id=''):
    #import pdb;pdb.set_trace()
    http_code, data=api.getUsers(request)
    data = json.loads(data)
    if http_code>=400:
        return HttpResponseRedirect('/signin')
    return HttpResponse(json.dumps(data['users']))

def groupList_view(request):
    http_code, data = api.getGroups(request)
    data = json.loads(data)
    #import pdb;pdb.set_trace()
    if http_code>=400:
        return HttpResponseRedirect('/signin')
    return HttpResponse(json.dumps(data['groups']))

def createGroup_view(request):
    if request.method =='POST':
        httpcode, data = api.createGroup(request)
        return HttpResponseRedirect('/users')
#get one group infomation
def getGroup_view(request):
    if request.method=='POST':
        #import pdb;pdb.set_trace()
        if request.POST.get('group_id')=='0':
            return userList_view(request)
        httpcode, data = api.getaGroup(request)
        data = json.loads(data)
        return HttpResponse(json.dumps(data['group'].get('users')))

def deleteGroup_view(request, group_id):
    httpcode = api.deleteGroup(request, group_id)   
    return HttpResponseRedirect('/users')

def bindGroup_view(request):
    #import pdb;pdb.set_trace()
    if request.method == 'POST':
        user_id = request.POST.get('user_id')
        groups = request.POST.get('group_ids').split(',')[:-1]
        for g in groups:
            ms_item = {}
            ms_item['user_id']=user_id
            ms_item['group_id']=g
            api.addMs(request, ms_item)
        return HttpResponse("")

def addUser_view(request):
    #import pdb;pdb.set_trace()
    if request.method == 'POST':
        users = request.POST.get('user_ids').split(',')[:-1]
        group_id = request.POST.get('group_id')
        for u in users:
            ms_item = {}
            ms_item['user_id']=u
            ms_item['group_id']=group_id
            api.addMs(request, ms_item)
        return HttpResponse("")

def deleteUser_view(request, user_id):
    httpcode = api.deleteUser(request, user_id)
    return HttpResponseRedirect('/users')

def signin_view(request, template_name="dashboard/signin.html"):
    #import pdb;pdb.set_trace()
    context = {}
    #import pdb;pdb.set_trace()
    if request.method == 'POST':
        api.login(request)
        http_code,data = api.login(request)
        if int(http_code)>=400:
            return HttpResponseRedirect('/signin')
        #import pdb;pdb.set_trace()
        login_info = json.loads(data)
        request.session['token']=login_info['token']
        response = HttpResponseRedirect('/')
        if login_info['username']=='admin':
            request.session['is_admin'] = True
        else:
            request.session['is_admin'] = False
        response.set_cookie('username', login_info['username'], 3600)
        request.session['user_id'] = login_info['user_id']
        request.session['is_authenticated']=True
        return response
    return render_to_response(template_name, context, context_instance=RequestContext(request))

def signout_view(request, template_name="dashboard/signin.html"):
    context = {}
    del request.session['is_authenticated']
    del request.session['token']
    return render_to_response(template_name, context, context_instance=RequestContext(request))

def signup_view(request, template_name="dashboard/signup.html"):
    #import pdb;pdb.set_trace()
    if request.method == 'POST':
        http_code,data = api.register(request)
        if http_code>=400:
            return HttpResponseRedirect('/signup')
        return HttpResponseRedirect('/signin')
    context = {}
    return render_to_response(template_name, context, context_instance=RequestContext(request))