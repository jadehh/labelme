#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @File     : packing.py
# @Author   : jade
# @Date     : 2021/12/12 12:28
# @Email    : jadehh@1ive.com
# @Software : Samples
# @Desc     :
from jade import *
def zip_lib_package(args):
    install_path = os.path.join(os.getcwd(),
                                "releases/{}/{}".format(args.name + "V" + args.app_version, getOperationSystem()))
    if getOperationSystem() == "Windows":
        zip_file(os.path.join(install_path,args.lib_path),os.path.join("Output/{}".format("Windows_lib32.zip")))
    elif getOperationSystem() == "Darwin":
        pass
    else:
        zip_file(os.path.join(install_path,args.lib_path),os.path.join("Output/{}_lib64.zip".format(getOperationSystem())))


if __name__ == '__main__':
    import argparse
    lib_path = "labelme_lib32"
    parser = argparse.ArgumentParser()
    parser.add_argument('--extra_sys_list', type=str,
                        default="")  ## 需要额外打包的路径
    parser.add_argument('--scripts_path', type=str,
                        default="")  ## 打包成一个完成的包
    parser.add_argument('--full', type=str,
                        default="False")  ## 打包成一个完成的包
    parser.add_argument('--extra_path_list', type=list,
                        default=["translate","config"])
    parser.add_argument('--lib_path', type=str, default=lib_path)  ## 是否lib包分开打包
    parser.add_argument("--head_str", type=str, default="from jade import *\n"
                                                        "update_lib('/tmp/{}')\n"
                                                        "import colorama\n"
                                                        "colorama.init()\n".format(lib_path))
    parser.add_argument('--use_jade_log', type=str,
                        default="True")  ##是否使用JadeLog

    parser.add_argument('--console', type=str,
                        default="False")  ## 是否显示命令行窗口,只针对与Windows有效
    parser.add_argument("--app_version", type=str, default=get_app_version())  ## 版本号
    parser.add_argument('--app_name', type=str,
                        default="labelme")  ##需要打包的文件名称
    parser.add_argument('--name', type=str,
                        default="labelme")  ##需要打包的文件名称
    parser.add_argument('--appimage', type=str,
                        default="True")  ## 是否打包成AppImage
    parser.add_argument('--is_auto_packing',type=str,default="False") ##是否自动打包
    parser.add_argument('--is_qt', type=str, default="True")  ## qt 会将controller view src 都进行编译
    parser.add_argument('--specify_files', type=str, default="")  ## 指定编译的文件
    args = parser.parse_args()
    ui_to_py(args)
    build(args)
    packAPP(args)
    install_path = os.path.join(os.getcwd(),
                                "releases/{}/{}".format(args.name + "V" + args.app_version, getOperationSystem()))
    ouput_name = get_app_name(args) + "_setup" + "-V" + args.app_version[:-2] + "-" + args.app_version[
                -1]
    packSetup(args, install_path, "{{7676530c-374a-11ee-a5ce-220db03570cb}", ouput_name)
    zip_lib_package(args)



