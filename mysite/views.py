import datetime

from django.shortcuts import render

# Create your views here.


def logMysiteInfo(accessInfo):
    with open(file=r'D:\seldom\rd\Django_school\django1006\static\log\accessLog.log',mode='a',encoding='utf-8',) as file:
        file.writelines(accessInfo+'\n')


count = 0

def index(request):
    global count
    count += 1
    accessInfo = str(datetime.datetime.now())+'有人访问了index页面:第'+str(count)+'次'
    logMysiteInfo(accessInfo)
    print(accessInfo)
    return render(request,'index.html')

# 这个的话是中间的处理路由,不会直接向客户端响应页面,主要是为了减轻index页面处理业务逻辑用的,处理完了业务逻辑之后
# 将会重定向到index路由然后再进行index路由的业务处理最后再返回最终处理完了的页面...
def handle_form_index(request):

    return None