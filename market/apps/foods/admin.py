from django.contrib import admin
# 引入模型
from foods.models import GoodsClassModel, GoodsSKUModel, GoodsSPUModel, UnitModel, BannerModel, ActivityModel


# 首页活动表
@admin.register(ActivityModel)
class ActivityModelAdmin(admin.ModelAdmin):
    list_per_page = 4  #: 每页显示条数

    actions_on_top: True  # 操作是否在上面显示, 默认  True  ,反正两个相反
    actions_on_bottom: True  # 操作是否在下面显示, 默认   False

    # 自定义显示列，在models类中对字段有方法的就填方法名
    list_display = ['id', 'activityName', 'imgUrl', 'urlUrl']

    # 设置在列表页字段上添加一个 a标签, 从而进入到编辑页面,在models类中对字段有方法的就填方法名
    list_display_links = ['id', 'activityName', 'imgUrl', 'urlUrl']

    # 列表右侧栏过滤器,只能写一个
    list_filter = ['activityName']

    # 搜索框,搜索字段 也只能写一个
    search_fields = ['activityName']

    # fields = []: 定义在添加或者编辑的时候操作哪些字段，一般不设

    # 对可编辑区域分组,列表里面的字段填写模型的属性，
    fieldsets = (
        ('活动名称', {"fields": ['activityName']}),
        ('图片地址', {"fields": ['imgUrl']}),
        ('url地址', {"fields": ['urlUrl']}),
    )


# 首页轮播商品表
@admin.register(BannerModel)
class RotationModelAdmin(admin.ModelAdmin):
    list_per_page = 4  #: 每页显示条数

    actions_on_top: True  # 操作是否在上面显示, 默认  True  ,反正两个相反
    actions_on_bottom: True  # 操作是否在下面显示, 默认   False

    # 自定义显示列，在models类中对字段有方法的就填方法名
    list_display = ['id', 'bannerName', 'goodsSKU', 'goodsImg', 'bannerOrder', 'Create_time', 'update_time',
                    'is_delete']

    # 设置在列表页字段上添加一个 a标签, 从而进入到编辑页面,在models类中对字段有方法的就填方法名
    list_display_links = ['id', 'bannerName', 'goodsSKU', 'goodsImg', 'bannerOrder', 'Create_time', 'update_time',
                          'is_delete']

    # 列表右侧栏过滤器,只能写一个
    list_filter = ['bannerName']

    # 搜索框,搜索字段 也只能写一个
    search_fields = ['bannerName']

    # fields = []: 定义在添加或者编辑的时候操作哪些字段，一般不设

    # 对可编辑区域分组,列表里面的字段填写模型的属性，
    fieldsets = (
        ('名称', {"fields": ['bannerName']}),
        ('商品SKUID', {"fields": ['goodsSKU']}),
        ('图片地址', {"fields": ['goodsImg']}),
        ('排序', {"fields": ['bannerOrder']}),
    )


# 商品SKU表
@admin.register(GoodsSKUModel)
class GoodsSKUModelAdmin(admin.ModelAdmin):
    list_per_page = 4  #: 每页显示条数

    actions_on_top: True  # 操作是否在上面显示, 默认  True  ,反正两个相反
    actions_on_bottom: True  # 操作是否在下面显示, 默认   False

    # 自定义显示列，在models类中对字段有方法的就填方法名
    list_display = ['id', 'goodsname', 'goodsbrief', 'price', 'stock', 'sales', 'goodslogo', 'shelves',
                    'goodsclass_id', 'spu_id', 'unit', 'Create_time', 'update_time', 'is_delete']

    # 设置在列表页字段上添加一个 a标签, 从而进入到编辑页面,在models类中对字段有方法的就填方法名
    list_display_links = ['id', 'goodsname', 'goodsbrief', 'price', 'stock', 'sales', 'goodslogo', 'shelves',
                          'goodsclass_id', 'spu_id', 'unit', 'Create_time', 'update_time', 'is_delete']

    # 列表右侧栏过滤器,只能写一个
    list_filter = ['goodsname']

    # 搜索框,搜索字段 也只能写一个
    search_fields = ['goodsname']

    # fields = []: 定义在添加或者编辑的时候操作哪些字段，一般不设

    # 对可编辑区域分组,列表里面的字段填写模型的属性，
    fieldsets = (
        ('商品名', {"fields": ['goodsname']}),
        ('商品简介', {"fields": ['goodsbrief']}),
        ('价格', {"fields": ['price']}),
        ('库存', {"fields": ['stock']}),
        ('销量', {"fields": ['sales']}),
        ('LOGO地址', {"fields": ['goodslogo']}),
        ('是否上架', {"fields": ['shelves']}),
        ('商品分类ID', {"fields": ['goodsclass_id']}),
        ('商品spu_id', {"fields": ['spu_id']}),
        ('单位id', {"fields": ['unit']}),
    )


# 商品SPU表
@admin.register(GoodsSPUModel)
class GoodsSPUModelAdmin(admin.ModelAdmin):
    list_per_page = 4  #: 每页显示条数

    actions_on_top: True  # 操作是否在上面显示, 默认  True  ,反正两个相反
    actions_on_bottom: True  # 操作是否在下面显示, 默认   False

    # 自定义显示列，在models类中对字段有方法的就填方法名
    list_display = ['id', 'SPU_name', 'SPU_details']

    # 设置在列表页字段上添加一个 a标签, 从而进入到编辑页面,在models类中对字段有方法的就填方法名
    list_display_links = ['id', 'SPU_name', 'SPU_details']

    # 列表右侧栏过滤器,只能写一个
    list_filter = ['SPU_name']

    # 搜索框,搜索字段 也只能写一个
    search_fields = ['SPU_name']

    # fields = []: 定义在添加或者编辑的时候操作哪些字段，一般不设

    # 对可编辑区域分组,列表里面的字段填写模型的属性，
    fieldsets = (
        ('SPU名', {"fields": ['SPUname']}),
        ('SPU简介', {"fields": ['SPUdetails']}),
    )




# 商品单位表
@admin.register(UnitModel)
class UnitModelAdmin(admin.ModelAdmin):
    list_per_page = 4  #: 每页显示条数

    actions_on_top: True  # 操作是否在上面显示, 默认  True  ,反正两个相反
    actions_on_bottom: True  # 操作是否在下面显示, 默认   False

    # 自定义显示列，在models类中对字段有方法的就填方法名
    list_display = ['id', 'unitname', 'Create_time', 'update_time', 'is_delete']

    # 设置在列表页字段上添加一个 a标签, 从而进入到编辑页面,在models类中对字段有方法的就填方法名
    list_display_links = ['id', 'unitname', 'Create_time', 'update_time', 'is_delete']

    # 列表右侧栏过滤器,只能写一个
    list_filter = ['unitname']

    # 搜索框,搜索字段 也只能写一个
    search_fields = ['unitname']


# 商品分类表
@admin.register(GoodsClassModel)
class GoodsClassModelAdmin(admin.ModelAdmin):
    list_per_page = 4  #: 每页显示条数

    actions_on_top: True  # 操作是否在上面显示, 默认  True  ,反正两个相反
    actions_on_bottom: True  # 操作是否在下面显示, 默认   False

    # 自定义显示列，在models类中对字段有方法的就填方法名
    list_display = ['id', 'classname', 'classbrief', 'Create_time', 'update_time', 'is_delete']

    # 设置在列表页字段上添加一个 a标签, 从而进入到编辑页面,在models类中对字段有方法的就填方法名
    list_display_links = ['id', 'classname', 'classbrief', 'Create_time', 'update_time', 'is_delete']

    # 列表右侧栏过滤器,只能写一个
    list_filter = ['classname']

    # 搜索框,搜索字段 也只能写一个
    search_fields = ['classname']

    # fields = []: 定义在添加或者编辑的时候操作哪些字段，一般不设

    # 对可编辑区域分组,列表里面的字段填写模型的属性，
    fieldsets = (
        ('分类名', {"fields": ['classname']}),
        ('分类简介', {"fields": ['classbrief']}),
    )


