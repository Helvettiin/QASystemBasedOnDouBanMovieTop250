# QASystemBasedOnDouBanMovieTop250
## 1. 项目简介
该项目是基于豆瓣电影Top250的问答系统，使用了豆瓣电影Top250的数据，使用python3.10进行编写，主要使用了flask框架，以及jieba、pyltp等工具进行自然语言处理。 项目的主要功能是对用户提出的问题进行解析，然后从数据库中提取答案，返回给用户，如下图所示：
## ![image](F:\Vscode_Project\QASystemBasedOnDouBanMovieTop250\img\chat1.png)
## ![image](F:\Vscode_Project\QASystemBasedOnDouBanMovieTop250\img\chat2.png)
## ![image](F:\Vscode_Project\QASystemBasedOnDouBanMovieTop250\img\chat3.png)
## 2. 项目结构
```
├── README.md
├── app
│   ├── chat.py
│   ├── movie_answer_search.py
│   ├── movie_question_classifier.py
│   ├── movie_question_parser.py
│
├── dict
│   ├── movie_name.txt
│   ├── movie_type.txt
│   ├── actor.txt
│   ├── director.txt
│   ├── relese_date.txt
│   ├── synopsis.txt
│
├── doubantop250
│   ├── douban_topmovies.csv
│   ├── actordirector.py
│   ├── classification.py
│   ├── datetoyear.py
│   ├── Doubantop250dl.py
│   ├── filtersynopsis.py
│   ├── removerepeat.py
│   ├── yearplusnian.py
│
├── img
│   ├── chat1.png
│   ├── chat2.png
│   ├── chat3.png
│   ├── chat4.png
│   ├── chat5.png

```
### 2.1 app目录
该目录下主要是项目的主要代码文件，包括chat.py、movie_answer_search.py、movie_question_classifier.py、movie_question_parser.py四个文件。
#### 2.1.1 chat.py
该文件是项目的主程序，主要是对用户的输入进行解析，然后从数据库中提取答案，最后返回给用户。
#### 2.1.2 movie_answer_search.py
该文件主要是从数据库中提取答案。
#### 2.1.3 movie_question_classifier.py
该文件主要是对用户的提问进行分类，判断用户的提问是属于哪一类。
#### 2.1.4 movie_question_parser.py
该文件主要是对用户的提问进行解析，提取出用户提问中的关键词。
### 2.2 dict目录
该目录下主要是一些词典文件，包括movie_name.txt、movie_type.txt、actor.txt、director.txt、relese_date.txt、synopsis.txt六个文件。
### 2.3 doubantop250目录
该目录下主要是对豆瓣电影Top250的数据进行爬取，包括douban_topmovies.csv、actordirector.py、classification.py、datetoyear.py、Doubantop250dl.py、filtersynopsis.py、removerepeat.py、yearplusnian.py八个文件。
#
# 3. 项目运行
## 3.1 环境配置
该项目使用的python版本是3.10，使用的库有flask、jieba、pyltp、pymysql、pandas、numpy等。
## 3.2 项目运行
在app目录下运行chat.py文件即可启动项目。
#
# 4. 项目总结
## 4.1 项目总结
该项目是基于豆瓣电影Top250的问答系统，使用了豆瓣电影Top250的数据，使用python3.10进行编写，主要使用了flask框架，以及jieba、pyltp等工具进行自然语言处理。 项目的主要功能是对用户提出的问题进行解析，然后从数据库中提取答案，返回给用户。
## 4.2 项目不足
该项目的数据库中的数据是通过爬虫爬取的，所以数据的准确性有待提高，还有就是该项目的问题分类和问题解析是使用的是规则，所以对于一些复杂的问题无法解析，需要使用机器学习的方法来进行解决。
#
# 5. 参考资料
## 5.1 数据来源
[豆瓣电影Top250](https://movie.douban.com/top250)
