# coding=<encoding name> ： # coding=utf-8
import sys
import os
from fzq_scnu import constants_download

main_path = '/home/pi/class/'  # 读取和保存文件所用主文件夹
system_platform = sys.platform    # 用于判断系统是否为win
if 'win' in system_platform:
    current_path = os.getcwd()    # 获取当前文件（exe）的位置
    main_path = current_path + r'/resources/assets/class'
files_path = main_path + r'/emulator_files'  # 仿真器所需文件路径
constants_file_path = files_path + r'/constants.py'
if not os.path.exists(constants_file_path):
    if not os.path.exists(files_path):
        os.makedirs(files_path)
    with open(constants_download.__file__, 'r', encoding='utf-8') as r:
        lines = r.readlines()
    with open(constants_file_path, 'w', encoding='utf-8') as w:
        w.writelines(lines)
try:
    sys.path.append(files_path)
    import constants as con
except Exception as result:
    from fzq_scnu import constants_download as con
    print(constants_file_path)
    print(result)
    print("Failed to import constants!（导入模块失败）")

# 参数
# --------------------------------------------------------------------------------------------------------
# 屏幕宽度，高度
# 代表现实场景中的长3000mm， 宽2167mm
WIDTH, HEIGHT = con.WIDTH, con.HEIGHT
# 中间区域Rect((200, 6), (900, 650))， 宽900px， 高650px。中心坐标(650, 331)
background_rect = con.background_rect
# TITLE
TITLE = con.TITLE
# ICON
ICON = con.ICON
# --------------------------------------------------------------------------------------------------------
# 主角运动速度比例(现实速度设置1，代表1mm每秒)
speed_setting = con.speed_setting  # 每秒40帧，则有0.0075*40 = 0.3px每秒 = 1mm每秒
mm_convert_px = con.mm_convert_px
px_convert_mm = con.px_convert_mm
# --------------------------------------------------------------------------------------------------------
# 场景矩形————用于检测碰撞(也就是用于框住所有场景中存在的物体)
# ((x,y), (width, height)), 矩形的坐标和宽高
scene = con.scene
scene0 = con.scene0
scene1 = con.scene1  # 红外场景
scene2 = con.scene2  # 超声波场景
scene3 = con.scene3  # 简单运动
scene4 = con.scene4  # 简单巡线
scene5 = con.scene5  # 智能家居
scene6 = con.scene6  #竞技机器人
scene7 = con.scene7
scene8 = con.scene8
scene9 = con.scene9
scene10 = con.scene10

# 场景内的积分星星
# 坐标(x, y)，中心坐标
star = con.star
star0 = con.star0
star1 = con.star1
star2 = con.star2
star3 = con.star3
star4 = con.star4
star5 = con.star5
star6 = con.star6
star7 = con.star7
star8 = con.star8
star9 = con.star9
star10 = con.star10

# 场景内的标志物，可用于视觉
# 格式{1: ['others/star', (300, 200), 'actors/car'], []}, 标志物图像，中心坐标，正视图
marker = con.marker
marker0 = con.marker0
marker1 = con.marker1
marker2 = con.marker2
marker3 = con.marker3
marker4 = con.marker4
marker5 = con.marker5
marker6 = con.marker6
marker7 = con.marker7
marker8 = con.marker8
marker9 = con.marker9
marker10 = con.marker10

# 角色，背景，赛道、障碍、物品或其他图像的名称与坐标或RGB(传感器不存放在这)
elements = con.elements
# --------------------------------------------------------------------------------------------------------
# 仿真界面所有固定及关联坐标点
hardware_pos_pic_right = con.hardware_pos_pic_right
hardware_pos_name_right = con.hardware_pos_name_right
io_pwm_pos_right = con.io_pwm_pos_right
return_data_pos_right = con.return_data_pos_right
return_data_pos_right_other = con.return_data_pos_right_other
# 以下待开发使用
hardware_pos_pic_left = con.hardware_pos_pic_left
hardware_pos_name_left = con.hardware_pos_name_left
return_data_pos_left = con.return_data_pos_left
# 文本框位置
texts_pos = con.texts_pos
# (1: [(60, 510), (140, 510)],
# 2: [(60, 533), (140, 533)],
# 3: [(75, 559), (150, 559)],
# 4: [(75, 582), (150, 582)],
# 5: [(75, 605), (150, 605)])
texts_pos_sitting = con.texts_pos_sitting
# 输入框位置
input_pos = con.input_pos
# 翻页框的位置
pageback_rect = con.pageback_rect
pageforward_rect = con.pageforward_rect


# --------------------------------------------------------------------------------------------------------
# 设置所有的背景或者关卡
class Level:  # 默认展示背景
    def __init__(self):
        self.interface = elements['interfaces'][1]  # 界面
        self.level = elements['levels']['默认']  # 场景
        self.racetrack = elements['racetracks'][0]  # 赛道
        self.actor = elements['actors']['默认']  # 角色
        self.others = []  # 特殊物品


class Level0:  # 空白背景
    def __init__(self):
        self.interface = elements['interfaces'][1]  # 界面
        self.level = elements['levels'][0]  # 场景
        self.racetrack = elements['racetracks'][0]  # 赛道
        self.actor = elements['actors'][0]  # 角色
        self.others = []  # 特殊物品


# --------------------------------------------------------------------------------------------------------
# 所有关卡的虚拟场景，及其参数
class Level1:
    def __init__(self):
        self.interface = elements['interfaces'][1]  # 界面
        self.level = elements['levels'][1]  # 场景
        self.racetrack = elements['racetracks'][0]  # 赛道
        self.actor = elements['actors'][1]  # 角色
        self.others = []  # 特殊物品


class Level2:
    def __init__(self):
        self.interface = elements['interfaces'][1]  # 界面
        self.level = elements['levels'][2]  # 场景
        self.racetrack = elements['racetracks'][0]  # 赛道
        self.actor = elements['actors'][2]  # 角色
        # self.others = [elements['others'][1], elements['others'][2]]  # 特殊物品
        self.others = []


class Level3:
    def __init__(self):
        self.interface = elements['interfaces'][1]  # 界面
        self.level = elements['levels'][3]  # 场景
        self.racetrack = elements['racetracks'][0]  # 赛道
        self.actor = elements['actors'][3]  # 角色
        self.others = []


class Level4:
    def __init__(self):
        self.interface = elements['interfaces'][1]  # 界面
        self.level = elements['levels'][4]  # 场景
        self.racetrack = elements['racetracks'][0]  # 赛道
        self.actor = elements['actors'][4]  # 角色
        self.others = []


class Level5:
    def __init__(self):
        self.interface = elements['interfaces'][1]  # 界面
        self.level = elements['levels'][5]  # 场景
        self.racetrack = elements['racetracks'][0]  # 赛道
        self.actor = elements['actors'][5]  # 角色
        self.others = []


class Level6:
    def __init__(self):
        self.interface = elements['interfaces'][1]  # 界面
        self.level = elements['levels'][6]  # 场景
        self.racetrack = elements['racetracks'][0]  # 赛道
        self.actor = elements['actors'][6]  # 角色
        self.others = []


class Level7:
    def __init__(self):
        self.interface = elements['interfaces'][1]  # 界面
        self.level = elements['levels'][7]  # 场景
        self.racetrack = elements['racetracks'][0]  # 赛道
        self.actor = elements['actors'][7]  # 角色
        self.others = []


class Level8:
    def __init__(self):
        self.interface = elements['interfaces'][1]  # 界面
        self.level = elements['levels'][8]  # 场景
        self.racetrack = elements['racetracks'][0]  # 赛道
        self.actor = elements['actors'][8]  # 角色
        self.others = []


class Level9:
    def __init__(self):
        self.interface = elements['interfaces'][1]  # 界面
        self.level = elements['levels'][9]  # 场景
        self.racetrack = elements['racetracks'][0]  # 赛道
        self.actor = elements['actors'][9]  # 角色
        self.others = []


class Level10:
    def __init__(self):
        self.interface = elements['interfaces'][1]  # 界面
        self.level = elements['levels'][10]  # 场景
        self.racetrack = elements['racetracks'][0]  # 赛道
        self.actor = elements['actors'][10]  # 角色
        self.others = []
