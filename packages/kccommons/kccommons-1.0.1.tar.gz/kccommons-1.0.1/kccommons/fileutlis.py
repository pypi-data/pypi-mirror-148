import os
import shutil

"""
 文件相关的工具方法
"""


def is_file(file: str) -> bool:
    """
    是否是合法的且存在的文件

    :param file: 字符串,可以是目录路径、可以是含文件名的路径、可以是绝对路径、可以是相对路径
    :return: 如果是合法且存在的文件则为True，否则为False
    """
    return os.path.isfile(file)


def is_file_exists(file: str) -> bool:
    """
    文件是否存在，如果不是文件则返回False，如果不存在则返回False，如果是文件且存在则返回True

    :param file: 字符串,可以是目录路径、可以是含文件名的路径、可以是绝对路径、可以是相对路径
    :return:
    """
    isfile = is_file(file)
    if not isfile:
        return False
    return os.path.exists(file)


def delete_file(file: str):
    """
    删除一个文件

    :param file: 需要删除的文件
    """
    if os.path.isdir(file):
        raise ValueError("删除文件失败，不能删除文件夹, 参数:" + file)
    if not is_file_exists(file):
        return
    try:
        os.remove(file)
    except FileNotFoundError as exception:
        pass


def rename_file(file: str, new_name: str):
    """
    重命名文件

    :param file: 源文件
    :param new_name: 新的文件名，注意不能存在路径
    """
    if new_name != os.path.basename(new_name):
        raise ValueError("重命名文件失败，新文件名不能存在路径, 参数:" + new_name)
    if not os.path.exists(file):
        raise ValueError("重命名文件失败，文件不存在, 参数:" + file)
    if not is_file(file):
        raise ValueError("重命名文件失败，参数不是文件, 参数:" + file)
    os.rename(file, new_name)


def copy_file(src_file: str, dest_file: str):
    """
    复制单个文件，如果目的路径中存在同名的文件则会覆盖

    :param src_file: 源文件，可以是绝对路径、也可以是相对路径
    :param dest_file: 目的文件，可以是绝对路径、也可以是相对路径，路径中必须含有文件，如果父级文件夹不存在则会抛出异常
    :return:
    """
    if not is_file_exists(src_file):
        raise ValueError("复制文件失败，源文件不存在, 参数:" + src_file)
    dest_abspath = os.path.abspath(dest_file)
    src_abspath = os.path.abspath(src_file)
    if dest_abspath == src_abspath:
        return
    dest_dir = os.path.dirname(dest_abspath)
    if not os.path.exists(dest_dir):
        raise ValueError("复制文件失败，目的文件夹不存在, 参数:" + dest_dir)
    if os.path.isdir(dest_abspath):
        raise ValueError("复制文件失败，缺少目的文件参数, 参数:" + dest_file)
    dest_base_name = os.path.basename(dest_abspath)
    if dest_base_name is None or dest_base_name.strip() == '':
        raise ValueError("复制文件失败，缺少目的文件参数, 参数:" + dest_file)
    shutil.copyfile(src_file, dest_file)


def move_file(src_file: str, dest: str):
    """
    移动文件\n
    1.dest的os.path.abspath如果是已存在的文件夹，则文件会移动到dest文件夹下，文件名不变；\n
    2.dest的os.path.abspath如果是已存在的文件，则文件会覆盖，文件名是dest的文件名；\n
    3.dest的os.path.abspath如果是不存在的文件，则文件会移动到os.path.dirname(dest_abspath)文件夹下，文件名是dest的文件名；\n
    :param src_file:
    :param dest:
    :param overwrite:
    :return:
    """
    if not is_file_exists(src_file):
        raise ValueError("移动文件失败，源文件不存在, 参数:" + src_file)
    dest_abspath = os.path.abspath(dest)
    # 判断目的文件夹是否存在
    if not os.path.exists(os.path.dirname(dest_abspath)):
        raise ValueError("移动文件失败，文件夹不存在, 参数:" + os.path.dirname(dest_abspath))
    shutil.move(src_file, dest)
