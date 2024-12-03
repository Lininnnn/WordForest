import tkinter as tk
from tkinter import Tk, Frame, Label, Entry, Button, messagebox
from PIL import Image, ImageTk
from datetime import date
from tkinter import messagebox
import json
import os
import random
from PIL import Image, ImageTk
import pygame
from pathlib import Path
# from tkinter import *
# Explicit imports to satisfy Flake8
from tkinter import Tk, Canvas, Entry, Text, Button, PhotoImage


OUTPUT_PATH = Path(__file__).parent
ASSETS_PATH = OUTPUT_PATH / Path(r"assets\frame0")

# 数据文件
USER_DATA_FILE = "users.json"
WORDS_DATA_FILE = "words.json"

# 用户数据
users_data = {}
# 单词本数据
words_data = {}

pygame.mixer.init()

music_files = []# 假设我们有一个存储音乐文件名的列表
study_days_label = None
font_path = os.path.join("font", "Chinese.otf")# 定义字体路径

# 使用自定义字体
def set_font(widget, text, font_size):
    widget.config(text=text, font=(font_path, font_size))

def load_music():
    """加载音乐文件"""
    music_folder = os.path.join(os.path.dirname(__file__), 'music')
    if os.path.exists(music_folder):
        # 遍历音乐文件夹中的所有文件
        for file in os.listdir(music_folder):
            if file.endswith('.mp3') or file.endswith('.wav'):  # 只加载音乐文件
                music_files.append(file)
                
def play_background_music():
    """播放背景音乐"""
    if 'background.mp3' in music_files:  # 检查背景音乐是否在列表中
        pygame.mixer.music.load(os.path.join(os.path.dirname(__file__), 'music', 'background.mp3'))  # 加载背景音乐
        pygame.mixer.music.play(-1)
        
def play_success_music():
    """播放成功音乐"""
    if 'success.mp3' in music_files:
        pygame.mixer.music.load(os.path.join(os.path.dirname(__file__), 'music', 'success.mp3'))
        pygame.mixer.music.play()
        
def play_failure_music():
    """播放失败音乐"""
    if 'failure.mp3' in music_files:  # 如果失败音乐在列表中
        pygame.mixer.music.load(os.path.join(os.path.dirname(__file__), 'music', 'failure.mp3'))  # 加载失败音乐
        pygame.mixer.music.play()  # 播放失败音乐


def get_img(image_path, width, height):
    """读取并调整图片大小"""
    image_path = os.path.join('images', '2.jpg')
    image = Image.open(image_path)
    image = image.resize((width, height))  # 调整图片大小
    return ImageTk.PhotoImage(image)


def load_data():
    """加载用户数据和单词数据"""
    global users_data, words_data
    if os.path.exists(USER_DATA_FILE):
        with open(USER_DATA_FILE, "r", encoding="utf-8") as file:
            users_data = json.load(file)
    if os.path.exists(WORDS_DATA_FILE):
        with open(WORDS_DATA_FILE, "r", encoding="utf-8") as file:
            words_data = json.load(file)


def save_data():
    """保存数据"""
    with open(USER_DATA_FILE, "w", encoding="utf-8") as file:
        json.dump(users_data, file, indent=4, ensure_ascii=False)
    with open(WORDS_DATA_FILE, "w", encoding="utf-8") as file:
        json.dump(words_data, file, indent=4, ensure_ascii=False)


def validate_input(user_input, input_type="text"):
    """简单的输入验证"""
    if input_type == "text" and len(user_input.strip()) == 0:
        return False
    if input_type == "number" and not user_input.isdigit():
        return False
    return True


def register_user(username, password):
    """注册新用户"""
    if username in users_data:
        return False
    users_data[username] = {
        "password": password,
        "total_score": 0,
        "correct_count": 0,
        "wrong_count": 0,
        "study_days": 0,
        "wrong_words": []
    }
    save_data()
    return True


def login_user(username, password):
    """用户登录验证"""
    if username in users_data and users_data[username]["password"] == password:
        return True
    return False


def add_word(word, part_of_speech, meaning):
    """增加单词"""
    words_data[word] = {
        "part_of_speech": part_of_speech,
        "meaning": meaning,
        "frequency": 0,
        "correct_rate": 0
    }
    save_data()


def modify_word(word, part_of_speech=None, meaning=None):
    """修改单词"""
    if word in words_data:
        if part_of_speech:
            words_data[word]["part_of_speech"] = part_of_speech
        if meaning:
            words_data[word]["meaning"] = meaning
        save_data()


def delete_word(word):
    """删除单词"""
    if word in words_data:
        del words_data[word]
        save_data()

def recite_mode(username):
    """背诵模式：用户浏览单词和释义"""

    def show_word():
        """更新当前单词显示"""
        word = word_list[current_word_index]
        word_info = words_data[word]
        word_label.config(text=f"单词: {word}")
        meaning_label.config(text=f"含义: {word_info['meaning']}")
        progress_label.config(text=f"数量: {current_word_index + 1}/{len(word_list)}")

    def next_word():
        """显示下一个单词"""
        nonlocal current_word_index
        current_word_index = (current_word_index + 1) % len(word_list)
        show_word()

    def previous_word():
        """显示上一个单词"""
        nonlocal current_word_index
        current_word_index = (current_word_index - 1) % len(word_list)
        show_word()

    word_list = list(words_data.keys())
    current_word_index = 0

     # 创建主窗口
    root = tk.Tk()
    root.geometry("600x600")
    root.title("背诵模式")

     # 创建Canvas作为背景
    canvas = tk.Canvas(root, width=600, height=400)
    canvas.pack(fill="both", expand=True)

    # 设置上下两部分背景颜色
    canvas.create_rectangle(0, 0, 600, 100, fill="#587387", outline="#587387")  # 上半部分背景
    canvas.create_rectangle(0, 100, 600, 800, fill="white", outline="white")  # 下半部分背景

    # 创建内容框
    content_frame = tk.Frame(root, bg="white", bd=2)
    # 方式 1：使用相对位置设置
    # 调整内容框在窗口中的位置
    content_frame.place(relx=0.5, rely=0.4, anchor="center", relwidth=0.8, relheight=0.4)

    # 添加顶部的Word标签
    word_label = tk.Label(content_frame, text="Word:", font=("Comic Sans MS", 18))
    word_label.pack(pady=(10, 5))

    # 添加Meaning标签
    meaning_label = tk.Label(content_frame, text="Meaning:", font=("Comic Sans MS", 14))
    meaning_label.pack(pady=(5, 10))

    # 按钮区
    button_frame = tk.Frame(root)
    button_frame.pack(pady=10, fill="x")  # 按钮区域横向填充

    prev_button = tk.Button(root, text="Last", font=("Comic Sans MS", 14), command=previous_word,bg='#90caf9', relief='raised', bd=1)
    prev_button.pack(side="left", padx=10, pady=5, expand=True)

    next_button = tk.Button(root, text="Next", font=("Comic Sans MS", 14), command=next_word,bg='#90caf9', relief='raised', bd=1)
    next_button.pack(side="right", padx=10, pady=5, expand=True)

    # 显示进度
    progress_label = tk.Label(content_frame, text="Progress: 0/0", font=("Comic Sans MS", 12))
    progress_label.pack(pady=(10, 20))

    show_word()
    root.mainloop()  


def spell_mode(username, words_data, users_data):
    """拼写模式：用户根据释义输入单词"""
    
    # 初始化计数器
    correct_count = 0
    wrong_count = 0
    current_word_index = 0
    total_score = 0  # 新增的总得分变量

    def next_word():
        """显示下一个单词"""
        nonlocal current_word_index
        if current_word_index < len(word_list):
            word = word_list[current_word_index]
            word_info = words_data[word]
            word_label.config(text=f"词性: {word_info['part_of_speech']}")
            meaning_label.config(text=f"含义: {word_info['meaning']}")
            answer_entry.delete(0, tk.END)
            progress_label.config(text=f"进度: {current_word_index + 1}/{len(word_list)}")
        else:
            messagebox.showinfo("学习完成", f"拼写模式结束！\n正确数量：{correct_count}\n错误数量：{wrong_count}")
            
            users_data[username]["correct_count"] = correct_count
            users_data[username]["wrong_count"] = wrong_count
            users_data[username]["total_score"] = total_score
            save_data() 
            root.quit()  # 退出主界面
            root.destroy()  # 销毁窗口并退出

    def check_answer():
        """检查答案"""
        nonlocal correct_count, wrong_count, current_word_index, total_score
        user_answer = answer_entry.get().strip()
        current_word = word_list[current_word_index]

        if user_answer.lower() == current_word.lower():
            result_label.config(text="Correct!", fg="green")
            correct_count += 1
            total_score += 10  # 答对时增加总得分
            score_label.config(text=f"得分: {total_score}")  # 更新得分
        else:
            result_label.config(text=f"Wrong! Correct: {current_word}", fg="red")
            wrong_count += 1
            total_score -= 10  # 答错时扣除总得分
            score_label.config(text=f"得分: {total_score}")  # 更新得分
        
        # 保存错误单词到错题本
        users_data[username]["wrong_words"].append(current_word)
        save_data()  # 保存数据到文件或数据库

        # 更新正确和错误数量标签
        correct_label.config(text=f"正确数: {correct_count}")
        wrong_label.config(text=f"错误数: {wrong_count}")
    
        # 更新当前单词索引并显示下一个单词
        current_word_index += 1
        next_word()

    word_list = list(words_data.keys())
    random.shuffle(word_list)
    current_word_index = 0
    correct_count = 0
    wrong_count = 0

    # 创建主界面窗口
    root = tk.Tk()
    root.geometry("600x400")
    root.title("拼写模式")

    # 标签和输入框
    meaning_label = tk.Label(root, text="Meaning:", font=("Comic Sans MS", 14))
    meaning_label.pack(pady=(10, 5))
    word_label = tk.Label(root, text="Word:", font=("Comic Sans MS", 18))
    word_label.pack(pady=(5, 10))
    answer_label = tk.Label(root, text="Your answer:", font=("Comic Sans MS", 14))
    answer_label.pack(pady=(15, 5))

    answer_entry = tk.Entry(root, font=("Comic Sans MS", 14), width=20)
    answer_entry.pack(pady=(5, 15))

    check_button = tk.Button(root, text="Check Answer", font=("Comic Sans MS", 14), command=check_answer, bg='#90caf9', relief='raised', bd=1)
    check_button.pack(padx=10, pady=5, expand=True)

    result_label = tk.Label(root, text="", font=("Comic Sans MS", 14))
    result_label.pack(pady=(10, 20))

    progress_label = tk.Label(root, text="Progress: 0/0", font=("Comic Sans MS", 12))
    progress_label.pack(pady=(10, 20))

# 新增的得分、正确数、错误数标签
    score_label = tk.Label(root, text=f"得分: {total_score}", font=("Comic Sans MS", 14))
    score_label.pack(side=tk.LEFT, padx=(5, 10))  # 添加水平间距
    correct_label = tk.Label(root, text=f"正确数: {correct_count}", font=("Comic Sans MS", 14))
    correct_label.pack(side=tk.LEFT, padx=(5, 10))  # 添加水平间距
    wrong_label = tk.Label(root, text=f"错误数: {wrong_count}", font=("Comic Sans MS", 14))
    wrong_label.pack(side=tk.LEFT, padx=(5, 10))  # 添加水平间距

    next_word()  # 显示第一个单词
    root.mainloop()
    
    
def choose_study_mode(username):
    """选择学习模式界面"""

    def start_study(mode):
        """启动对应的学习模式"""
        root.quit()
        if mode == "recite":
            recite_mode(username)
        elif mode == "spell":
            spell_mode(username,words_data,users_data)

    root = tk.Tk()
    root.geometry("400x200")
    root.title("选择学习模式")

    button_config = {
        "width": 20, # 设置按钮的宽度
        "height": 1,  # 设置按钮的高度
        "relief": 'raised',  # 设置按钮风格
        "font": ("Comic Sans MS", 15)  # 字体设置
    }

    # 定义颜色
    recite_button_color = '#cfd8dc'  # 背诵模式按钮颜色
    spell_button_color = '#cfd8dc'    # 拼写模式按钮颜色

    recite_button = tk.Button(root, text="Recite", bg=recite_button_color, command=lambda: start_study("recite"), **button_config)
    recite_button.pack(pady=20)

    spell_button = tk.Button(root, text="Spell", bg=spell_button_color, command=lambda: start_study("spell"), **button_config)
    spell_button.pack(pady=20)


    root.mainloop()



def review_wrong_words(username):
    """复习错题本（图形界面版）"""
    wrong_words = users_data[username]["wrong_words"]

    if not wrong_words:
        messagebox.showinfo("没有错题", "没有错题可复习！")
        return

    current_word_index = 0

    def show_next_word():
        """显示下一个错题"""
        nonlocal current_word_index
        if current_word_index < len(wrong_words):
            word = wrong_words[current_word_index]
            word_info = words_data[word]
            word_label.config(text=f"单词: {word}")
            meaning_label.config(text=f"含义: {word_info['meaning']}")
            current_word_index += 1
        else:
            # 复习完成后删除错题单词
            users_data[username]["wrong_words"] = []
            save_data()  # 确保错题本数据被保存
            messagebox.showinfo("复习完成", "恭喜！你已复习完所有错题！")
            root.quit()  # 关闭窗口

    def show_prev_word():
        """显示上一个错题"""
        nonlocal current_word_index
        if current_word_index > 0:
            current_word_index -= 1
            word = wrong_words[current_word_index]
            word_info = words_data[word]
            word_label.config(text=f"单词: {word}")
            meaning_label.config(text=f"含义: {word_info['meaning']}")

    # 创建复习错题的窗口
    root = tk.Tk()
    root.geometry("600x400")
    root.title("错题本复习")

    # 显示当前错题的单词和释义
    word_label = tk.Label(root, text="单词:", font=("Comic Sans MS", 18))
    word_label.pack(pady=10)

    meaning_label = tk.Label(root, text="含义:", font=("Comic Sans MS", 14))
    meaning_label.pack(pady=10)

    # 显示复习进度
    progress_label = tk.Label(root, text=f"数量: {current_word_index}/{len(wrong_words)}", font=("Comic Sans MS", 12))
    progress_label.pack(pady=5)

    button_config = {
        "width": 20,  # 设置按钮的宽度
        "height": 2,  # 设置按钮的高度
        "relief": 'raised',  # 设置按钮风格
        "font": ("Comic Sans MS", 15)  # 字体设置
    }

    prev_button = tk.Button(root, text="Last", bg='#78909c', command=show_prev_word, **button_config)
    prev_button.pack(side=tk.LEFT, padx=20, pady=20)

    next_button = tk.Button(root, text="Next", bg='#cfd8dc', 
                            command=lambda: [show_next_word(),
                                             progress_label.config(text=f"数量: {current_word_index}/{len(wrong_words)}")],
                            **button_config)
    next_button.pack(side=tk.RIGHT, padx=20, pady=20)

    # 显示第一个错题
    show_next_word()

    root.mainloop()


def relative_to_assets(path: str) -> Path:
    return ASSETS_PATH / Path(path)


def create_main_window():

    root = tk.Tk()
    root.geometry("642x642")
    root.configure(bg="#FFFFFF")
    
    login_frame = tk.Frame(root, bg="#FFFFFF")
    login_frame.pack(fill="both", expand=True)


    canvas = Canvas(
        root,
        bg="#FFFFFF",
        height=642,
        width=642,
        highlightthickness=0,
        relief="ridge"
    )
    canvas.place(x=0, y=0)

    canvas = Canvas(root, width=642, height=642, bg="#FFFFFF", bd=0, highlightthickness=0, relief="ridge")
    canvas.place(x = 0, y = 0)

    image_image_1 = PhotoImage(file=relative_to_assets("image_1.png"))
    canvas.create_image(321, 321.0, image=image_image_1)
    
    entry_image_1 = PhotoImage(file=relative_to_assets("entry_1.png"))
    canvas.create_image(329.0, 268.0, image=entry_image_1)
    entry_1 = Entry(bd=0, bg="#F9FFFF", fg="#000716", highlightthickness=0)
    entry_1.place(x=187.0, y=249.0, width=284.0, height=36.0)
    
    entry_image_2 = PhotoImage(file=relative_to_assets("entry_2.png"))
    canvas.create_image(329.0, 331.0, image=entry_image_2)
    entry_2 = Entry(bd=0, bg="#F8FCFC", fg="#000716", highlightthickness=0,show="*")
    entry_2.place(x=187.0, y=312.0, width=284.0, height=36.0)


    button_image_1 = PhotoImage(file=relative_to_assets("button_1.png"))
    button_image_2 = PhotoImage(file=relative_to_assets("button_2.png"))

    def show_login_screen():
        """显示登录界面"""
        load_music()
        play_background_music()

        def login_action():
            username = entry_1.get()
            password = entry_2.get()

            if not validate_input(username) or not validate_input(password):
                play_failure_music()
                messagebox.showerror("错误", "请输入有效的用户名和密码")
                return

            if login_user(username, password):
                play_success_music()
                messagebox.showinfo("成功", "登录成功")
                login_frame.pack_forget()  # 隐藏登录框
                show_main_screen(username)  # 显示主界面
            else: 
                play_failure_music()
                messagebox.showerror("错误", "用户名或密码错误")

            

        def register_action():
            username = entry_1.get()
            password = entry_2.get()

            if not validate_input(username) or not validate_input(password):
                play_failure_music()
                messagebox.showerror("错误", "请输入有效的用户名和密码")
                return

            if register_user(username, password):
                play_success_music()
                messagebox.showinfo("成功", "注册成功")
                login_frame.pack_forget()  # 隐藏登录框
                show_main_screen(username)  # 显示主界面
            else:
                play_failure_music()
                messagebox.showerror("错误", "用户名已存在")

        button_1 = Button(
            image=button_image_1,
            borderwidth=0,
            highlightthickness=0,
            command=login_action,
            relief="flat"
        )
        button_1.place(
        x=139.0,
        y=444.0,
        width=132.0,
        height=52.0
        )

        button_2 = Button(
            image=button_image_2,
            borderwidth=0,
            highlightthickness=0,
            command=register_action,
            relief="flat"
        )
        button_2.place(
        x=364.0,
        y=444.0,
        width=132.0,
        height=52.0
        )
            
        login_frame.grid_columnconfigure(0, weight=1)  # 列0占用所有可用空间
        login_frame.grid_columnconfigure(1, weight=1)  # 列1也占用空间，保证对齐
        login_frame.grid_rowconfigure(0, weight=1)  # 行0、1和2也可以扩展，使控件居中
        login_frame.grid_rowconfigure(1, weight=1)
        login_frame.grid_rowconfigure(2, weight=1)

        # 使得窗口在屏幕中居中
        # 使得窗口在屏幕中居中
        root.update()
        width = root.winfo_width()
        height = root.winfo_height()
        screen_width = root.winfo_screenwidth()
        screen_height = root.winfo_screenheight()

        # 计算居中位置
        position_top = int(screen_height / 2 - height / 2)
        position_left = int(screen_width / 2 - width / 2)

        root.geometry(f'{width}x{height}+{position_left}+{position_top}')  # 设置窗口居中

    def show_main_screen(username):
        global study_days_label
        """显示主界面"""
        load_data()  
        root.geometry("750x550")  # 登录页面的尺寸
      
        im_root = get_img('2.jpg',700, 500)  
        bg_label = tk.Label(root, image=im_root)  # 使用Label显示背景图片
        bg_label.place(relwidth=1, relheight=1)  # 设置背景图片填充整个窗口

        # 保持对图片的引用，防止被垃圾回收
        bg_label.image = im_root

        # 创建一个主框架，放置其他控件
        main_frame = tk.Frame(root, bg="#FFFFFF", bd=10)  
        main_frame.place(relx=0.5, rely=0.5, anchor="center")  

        # 显示欢迎信息
        welcome_label = tk.Label(main_frame, text=f"Welcome, {username}", font=("Comic Sans MS", 16))
        welcome_label.pack(pady=10)  # 上下间距
        load_music()
        play_background_music()
 

        # 获取用户的成绩数据
        if username in users_data:
            user_info = users_data[username]
            total_score = user_info["total_score"]
            correct_count = user_info["correct_count"]
            wrong_count = user_info["wrong_count"]

            # 显示用户成绩信息
            info_text = (
                f"总分: {total_score} | "
                f"正确回答数: {correct_count} | "
                f"错误回答数: {wrong_count} "
            )

            # 显示成绩信息的 Label
            info_label = tk.Label(main_frame, text=info_text, font=("Comic Sans MS", 12), justify="center")
            info_label.pack(pady=10)
 
            # 显示学习天数
            study_days_label = tk.Label(main_frame, text=f"学习天数: {users_data[username]['study_days']} 天", 
            font=("Comic Sans MS", 12), justify="center")
            study_days_label.pack(pady=10)

        # 使用 grid 布局管理器来排列按钮
        button_frame = tk.Frame(main_frame)
        button_frame.pack(pady=15)  # 按钮区域的垂直间距

        # 按钮样式
        button_config = {
            "width": 20,  # 设置按钮的宽度
            "height": 1,  # 设置按钮的高度
            "relief": 'raised',  # 设置按钮风格
            "font": ("Comic Sans MS", 12)  # 字体设置
        }

        # 开始背单词按钮
        start_button = tk.Button(button_frame, text="Begin", command=lambda: choose_study_mode(username),
                                 bg='#eceff1', **button_config)
        start_button.grid(row=0, column=0, padx=10, pady=5, sticky="ew")

        # 错题复习按钮
        review_button = tk.Button(button_frame, text="Review", command=lambda: review_wrong_words(username),
                                  bg='#cfd8dc', **button_config)
        review_button.grid(row=1, column=0, padx=10, pady=5, sticky="ew")

        # 打卡按钮
        clock_in_button = tk.Button(button_frame, text="Check-in", command=lambda: clock_in(username),
                                    bg='#78909c', **button_config)
        clock_in_button.grid(row=2, column=0, padx=10, pady=5, sticky="ew")

        # 管理单词本按钮
        manage_button = tk.Button(button_frame, text="Word Book", command=show_word_management_screen,
                                  bg='#e1f5fe', **button_config)
        manage_button.grid(row=3, column=0, padx=10, pady=5, sticky="ew")

        # 退出按钮
        exit_button = tk.Button(button_frame, text="Exit", command=root.quit,
                                bg='#bbdefb', **button_config)
        exit_button.grid(row=4, column=0, padx=10, pady=5, sticky="ew")
        
        # 假设已经有一个函数用于暂停音乐
        def pause_music():
    # 这里添加暂停音乐的逻辑
           if pygame.mixer.music.get_busy():  # 检查音乐是否正在播放
            pygame.mixer.music.pause()  # 暂停音乐
        
           else:
            pygame.mixer.music.unpause()  # 如果音乐已暂停，则恢复播放
            pass

# 创建一个新的按钮用于暂停音乐
        pause_button = tk.Button(button_frame, text="Pause/On music", command=pause_music,
                         bg='#ffccbc', **button_config)
        pause_button.grid(row=5, column=0, padx=10, pady=5, sticky="ew")

# 将按钮定位在右下方
        pause_button.grid(row=5, column=0, padx=(10, 10), pady=(0, 10), sticky="se")



        # 调整窗口居中
        root.update()
        width = root.winfo_width()
        height = root.winfo_height()
        screen_width = root.winfo_screenwidth()
        screen_height = root.winfo_screenheight()

        position_top = int(screen_height / 2 - height / 2)
        position_left = int(screen_width / 2 - width / 2)

        root.geometry(f'{width}x{height}+{position_left}+{position_top}')  # 设置窗口居中

    def show_word_management_screen():
        load_data()
        """显示单词本管理界面"""
        management_frame = tk.Toplevel(root)
        management_frame.title("单词本管理")

        tk.Label(management_frame, text="单词:").grid(row=0, column=0)
        tk.Label(management_frame, text="词性:").grid(row=1, column=0)
        tk.Label(management_frame, text="释义:").grid(row=2, column=0)

        word_entry = tk.Entry(management_frame)
        pos_entry = tk.Entry(management_frame)
        meaning_entry = tk.Entry(management_frame)

        word_entry.grid(row=0, column=1)
        pos_entry.grid(row=1, column=1)
        meaning_entry.grid(row=2, column=1)

        def add_word_action():
            """添加单词"""
            word = word_entry.get()
            pos = pos_entry.get()
            meaning = meaning_entry.get()
            if validate_input(word) and validate_input(pos) and validate_input(meaning):
                if word in words_data:
                    messagebox.showerror("错误", "单词已存在")
                else:
                    add_word(word, pos, meaning)
                    messagebox.showinfo("成功", "单词已添加")
                    refresh_word_list()  # 添加成功后刷新列表
            else:
                messagebox.showerror("错误", "请输入有效的单词信息")

        def modify_word_action():
            """修改选中的单词"""
            word = word_entry.get()
            pos = pos_entry.get()
            meaning = meaning_entry.get()
            if validate_input(word):
                if word in words_data:
                    modify_word(word, part_of_speech=pos, meaning=meaning)
                    messagebox.showinfo("成功", "单词已修改")
                    refresh_word_list()  # 修改成功后刷新列表
                else:
                    messagebox.showerror("错误", "单词不存在")
            else:
                messagebox.showerror("错误", "请输入有效的单词信息")

        def delete_word_action():
            """删除单词"""
            word = word_entry.get()
            if validate_input(word):
                if word in words_data:
                    delete_word(word)
                    messagebox.showinfo("成功", "单词已删除")
                    refresh_word_list()  # 删除后刷新列表
                else:
                    messagebox.showerror("错误", "单词不存在")
            else:
                messagebox.showerror("错误", "请输入有效的单词")

        def refresh_word_list():
            """刷新单词列表"""
            word_listbox.delete(0, tk.END)
            for word, info in words_data.items():
                word_listbox.insert(tk.END, f"{word} ({info['part_of_speech']}): {info['meaning']}")

        def on_word_select(event):
            """选择单词时自动填充到输入框"""
            selected_word = word_listbox.get(word_listbox.curselection())
            word = selected_word.split(' ')[0]  # 获取单词
            pos = selected_word.split('(')[1].split(')')[0]  # 获取词性
            meaning = selected_word.split(': ')[1]  # 获取释义

            word_entry.delete(0, tk.END)
            pos_entry.delete(0, tk.END)
            meaning_entry.delete(0, tk.END)

            word_entry.insert(0, word)
            pos_entry.insert(0, pos)
            meaning_entry.insert(0, meaning)

        # 单词列表显示
        word_listbox = tk.Listbox(management_frame, width=50, height=10)
        word_listbox.grid(row=4, column=0, columnspan=3)
        word_listbox.bind("<Double-1>", on_word_select)  # 双击选择单词填充

        # 刷新按钮
        refresh_button = tk.Button(management_frame, text="刷新单词列表", command=refresh_word_list)
        refresh_button.grid(row=5, column=1)

          # 操作按钮
        tk.Button(management_frame, text="添加单词", command=add_word_action).grid(row=3, column=0)
        tk.Button(management_frame, text="修改单词", command=modify_word_action).grid(row=3, column=1)
        tk.Button(management_frame, text="删除单词", command=delete_word_action).grid(row=3, column=2)

        # 初次加载单词列表
        refresh_word_list()

    def clock_in(username):
        """打卡并弹出成功提示框"""
    
    # 获取今天的日期
        today_date = date.today().strftime("%Y-%m-%d")

    # 获取用户数据
        user_data = users_data.get(username)

        if user_data:
        # 检查用户是否没有 last_clock_in 键
           if "last_clock_in" not in user_data:
            # 如果没有 last_clock_in 键，初始化该键并记录今天的日期
                user_data["last_clock_in"] = today_date
           elif user_data["last_clock_in"] == today_date:
                 play_failure_music()
                 messagebox.showinfo("提示", "今天已经打卡过了！")
                 load_music()
                 play_background_music()
                 return  # 如果今天已经打卡过，直接返回
            
           # 更新打卡天数
           user_data["study_days"] += 1
           user_data["last_clock_in"] = today_date  # 更新最后打卡日期
           # 保存数据
           save_data()
            # 弹出提示框，提示用户打卡成功
           play_success_music()
           messagebox.showinfo("打卡成功", f"{username}，打卡成功！已累计学习 {user_data['study_days']} 天。")
                # 直接更新学习天数标签
           load_music()
           play_background_music()
           study_days_label.config(text=f"学习天数: {user_data['study_days']} 天")
        
        else : 
           play_failure_music()
           messagebox.showerror("错误", f"用户 {username} 不存在！")
           load_music()
           play_background_music()
    
    show_login_screen()

    root.resizable(False, False)
    root.mainloop()


if __name__ == "__main__":
    load_data()
    create_main_window()