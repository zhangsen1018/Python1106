from django.shortcuts import render

# Create your views here.
from django.shortcuts import render
from django.views import View

from goods.models import GoodsSKU, Category


class IndexView(View):
    # 商品首页

    def get(self, request):
        return render(request, 'goods/index.html')


class CategorView(View):
    # 商品分类

    #
    # 1. 页面刚加载的时候 显示的商品只 显示 排序 排第一的分类下的商品
    # 2. 点击哪个分类 就显示 对应分类下的商品
    # 3. 可以按照 销量,价格(降,升),添加时间,综合(pk) 排序 并且 是对应分类下的商品
    #     添加一个参数order:
    #         0: 综合
    #         1: 销量降
    #         2: 价格升
    #         3: 价格降
    #         4: 添加时间降
    #     order_rule = ['pk', '-sale_num', 'price', '-price', '-create_time']

    def get(self, request, cate_id, order):
        # 查询所有的分类 默认为0
        categorys = Category.objects.filter(is_delete=False).order_by("-order")

        # 取出第一个分类
        # print(categorys[0])
        # print(categorys.first())
        # 如果 cate_id 为空的话, 默认等于 分类的id
        if cate_id == "":
            category = categorys.first()
            cate_id = category.pk
        else:
            # 根据分类id查询对应的分类
            cate_id = int(cate_id)
            category = Category.objects.get(pk=cate_id)

        # 查询对应类下的所有商品
        # print(category.goodssku_set.all())
        goods_skus = GoodsSKU.objects.filter(is_delete=False, category=category)

        # 排序默认为 0 如果输入为空 那么等于 0
        if order == "":
            order = 0

        # 因为传入的排序是字符串类型,要转换为数字类型
        order = int(order)

        # 排序规则列表
        order_rule = ['pk', '-sale_num', 'price', '-price', '-create_time']
        # 排序通过上面的列表
        goods_skus = goods_skus.order_by(order_rule[order])
        # if order == 0:
        # 当排序等于0 时, 通过id来排序,-->综合
        #     goods_skus = goods_skus.order_by("pk")
        # elif order == 1:
        # 当排序等于1 时, 通过id来排序,-->销量
        #     goods_skus = goods_skus.order_by("-sale_num")
        # elif order == 2:
        # 当排序等于2 时, 通过id来排序,-->价格升序
        #     goods_skus = goods_skus.order_by("price")
        # elif order == 3:
        # 当排序等于0 时, 通过id来排序,-->价格降序
        #     goods_skus = goods_skus.order_by("-price")
        # elif order == 4:
        # 当排序等于0 时, 通过id来排序,-->最新数据的新品
        #     goods_skus = goods_skus.order_by("-create_time")

        context = {
            'categorys': categorys,
            'goods_skus': goods_skus,
            'cate_id': cate_id,
            'order': order,
        }

        return render(request, 'goods/category.html', context=context)


class DetailView(View):
    """商品详情"""

    def get(self, request, id):
        # 获取商品sku的信息
        goods_sku = GoodsSKU.objects.get(pk=id)

        # 渲染页面
        context = {
            'goods_sku': goods_sku,
        }
        return render(request, 'goods/detail.html', context=context)
