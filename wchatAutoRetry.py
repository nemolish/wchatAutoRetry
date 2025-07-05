from wxauto import WeChat
import time

# 设置要监听的联系人或群聊名称
target_name = '林老师'

# 设置要转发到的联系人或群聊名称
forward_name = '消息自动发送'

# 初始化变量，用于记录上一次的消息
last_msg = ""

# 备份聊天记录
def save_chat_to_file(chat_message, file_path='chat_backup.txt'):
    try:
        with open(file_path, 'a', encoding='utf-8') as file:
            file.write(chat_message + '\n')  # 将聊天记录写入文件并换行
        print(f"聊天记录已成功写入文件: {file_path}")
    except Exception as e:
        print(f"写入文件时出错: {e}")

# 读聊天记录
def read_last_line(file_path='chat_backup.txt'):
    """
    从文件中读取最后一行记录

    :param file_path: 文件路径
    :return: 最后一行内容（字符串），如果文件为空则返回 None
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            lines = file.readlines()  # 读取所有行
            if lines:  # 如果文件不为空
                return lines[-1].strip()  # 返回最后一行并去除换行符
            else:
                return None  # 文件为空
    except Exception as e:
        print(f"读取文件时出错: {e}")


def get_unsend_message():
    global last_msg
    wx.ChatWith(who=target_name)
    arr = wx.GetAllMessage()
    last_index = -1  # 初始化目标元素最后一次出现的索引
    for i in range(len(arr)):
        if arr[i].content == last_msg:  # 找到目标元素
            last_index = i  # 更新最后一次出现的索引
    last_msg = arr[-1].content;
    if last_index != -1:  # 如果目标元素存在
        return arr[last_index + 1:]  # 返回目标元素之后的所有元素
    return []  # 如果目标元素不存在，返回空列表

# 初始化微信客户端
wx = WeChat()

# 持续监听消息
while True:
    try:
        msgs = get_unsend_message();
        # raise Exception("模拟异常!");
        # 输出消息内容
        for msg in msgs:
            if msg.type == 'friend' and msg.sender == target_name:
                print(f'{msg.sender.rjust(20)}：{msg.content}')
                wx.SendMsg(msg.content, forward_name)
                save_chat_to_file(msg.content)
        # 每隔0.5秒检查一次新消息
        time.sleep(0.5)

    except Exception as e:
        print(f"发生错误: {e}")