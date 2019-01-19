from django.shortcuts import redirect


# 将验证登录的方法写成装饰器,在每次进行验证session中的数据
def check_login(func):
    def verify_login(request, *args, **kwargs):
        # 判断是否登录
        # 根据session里面的id 判断
        if request.session.get('ID') is None:
            # 跳转到登录
            return redirect('用户:用户登录')
        else:
            # 调用原函数
            return func(request, *args, **kwargs)

    # 返回新函数
    return verify_login
