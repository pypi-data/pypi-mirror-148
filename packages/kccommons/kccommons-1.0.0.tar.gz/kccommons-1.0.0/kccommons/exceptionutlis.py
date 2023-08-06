# 自定义异常

# 参数异常
class ArgumentException(RuntimeError):
    def __init__(self, *args, **kwargs):
        pass
