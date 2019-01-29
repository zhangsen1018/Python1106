from django.http import JsonResponse
from django.shortcuts import render

# Create your views here.
from django_redis import get_redis_connection

from DB.base_view import BaseVerifyView
from goods.models import GoodsSKU
from cart.helper import json_msg, get_cart_count


class AddCartView(BaseVerifyView):
    def get(self, request):
        pass

    # 操作购物车, 添加购物车数据
    """
        1. 需要接收的参数
            sku_id count 
            从session中获取用户id

        2. 验证参数合法性
            a. 判断 为整数
            b. 要在数据库中存在商品
            c. 验证库存是否充足

        3. 操作数据库
            将购物车 保存到redis
            存储的时候采用的数据库类型为hash
            key           field value  field value
            cart_user_id  sku_id count

    """

    def post(self, request):
        # 1. 接收参数
        user_id = request.session.get("ID")
        sku_id = request.POST.get("sku_id")
        count = request.POST.get("count")

        # a.判断为整数 , 因为数据是二进制的数据要转换
        try:
            sku_id = int(sku_id)
            count = int(count)
        except:
            return JsonResponse(json_msg(1, "参数错误!"))
        # b.要在数据库中存在商品 count必须大于0
        try:
            goods_sku = GoodsSKU.objects.get(pk=sku_id)
        except GoodsSKU.DoesNotExist:
            return JsonResponse(json_msg(2, "商品不存在!"))

        # 判断库存
        if goods_sku.stock < count:
            return JsonResponse(json_msg(3, "库存不足!"))

        # 2. 操作数据  购物车加入数量(count),当前商品ID(sku_id)
        # 创建连接
        r = get_redis_connection()
        # 处理购物车的 key
        cart_key = f"cart_{user_id}"

        # 添加
        # 获取购物车中已经存在的数量 加 上 需要添加 与 库存进行比较
        old_count = r.hget(cart_key, sku_id)  # 二进制
        if old_count is None:
            old_count = 0
        else:
            old_count = int(old_count)

        if goods_sku.stock < old_count + count:
            return JsonResponse(json_msg(3, "库存不足!"))

        # 将商品添加到购物车
        # r.hset(cart_key,sku_id,old_count + count)
        # ctrl + shift + u
        r.hincrby(cart_key, sku_id, count)

        # 获取购物车中的总数量
        cart_count = get_cart_count(request)

        # 3. 合成响应
        return JsonResponse(json_msg(0, "添加购物车成功", data=cart_count))


class ShopCartView(BaseVerifyView):
    #   购物车显示页面
    def get(self, request):
        # 获取购物车中的商品信息
        goods_sku = GoodsSKU.objects.filter(is_delete=False)
        #  sku_id count
        # 先获取sku_id, 在查询获取商品的完整信息
        # 计算总价格
        # 连接数据库 默认配置
        r = get_redis_connection("default")
        # 获取redis中的sku_id count 商品的数量
        user_id = request.session.get("ID")
        # cart_key = "cart_{}".format(request.session.get('ID'))
        cart_key = f"cart_{user_id}"
        # 获取
        cart_data = r.hgetall(cart_key)  # 字典, 键和值都二进制编码
        # 遍历得到的数据字典
        # 使用一个变量保存商品
        goodsskus = []
        for sku_id, count in cart_data.items():
            sku_id = int(sku_id)
            count = int(count)

            # 查询商品的完整信息
            goodssku = GoodsSKU.objects.get(pk=sku_id)

            # 将count保存到 商品对象上(对象上添加一个自定义的属性)
            goodssku.count = count

            # 保存到列表
            goodsskus.append(goodssku)

        # 渲染数据到页面
        context = {
            "goodsskus": goodsskus,
            "goods_sku": goods_sku,

        }

        return render(request, "cart/shopcart.html", context)

    def post(self, request):
        pass
