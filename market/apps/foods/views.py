from django.shortcuts import render
from django.views import View


# Create your views here.


# 商品首页

class Index(View):
    # def post(self,request):
    #     return HttpResponse('商品首页post')
    def get(self, request):
        return render(request, 'foods/index.html')


# 商品分类(商品列表)
class Category(View):
    # def post(self,request):
    #     return HttpResponse('商品分类post')
    def get(self, request):
        return render(request, 'foods/category.html')


# 商品详情
class Detail(View):
    # def post(self,request):
    #     return HttpResponse('商品分类post')
    def get(self, request):
        return render(request, 'foods/detail.html')
