import os
import shutil

"""
 文件夹相关的工具方法
"""


def is_dir(dir_str: str) -> bool:
    """
    是否是合法的且存在的目录

    :param dir_str: 目录字符串
    :return: 如果是合法且存在的字符串则为True，否则为False
    """
    return os.path.isdir(dir_str)


def is_dir_exists(dir_str: str) -> bool:
    """
    文件夹是否存在，如果不是文件夹则返回False，如果不存在则返回False，如果是文件夹且存在则返回True

    :param dir_str: 字符串,可以是目录路径、可以是含文件名的路径、可以是绝对路径、可以是相对路径
    :return:
    """
    isdir = is_dir(dir_str)
    if not isdir:
        return False
    return os.path.exists(dir_str)


def get_current_working_dir() -> str:
    """
     获取当前的工作目录，即当前路径，相当于Linux的pwd命令
    """
    return os.getcwd()


def change_current_working_dir(dest_dir: str) -> bool:
    """
    切换当前的工作目录

    :param dest_dir: 目标目录
    """
    isdir = is_dir(dest_dir)
    if not isdir:
        return False
    os.chdir(dest_dir)
    return True


def create_dir(dir_str: str) -> None:
    """
    创建文件夹，注意父层级问价夹必须存在,如果不存在会抛出异常

    :param dir_str: 文件夹路径，可以是相对路径或者绝对路径
    :return:
    """
    abspath = os.path.abspath(dir_str)
    dirname = os.path.dirname(abspath)
    if not os.path.isdir(dirname):
        raise ValueError("创建文件夹失败，文件夹不存在:" + dirname)
    if os.path.exists(abspath) and os.path.isdir(abspath):
        raise ValueError("创建文件夹失败，文件夹已经存在:" + dirname)
    os.mkdir(dir_str)


def create_dirs(dir_str: str) -> None:
    """
    创建文件夹，注意父层级问价夹如果不存在，则会递归创建，如果文件夹已经存在，不会抛出异常

    :param dir_str: 文件夹路径，可以是相对路径或者绝对路径
    :return:
    """
    os.makedirs(dir_str, exist_ok=True)


def delete_empty_dir(dir_str: str) -> None:
    """
    删除一个空文件夹，如果不是文件夹、或者文件夹不为空会抛出异常

    :param dir_str:
    :return:
    """
    if os.path.isfile(dir_str):
        raise ValueError("删除文件夹失败，不能删除文件, 参数:" + dir_str)
    if not is_dir_exists(dir_str):
        return
    # 判断文件夹是否为空
    child_files = os.listdir(dir_str)
    if len(child_files) > 0:
        raise ValueError("删除文件夹失败，文件夹不为空, 参数:" + dir_str)
    os.rmdir(dir_str)


def delete_dirs_force(dir_str: str) -> None:
    """
    递归强制删除当前文件夹、当前文件夹下的所有文件及文件夹

    :param dir_str:
    :return:
    """
    if not os.path.exists(dir_str):
        return
    if not is_dir(dir_str):
        raise ValueError("删除文件夹失败，不是文件夹, 参数:" + dir_str)
    shutil.rmtree(dir_str)


def copy_dir_recursion(src_dir: str, dest_dir: str) -> None:
    """
    递归复制文件夹：将src_dir文件夹下所有内容递归的复制到dest_dir文件夹下。
    1.当dest_dir文件夹存在时，不会报错，并且会强制覆盖dest_dir文件夹下同名的文件(dirs_exist_ok=True)；
    2.当dest_dir文件夹不存在时，会自动创建文件夹

    :param src_dir: 原文文件夹
    :param dest_dir: 目的文件夹
    :return:
    """
    src_abspath = os.path.abspath(src_dir)
    dest_abspath = os.path.abspath(dest_dir)
    if dest_abspath == src_abspath:
        return
    if not os.path.isdir(src_abspath):
        raise ValueError("复制文件夹失败，不是文件夹, 参数:" + src_abspath)
    if os.path.exists(dest_abspath) and os.path.isfile(dest_abspath):
        raise ValueError("复制文件夹失败，不是文件夹, 参数:" + dest_abspath)
    shutil.copytree(src_dir, dest_dir, ignore_dangling_symlinks=True, dirs_exist_ok=True)


def move_dir(src_dir: str, dest_dir: str):
    """
    移动文件夹\n
    1.如果dest_dir文件夹不存在，则会"递归"创建文件夹，并将src_dir文件夹"下"的所有文件、文件夹 移动到 dest_dir的文件夹下;\n
    2.如果dest_dir文件夹存在，则会将src_dir "这个文件夹" 移动到 dest_dir的文件夹下；\n
    3.如果dest_dir是一个存在的文件，会抛出异常

    :param src_dir:
    :param dest_dir:
    :return:
    """
    src_abspath = os.path.abspath(src_dir)
    dest_abspath = os.path.abspath(dest_dir)
    if not os.path.exists(src_abspath):
        raise ValueError("复制文件夹失败，源文件夹不存在, 参数:" + src_abspath)
    if not os.path.isdir(src_abspath):
        raise ValueError("复制文件夹失败，不是文件夹, 参数:" + src_abspath)
    if os.path.exists(dest_abspath) and os.path.isfile(dest_abspath):
        raise ValueError("复制文件夹失败，不是文件夹, 参数:" + dest_abspath)
    shutil.move(src_dir, dest_dir)
