import hashlib


# 创建一个哈希加密方法
def set_password(password):
    # 加密方法
    h = hashlib.md5(password.encode('utf-8'))
    # 返回 加密后的字符串
    return h.hexdigest()
