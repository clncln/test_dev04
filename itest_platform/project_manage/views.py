from django.shortcuts import render
# from django.http import HttpResponse

# Create your views here.
def hello(request):
    if request.method == 'GET':
        print("get 请求")
        name = request.GET.get("name", "")
        print(name)
        return render(request, 'hello.html', {"n": name })

def index(request):
    '''
    实现登录
    '''
    # 当请求是GET类型时，返回登录页面
    if request.method == 'GET':
        return render(request, 'index.html')
    # 当请求是POST类型时，处理登陆的数据
    if request.method == 'POST':
        username = request.POST.get("username", "")
        password = request.POST.get("password", "")
        print("-->", username, password)
        if username == "" or password == "":
            print("用户名或密码不能为空")
            return render(request, 'index.html', {"error": "The username or password is empty "})
        if username == "admin" and password == "admin123456":
            return render(request, 'index.html', {"error": "login success!"})
        else:
            return render(request, 'index.html', {"error": "Wrong username or password"})