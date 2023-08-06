# coding=<encoding name> ： # coding=utf-8
# 名称：启动-转换-写入文件
# 此文件为第一文件，即启动文件

import os
import sys
import subprocess
from fzq_scnu import fzrunner

# 这里储存你需要转换的原码语句（关键词，库名，类或函数名）以及它转换后的仿真语句（关键词，库名，类或函数名）
tra_string = {'from control import': 'from control import',
              'control': 'fzq_scnu.fzcontrol',
              'gpio': 'fzgpio',
              'from fzq_scnu import change': '',
              'import sys': '',
              'change.go()': '',
              'change.files_path': '',
              'sys.exit()': '',
              'code_path = os.path.realpath(sys.argv[0])': '',
              'fzq = change.Create(': '#(',
              'fzq.background': '#',
              'fzq.racetrack': '#',
              'fzq.level': '#',
              'fzq.go()': ''
              }

# fzrunner_path = tools.path_processing(fzq_scnu.__file__, -1, 'fzrunner.py')
fzrunner_path = fzrunner.__file__  # 库中fzrunner的路径
code_path = sys.argv[0]  # 运行脚本的绝对路径
emulator_path = os.path.abspath(os.path.dirname(sys.argv[0])) + '\\Hardware_emulator.py'  # 运行脚本所在目录的绝对路径
main_path = r'/home/pi/class'  # 读取和保存文件所用主文件夹（树莓派上）
system_platform = sys.platform    # 用于判断系统是否为win
if 'win' in system_platform:
    current_path = os.getcwd()    # 获取当前文件（exe）的位置
    main_path = current_path + r'/resources/assets/class'
files_path = main_path + r'/emulator_files'  # 仿真器所需文件路径


class Create:
    def __init__(self, level='', code_p=code_path, emulator_p=emulator_path, files_p=files_path):
        self.code_path = code_p
        self.emulator_path = emulator_p
        self.files_path = files_p
        self.new_codes = list()
        self.level = level  # 设置关卡
        # 读入第二文件，即图形化编程软件编程生成的原代码文件（以下代码关键位置：原代码文件名）
        # 对必要原码语句进行更改
        with open(self.code_path, 'r', encoding='utf-8') as r:
            ori_codes = r.read().splitlines()
            for line in ori_codes:
                if line:
                    for key, value in tra_string.items():
                        if key in line:
                            line = line.replace(key, value)
                            break
                    self.new_codes.append(line)
        try:
            sys.path.append(files_path)
        except Exception as result:
            print(result)
        import constants

    def change(self):
        # 读入第三文件，即仿真器运行文件（核心文件）
        with open(fzrunner_path, 'r', encoding='utf-8') as r:
            fzlines = r.readlines()

        # 生成新文件，即新仿真器运行文件（最终文件）
        # 生成的仿真器运行文件名，可自行设置.(以下代码关键位置：新文件名、判断仿真代码插入点的第一条if语句)
        with open(self.emulator_path, 'w', encoding='utf-8') as w:
            for fzline in fzlines:
                if '    files_path = \'\'\n' == fzline:
                    if '\\' in self.files_path:
                        self.files_path = self.files_path.replace('\\', '/')
                        if '//' in self.files_path:
                            self.files_path = self.files_path.replace('//', '/')
                    intact_path = '    files_path = "' + self.files_path + '/"\n'
                    w.write(intact_path)
                elif 'run = \'\'\n' == fzline:
                    w.write('run = \'1\'\n')
                elif '    LEVEL = constants.Level()\n' == fzline:
                    line1 = '    LEVEL = constants.Level' + self.level + '()\n'
                    w.write(line1)
                elif '        try:\n' == fzline:
                    w.write(fzline)
                    for new_code in self.new_codes:
                        new_code = '            ' + new_code + '\n'
                        w.write(new_code)
                elif '\'\'\'' in fzline:
                    pass
                else:
                    w.write(fzline)

    def go(self):
        try:
            self.change()
        except Exception as result:
            print(result)
            sys.exit(0)

        # 运行新仿真器运行文件，得到仿真器
        # emulator_path = tools.path_processing(self.code_path, -1, "Hardware_emulator.py")
        # 用shell执行（避免用pycharm等其他软件打开）
        subprocess.call("python \"{}\"".format(self.emulator_path), shell=True)  # 法一
        # os.system("python \"{}\"".format(self.emulator_path))  # 法二
        sys.exit(0)
