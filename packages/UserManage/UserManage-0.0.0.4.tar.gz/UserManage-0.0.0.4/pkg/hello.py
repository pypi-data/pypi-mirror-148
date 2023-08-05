"""UserManage
Usage:
  user_manage user (add|delete) (<name>) [<password>  --authority=<authority>]
  user_manage change_name <name>
  user_manage change_pwd <password>
  user_manage add_description <description>...
  user_manage -h | --help
  user_manage --version

Options:
  -h --help     帮助.
  -v --version     查看版本号.
  --authority=<authority>  权限设置 [default: user].
  --group=<group>      分组
"""

from docopt import docopt
__version__ = "0.0.0.4"

def cmd():
    arguemnts = docopt(__doc__,version=__version__)
    if arguemnts.get("add"):
        print("添加用户成功")
    elif arguemnts.get("delete"):
        print("删除用户成功")
    elif arguemnts.get("change_name"):
        print("修改名字成功")
    elif arguemnts.get("change_pwd"):
        print("修改密码成功")
    elif arguemnts.get("add_description"):
        print("添加用户描述成功")

if __name__ == "__main__":
    cmd()