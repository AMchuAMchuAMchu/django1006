import datetime

from django.shortcuts import render, redirect

# Create your views here.
from mysite import models


# 全局变量计算次数
count = 0



# 日志功能
def logMysiteInfo(accessInfo):
    with open(file=r'D:\seldom\rd\Django_school\django1006\static\log\accessLog.log',mode='a',encoding='utf-8',) as file:
        file.writelines(accessInfo+'\n')

# session的判断方法封装
def session_judge(request):
    username = request.session.get('username')
    password = request.session.get('password')
    # 到数据库查询一下是否有...
    users = models.UserInfo.objects.filter(username=username,password=password)
    accessInfo = str(datetime.datetime.now())+'进行了session判断'
    logMysiteInfo(accessInfo)
    return users.count()


# 首页,页面展示以及登录功能的实现
def index(request):
    global count
    count += 1
    # 这里的有人其实可以实时的展示到底是谁访问的...诶,才发现其实的话是有很多优化的地方的说
    accessInfo = str(datetime.datetime.now())+'有人访问了index页面:第'+str(count)+'次'
    logMysiteInfo(accessInfo)
    print(accessInfo)
    return render(request,'index.html')


# 这个的话是中间的处理路由,不会直接向客户端响应页面,主要是为了减轻userInfoList页面处理业务逻辑用的(避免userInfoList业务逻辑过于复杂)
# ,处理完了业务逻辑之后
# 将会重定向到index路由然后再进行index路由的业务处理最后再返回最终处理完了的页面...
def handle_form_index(request):
    if request.POST.get('username') != '' and request.POST.get('password') != '':
        username = request.POST.get('username')
        password = request.POST.get('password')
        # 到数据库
        users = models.UserInfo.objects.filter(username=username,password=password)
        if users.count() > 0:
            request.session['username'] = username
            request.session['password'] = password
            request.session.set_expiry(value=120)
            return redirect(to='/userInfoList/',request=request)
        else:
            return render(request,'error_index.html')
    return render(request,'error_index.html')

# 用户的列表展示以及添加用户http://127.0.0.1:8001/userInfoList/
def userInfoList(request):
    countUIL = session_judge(request)
    if countUIL > 0:
        # 去掉空格
        username_userInfoList = str(request.POST.get('username_userInfoList')).strip()
        password_userInfoList = str(request.POST.get('password_userInfoList')).strip()
        # 这里的话是必须需要四重判断才可以!!!!  != '' 且 != None
        if username_userInfoList != '' and password_userInfoList != '' and username_userInfoList != None and password_userInfoList != None and username_userInfoList != 'None' and password_userInfoList != 'None':
        # index那边来的用户名和我们userInfoList添加的用不用的key名字即可区分....
            models.UserInfo.objects.create(username=username_userInfoList,password=password_userInfoList)
            user_list = list(models.UserInfo.objects.all())
            return render(request,'userInfoList.html',{'data':user_list})
        # 这里的话是第一次从handle_form_index路由过来的时候需要直接返回数据库已有的数据进行展示
        userList = list(models.UserInfo.objects.all())
        return render(request,'userInfoList.html', {'data': userList})
    return render(request,'error_index.html')