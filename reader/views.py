# -*- coding:utf-8 -*-

from django.shortcuts import render, render_to_response
from django.http import HttpResponse, HttpResponseRedirect
# Create your views here.

from django import forms
from django.views.decorators.csrf import csrf_exempt

from models import Reader

from datetime import *

import re
import json
import os

# 登入登出的restful API
# get 代表获取 session
# post 代表创建 session
# delete 代表删除 session 登出
@csrf_exempt
def session(request):
    if request.method == 'GET':
        if 'readerName' in request.COOKIES:
            return HttpResponseRedirect('/')
        errMsg = request.GET.get('errMsg')
        if errMsg != None:
            return render(request, "reader/login.html", {'errMsg': errMsg})
        else:
            return render(request, "reader/login.html")
    elif request.method == 'POST':
        lf = forms.Form(request.POST)
        if lf.is_valid():
            readerName = lf.data['readerName']
            password = lf.data['password']
            reader = Reader.objects.filter(readerName=readerName, password=password)
            if len(reader) == 0:
                return HttpResponseRedirect("session?errMsg=Wrong Username Or Password")
            response = HttpResponseRedirect('/')
            response.set_cookie('readerName', readerName, 24 * 3600)
            return response
        else:
            return HttpResponseRedirect("session?errMsg=Missing Username Or Password")
    elif request.method == 'DELETE':
        print '123'
        #response = HttpResponseRedirect('/')
        response = HttpResponse()
        response.delete_cookie('readerName')
        return response

# 登入登出的restful API
# get 代表获取 session
# post 代表创建 session
# delete 代表删除 session 登出
@csrf_exempt
def fresher(request):
    if request.method == 'GET':
        if 'readerName' in request.COOKIES:
            return HttpResponseRedirect('/')
        errMsg = request.GET.get('errMsg')
        if errMsg != None:
            return render(request, "reader/register.html", {'errMsg': errMsg})
        else:
            return render(request, "reader/register.html")
    if request.method == 'POST':
        rf = forms.Form(request.POST)
        # 防止直接通过url访问
        if rf.is_valid() and 'readerName' in rf.data:

            errMsg = ""
            readerName = rf.data['readerName']
            password = rf.data['password']
            repeatPassword = rf.data['repeatPassword']
            email = rf.data['email']

            pattern = re.compile(r'[0-9a-zA-Z.]+@[0-9a-zA-Z.]+?com')

            if len(readerName) < 3:
                errMsg = "Username Too Short"
            elif password != repeatPassword:
                errMsg = "Password Unmatched"
            elif len(password) < 6:
                errMsg = "Password Too Short"
            elif pattern.match(email) == None:
                errMsg = "Invaild Email"

            # if errMsg != ""
            # 密码和用户是否能正常注册 用mysql

            check = Reader.objects.filter(readerName=readerName)

            if len(check) != 0:
                errMsg = "Username exists"

            if errMsg == "":

                newReader = Reader(readerName=readerName,
                                   password=password,
                                   email=email,
                                   registerDate=datetime.now(),  # .strftime('%Y-%m-%d %H:%M:%S')
                                   birthday=date(1900, 01, 01))
                newReader.save()

                response = HttpResponseRedirect('/')
                response.set_cookie('readerName', readerName, 24 * 3600)
                return response
            else:
                # return render_to_response('reader/register.html', {'errMsg': errMsg})
                return HttpResponseRedirect("fresher?errMsg=" + errMsg)

        else:
            return HttpResponseRedirect("fresher?errMsg=Information Missing")

def profile(request):

    if request.method == 'GET':

        if 'readerName' not in request.COOKIES:
            return HttpResponseRedirect('session')
        else:
            reader = Reader.objects.filter(readerName=request.COOKIES['readerName']).first()
            if reader == None:
                return HttpResponseRedirect('session')
            else:
                errMsg = request.GET.get('errMsg')
                if errMsg != None:
                    return render(request, 'reader/profile.html', {'reader': reader, 'errMsg': errMsg})
                else:
                    return render(request, 'reader/profile.html', {'reader':reader})

    elif request.method == 'PUT':
        if 'readerName' not in request.COOKIES:
            return HttpResponseRedirect('session')
        else:
            upf = forms.Form(request.POST)

            newPassword = upf.data['newPassword']
            repeatNewPassword = upf.data['repeatNewPassword']

            errMsg = ""

            if newPassword != repeatNewPassword:
                errMsg = "Password Unmatched"
            elif len(newPassword) < 6:
                errMsg = "Password Too Short"

            if errMsg == "":
                reader = Reader.objects.filter(readerName=request.COOKIES['readerName']).first()
                reader.password = newPassword
                reader.save()
                return HttpResponseRedirect('profile')
            else:
                return HttpResponseRedirect("profile?errMsg=" + errMsg)

def profileUpdate(request):

    if 'readerName' not in request.COOKIES:
        return HttpResponseRedirect('session')
    else:
        upf = forms.Form(request.POST)
        reader = Reader.objects.filter(readerName=request.COOKIES['readerName']).first()
        reader.gender = upf.data['gender']
        birthday = [int(element) for element in upf.data['birth'].split('-')]
        reader.birthday = date(birthday[0],birthday[1],birthday[2])
        reader.save()
        return HttpResponseRedirect('profile')


def passwordUpdate(request):
    if 'readerName' not in request.COOKIES:
        return HttpResponseRedirect('session')
    else:
        upf = forms.Form(request.POST)

        newPassword = upf.data['newPassword']
        repeatNewPassword = upf.data['repeatNewPassword']

        errMsg = ""

        if newPassword != repeatNewPassword:
            errMsg = "Password Unmatched"
        elif len(newPassword) < 6:
            errMsg = "Password Too Short"

        if errMsg=="":
            reader = Reader.objects.filter(readerName=request.COOKIES['readerName']).first()
            reader.password = newPassword
            reader.save()
            return HttpResponseRedirect('profile')
        else:
            return HttpResponseRedirect("profile?errMsg="+errMsg)


@csrf_exempt
def uploadIcon(request):

    file = request.FILES.get('tmpIcon')

    readerName = request.COOKIES['readerName']

    if file==None:
        return HttpResponse(json.dumps({'msg':'fail','extra':'No File Uploaded'}), content_type='application/json')
    else:

        #判断是不是合法的图片
        import imghdr
        if imghdr.what(file)==None:
            return HttpResponse(json.dumps({'msg': 'fail', 'extra': 'Wrong Type'}),
                                content_type='application/json')

        BASE_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),"static", "img", "icons");

        #为用户新建头像文件夹
        try:
            BASE_DIR = os.path.join(BASE_DIR, readerName)
            os.mkdir(BASE_DIR)
        except:
            print 'Folder xists'

        temp_name = str(datetime.now())
        modified_name = temp_name+"."+file.name.split('.')[-1]

        url = os.path.join(BASE_DIR, modified_name) #本地路径

        f = open(url, "wb")

        for chunck in file.chunks():
            f.write(chunck)
        f.close()

        return HttpResponse(json.dumps({'msg':'success', 'url':readerName+'/'+modified_name}), content_type='application/json')


def updateIcon(request):
    if 'readerName' not in request.COOKIES:
        return HttpResponseRedirect('session')
    else:
        form = forms.Form(request.POST)

        readerName = request.COOKIES['readerName']

        if form.data['newIconName']==None or form.data['newIconName']=='':
            return HttpResponseRedirect('profile')
        else:
            reader = Reader.objects.filter(readerName=readerName).first()
            reader.icon = form.data['newIconName']
            reader.save()
            return HttpResponseRedirect('profile')


def space(request, readerName):
    return HttpResponse(readerName+"'s Space... Please wait")