from movie_question_classifier import *  # 假设您有一个电影问题分类器
from movie_question_parser import *  # 使用之前为您修改的电影问题解析器
from movie_answer_search import *  # 假设您有一个电影答案搜索器

'''电影问答类'''
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

if __name__ == '__main__':
    handler = MovieChatBotGraph()
    while 1:
        tip = '您好，我是电影智能助理，希望可以帮到您。如果有任何问题，请随时提问。'
        print(tip)
        question = input('请输入问题:')
        answer = handler.chat_main(question)
        print('电影助理:', answer)
        break

    # question = '蔡少芬参演的电影有什么？'
    #
    # answer = handler.chat_main(question)
    # print('电影助理:', answer)
