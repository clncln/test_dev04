from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib import auth     # 导入登录认证的包
from django.contrib.auth.decorators import login_required       # 导入login的装饰器


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
            # print("用户名或密码不能为空")
            return render(request, 'index.html', {"error": "The username or password is empty "})

        # 上面拿到当前登录的用户的信息，在这里我们调用一下auth认证的函数，然后把user的信息打印出来，检查一下
        user = auth.authenticate(username=username, password=password)
        print("==>", user)

        if user is not None:
            auth.login(request, user)       # 登录成功后到数据库中写session_key
            # return render(request, 'manage.html')   # 登录成功之后我们想让它跳转到一个新的页面，那么我们可以在这里新建一个html文件来展示登录成功的信息；
            # 这样虽然分开展示了登录成功的信息，但仍然在index页面中；要让它在新的页面中展示，这里就不要给它返回一个页面，而要用到登录成功之后的重定向，重定向到其他路经下面
            return HttpResponseRedirect("/manage/")

        else:
            return render(request, 'index.html', {"error": "Wrong username or password"})

@login_required
def manage(request):
    """
    管理页面
    """
    return render(request, "manage.html")
    # 这样的话，我们登录之后就跳转到了新的manage页面了。
    # 但是呢，这么实现的话，有一个很大的坑，我们这里写了一个manage的页面，我们只要知道这个manage的路径，不用登录就可以直接进来了，那么登录就没有意义了
    # 我们怎么要把这个窗户堵上，让它只能通过登录这一个门进来呢，这里就需要引入django里面的另外一个函数，login的装饰器，通过这个装饰器来控制视图允不允许你在未登录的情况下访问（第4行导包）
    # 第45行，在方法前面增加装饰器，控制用户在未登录状态下不能进入该页面
    # 以上，我们把门关上了，那么它的实现逻辑是怎么样的呢？为什么我们在这里只加一个装饰器就可以控制访问了呢？
    # 有一个核心代码在第37行，当我们登录成功的时候，调用了auth.login(request, user)方法，这个方法的作用是什么呢？是到数据库里面去写session_key

# 以上登录的功能就实现了，那么，登录之后也需要一个退出按钮来退出登录；
# 首先，在登录成功的manage.html上加一个logout按钮，然后在urls.py文件中增加logout的路径；然后在视图文件中定义logout，并调用认证里面的logout函数
# 退出系统之后，我们要能够回到原来的登录页面，因此还需要加上退出之后的重定向地址，退回到index页面

def logout(request):
    """
    退出登录
    """
    auth.logout(request)        # 退出成功后，到数据库中删除session，下一次只能登录后访问，不能直接访问manage页面了
    return HttpResponseRedirect("/index/")

