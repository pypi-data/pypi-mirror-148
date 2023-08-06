from setuptools import setup

"""
源码打包/安装步骤(不需要考虑跨平台、Pyhton版本问题)：
1.终端切换到当前目录；
2.执行命令打包：python3 setup.py sdist
3.将当前目录下dist文件夹下的压缩包corecommons-1.0.0.tar.gz复制到服务器中
4.执行安装命令: pip install kccommons-1.0.0.tar.gz

# 上传包
1.pip安装twine
2.关闭终端，重新打开终端，切换到dist目录
3.执行命令：twine upload kccommons-1.0.0.tar.gz
"""
REQUIREMENTS = open('requirements.txt').readlines()
setup(
    # 打包时的包名
    name="kccommons",
    # 版本
    version="1.0.0",
    description="常用工具包",
    author='LiYanAn',
    author_email='liyanan2010@sina.cn',
    # 需要打包的包(也就是当前根目录下的文件夹)，安装时会将这里出现的包文件夹以及这个包下的文件放在site-packages目录下
    # 当使用时:"import 这里出现的包名"
    packages=["kccommons"],
    # 需要打包的单文件模块, 这里的单文件模块安装时，会直接放在site-packages目录下
    # 当使用时:"import 这里出现的单文件模块名"
    py_modules=[""],
    include_package_data=True,
    # python版本
    python_requires='>=3.7.0',
    # 依赖包
    install_requires=REQUIREMENTS
)
