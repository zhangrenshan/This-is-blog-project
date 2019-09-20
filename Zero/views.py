from django.shortcuts import render, HttpResponseRedirect
from Zero.models import *
import hashlib


def base(request):
    return render(request, 'base.html', locals())


def setPassword(password):
    md5 = hashlib.md5()
    md5.update(password.encode())
    result = md5.hexdigest()
    return result


def loginValid(func):
    def inner(request, *args, **kwargs):
        cookie_email = request.COOKIES.get('user_email')
        session_email = request.session.get('user_email')
        if cookie_email and session_email and cookie_email == session_email:
            return func(request, *args, **kwargs)
        else:
            return HttpResponseRedirect('/login/')
    return inner


def register(request):
    if request.method == 'POST':
        user_email = request.POST.get('email')
        if user_email:
            user = User.objects.filter(user_email=user_email).first()
            if not user:
                user_password = request.POST.get('password')
                user_password2 = request.POST.get('password2')
                if user_password == user_password2:
                    new_user = User()
                    new_user.user_email = user_email
                    new_user.user_password = setPassword(user_password)
                    new_user.user_name = request.POST.get('username')
                    new_user.save()
                    response = HttpResponseRedirect('/login/')
                    return response
                else:
                    error_message = '请确认两次密码输入是否一致'
            else:
                error_message = '邮箱已被注册，请登录'
        else:
            error_message = '邮箱不可以为空'
    return render(request, 'register.html', locals())


def login(request):
    if request.method == 'POST':
        user_email = request.POST.get('email')
        user_password = request.POST.get('password')
        if user_email:
            user = User.objects.filter(user_email=user_email).first()
            if user:
                db_password = user.user_password
                user_password = setPassword(user_password)
                if db_password == user_password:
                    print(db_password)
                    print(user_password)
                    response = HttpResponseRedirect('/index/')
                    # cookie里面的第一个参数，和之前的user_email没有任何关系，类似于变量名
                    response.set_cookie('user_email', user.user_email)
                    # 没有人会把密码设为cookie
                    # response.set_cookie('user_password', user.user_password)
                    response.set_cookie('id', user.id)
                    request.session['user_email'] = user.user_email
                    request.session['id'] = user.id
                    return response
    return render(request, 'login.html', locals())

@loginValid
def index(request):
    type_list = ArticleType.objects.all()
    result = []
    for ty in type_list:
        article = ty.article_set.order_by('article_public_time')
        if len(article) >= 3:
            article = article[:3]
            print(len(article))
            result.append({'type': ty, 'article_list': article})
    return render(request, 'index.html', locals())


def article_list(request):
    pass


@loginValid
def details(request, id):
    article = Article.objects.get(id=int(id))
    return render(request, 'details.html', locals())
# Create your views here.
