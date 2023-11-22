import tkinter as tk
from tkinter import Listbox, Entry, Text, Scrollbar, Button, messagebox
from movie_question_classifier import *  # 假设您有一个电影问题分类器
from movie_question_parser import *  # 使用之前为您修改的电影问题解析器
from movie_answer_search import *  # 假设您有一个电影答案搜索器

entry = None
text = None

class MovieChatBotGraph:
    def __init__(self):
        self.classifier = MovieQuestionClassifier()  # 电影问题分类器
        self.parser = MovieQuestionPaser()  # 电影问题解析器
        self.searcher = MovieAnswerSearcher()  # 电影答案搜索器

    def chat_main(self, sent):


        error = '抱歉，您的问题我还不太懂，我会继续努力的。'
        res_classify = self.classifier.classify(sent)
        if not res_classify:
            return error

        res_sql = self.parser.parser_main(res_classify)
        final_answers = self.searcher.search_main(res_sql)

        if not final_answers:
            return error
        else:
            return '\n'.join(final_answers)

def load_movie_data():
    movie_name = []
    movie_type = []
    base_path = "F:\\Vscode_Project\\Testpro_chat\\dict\\"
    movie_name = os.path.join(base_path, "movie_name.txt")
    movie_type = os.path.join(base_path, "movie_type.txt")
    with open(movie_name, 'r', encoding='utf-8') as f:
        movie_name = [i.strip() for i in f if i.strip()]
    with open(movie_type, 'r', encoding='utf-8') as f:
        movie_type = [i.strip() for i in f if i.strip()]
    return movie_name, movie_type

def send_question(event=None):
    global entry, text
    question = entry.get()
    # 这里应该是处理问题并返回答案的代码
    handler = MovieChatBotGraph()
    answer = handler.chat_main(question)
    # 以下是示例回答
    text.config(state=tk.NORMAL)
    text.insert(tk.END, "问: " + question + "\n")
    text.insert(tk.END, "答: " + answer + "\n\n")
    text.config(state=tk.DISABLED)
    entry.delete(0, tk.END)


def copy_to_clipboard(event, listbox):
    window.clipboard_clear()
    selected = listbox.get(listbox.curselection())
    window.clipboard_append(selected)

def clear_text():
    global text
    text.config(state=tk.NORMAL)
    text.delete('1.0', tk.END)
    text.config(state=tk.DISABLED)

def create_ui():
    global entry, text, window
    window = tk.Tk()
    window.title("电影问答系统")

    # 创建列表框
    frame_lists = tk.Frame(window)
    listbox_movies = Listbox(frame_lists)
    listbox_types = Listbox(frame_lists)

    # 加载电影数据
    movie_name, movie_type = load_movie_data()

    # 将电影数据添加到列表框
    for name in movie_name:
        listbox_movies.insert(tk.END, name)
    for type in movie_type:
        listbox_types.insert(tk.END, type)

    listbox_movies.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
    listbox_types.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)
    frame_lists.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

    listbox_movies.bind("<Double-1>", lambda e: copy_to_clipboard(e, listbox_movies))
    listbox_types.bind("<Double-1>", lambda e: copy_to_clipboard(e, listbox_types))

    listbox_movies.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
    listbox_types.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)
    frame_lists.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

    # 创建对话框
    frame_chat = tk.Frame(window)
    entry = Entry(frame_chat)
    entry.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
    clear_button = Button(frame_chat, text="清空", command=clear_text)  # 添加清空按钮
    clear_button.pack(side=tk.RIGHT)
    send_button = Button(frame_chat, text="发送", command=send_question)
    send_button.pack(side=tk.RIGHT)
    entry.bind("<Return>", send_question)
    frame_chat.pack(side=tk.TOP, fill=tk.X)

    # 创建文本框显示对话
    text = Text(window, state=tk.DISABLED)
    scrollbar = Scrollbar(window, command=text.yview)
    text.config(yscrollcommand=scrollbar.set)
    scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
    text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

    window.mainloop()

if __name__ == "__main__":
    create_ui()
