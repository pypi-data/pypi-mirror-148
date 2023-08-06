# -*- coding: utf-8 -*-
""" pcsget: the spider for pcs-protocol """

__author__ = "zhoujianwei.garen"

import os.path
import sys

import config
import log
import sync


def execute():
    reload(sys)
    sys.setdefaultencoding("utf-8")
    log.init()
    args = sys.argv
    log.d("main invoke, args:" + str(args))
    base_dir = os.path.abspath("..")
    arg_len = len(args)
    if arg_len > 3:
        log.e("sorry, incorrect number of parameters. ")
        log.e("please checkout something useful by '--help'.")
        return
    # 未输入参数，默认更新当前目录层级的协议
    if arg_len <= 1:
        sync.sync_dir(base_dir)
        return
    option = args[1]
    if option == "--help" or option == "-help":
        _print_help()
        return
    if option == "--version" or option == "-v":
        _print_version()
        return
    if option.startswith("--set-"):
        k = option.replace("--set-", "")
        v = args[2]
        config.setup_config(k, v)
        return
    if option == "-f" or option == "--feat":
        sync.sync_demand(args[2])
        return
    if option == "-n" or option == "--name":
        sync.sync_names(args[2])
        return
    if option == "-u" or option == "--update":
        sync.sync_dir(base_dir)
        return
    log.w("输入的参数暂不支持，请输入--help查看")


def _print_help():
    print("pcsget [option] <param_value>")
    print("options:")
    print("     none,               - 无选项，更新当前目录层级已存在的协议")
    print("     -u, --update,       - 更新当前目录层级已存在的协议")
    print("     -f, --feat,         - 按需求编号同步协议")
    print("     -n, --name,         - 按协议名称同步协议，如有多个协议名按英文逗号拼接")
    print("     --set-token,        - 可选项，协议管理系统的csrftoken, 用于维持登录状态，可从浏览器开发者工具中查看Header获取")
    print("     --set-session,      - 可选项，协议管理系统的sessionid, 用于维持登录状态，可从浏览器开发者工具中查看Header获取")
    print("     --set-user,         - 可选项，用户名（oa账号），用于cookie过期时的自动登录")
    print("     --set-password,     - 可选项，密码，用于cookie过期时的自动登录")
    print("     --set-lang,         - 协议文件格式，可选：java(默认), kotlin, kotlin-marshallize(TODO)，swift(TODO), oc(TODO)")
    print("     -h, --help,         - 帮助")
    print("     -v, --version,      - 查看版本")


def _print_version():
    print("0.9.0")
    print("2022-4-29")
    print("based on Python2.7")


if __name__ == '__main__':
    execute()
