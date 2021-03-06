from django.conf.urls import patterns, include, url
from django.conf import settings
from disk.views import *

urlpatterns = patterns('',
    url(r'^$', index_view, name='index'),
    url(r'^signin/$', signin_view, name='signin'),
    url(r'^signout/$', signout_view, name='signout'),
    url(r'^signup/$', signup_view, name='signup'),
    url(r'^(?P<path>(((/.*/)|(/))([^/]+)))/$', index_view, name='next'),
    url(r'^upload/$', upload_view, name='upload'),
    url(r'^createFolder/$', createFolder_view, name='createFolder'),
    url(r'^deleteFolder/(?P<folder_id>\d+)/$', deleteFolder_view, name='deleteFolder'),
    url(r'^deleteFile/(?P<file_id>\d+)/$', deleteFile_view, name='deleteFile'),
    #url(r'^shared/$', shared_view, name='shared'),
    #url(r'^shared/(?P<path>(((/.*/)|(/))([^/]+)))/$', shared_view, name='shared_next'),
    url(r'^trash/$', trash_view, name='trash'),
    url(r'^trash/(?P<path>(((/.*/)|(/))([^/]+)))/$', trash_view, name='trash_next'),
    url(r'^download/(?P<file_id>\d+)/$', download_view, name='download'),
    url(r'^userlist/$', userList_view, name='userlist'),
    url(r'^deleteTrashFolder/(?P<folder_id>\d+)/$', deleteTrashFolder_view, name='deleteTrashFolder'),
    url(r'^deleteTrashFile/(?P<file_id>\d+)/$', deleteTrashFile_view, name='deleteTrashFile'),
    url(r'^shareFolder/$', shareFolder_view, name='shareFolder'),
    url(r'^shareFile/$', shareFile_view, name='shareFile'),
    url(r'^users/$', users_view, name='users'),
    url(r'^createGroup/$', createGroup_view, name='createGroup'),
    url(r'^group/(?P<group_id>\d+)/$', deleteGroup_view, name='deleteGroup'),
    url(r'^user/(?P<user_id>\d+)/$', deleteUser_view, name='deleteUser'),
    url(r'^grouplist/$', groupList_view, name='groupList'),
    url(r'^bindgroup/$', bindGroup_view, name='bindgroup'),
    url(r'^adduser/$', addUser_view, name='adduser'),
    url(r'getgroup/$', getGroup_view, name='getgroup'),
)