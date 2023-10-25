import os
import json
from py2neo import Graph, Node


class MovieAnswerSearcher:
    def __init__(self):
        self.g = Graph(profile="bolt://localhost:7687", auth=("neo4j", "12345678"), name="neo4j")
        # a = self.g.run('MATCH (n) RETURN n')
        # print(a)


    def search_main(self, sqls):
        # 根据sql查询对应的结果 传入的sqls为[{question_type:xx, sql:xx}]
        final_answers = []
        for sql_ in sqls:
            question_type = sql_['question_type']
            #print(question_type,1)
            queries = sql_['sql']
            #print(queries, 2)
            answers = []
            for query in queries:
                #print(query, 3)
                res = self.g.run(query).data()
                t = self.g.run(query)
                #print('t', t)
                answers += res
            #print('ans', answers)
            # answers = self.g.run(query).data()
            final_answer = self.answer_prettify(question_type, answers)

            if final_answer:
                final_answers.append(final_answer)
        return final_answers

    def answer_prettify(self, question_type, answers):
        # 根据不同的问题类型格式化答案
        final_answer = []

        PrimaryType = ''
        PrimaryName = ''
        SecondaryType = ''
        SecondaryName = ''

        if not answers:
            return ''
        #print(answers) # 获取的答案debug
        if question_type == 'movie_type':
            PrimaryType = '电影'
            PrimaryName = answers[0]['n.name']
            SecondaryType = "类型"
            SecondaryName = 's.type'

        elif question_type == 'movie_release_date':
            PrimaryType = '电影'
            PrimaryName = answers[0]['n.name']
            SecondaryType = "上映时间"
            SecondaryName = 's.year'

        elif question_type == 'movie_director':
            PrimaryType = '电影'
            PrimaryName = answers[0]['n.name']
            SecondaryType = "导演"
            SecondaryName = 's.person'

        elif question_type == 'movie_actor':
            PrimaryType = '电影'
            PrimaryName = answers[0]['n.name']
            SecondaryType = '演员'
            SecondaryName = 's.person'

        elif question_type == 'director_movie':
            PrimaryType = '导演'
            PrimaryName = answers[0]['n.person']
            SecondaryType = '电影'
            SecondaryName = 's.name'

        elif question_type == 'actor_movie':
            PrimaryType = '演员'
            PrimaryName = answers[0]['n.person']
            SecondaryType = '电影'
            SecondaryName = 's.name'

        elif question_type == 'movie_introduction':
            PrimaryType = '电影'
            PrimaryName = answers[0]['n.name']
            SecondaryType = '剧情简介'
            SecondaryName = 's.synopsis'

        elif question_type == 'type_movie':
            PrimaryType = '类型'
            PrimaryName = answers[0]['n.type']
            SecondaryType = '电影'
            SecondaryName = 's.name'

        elif question_type == 'release_date_movie':
            PrimaryType = '上映时间'
            PrimaryName = answers[0]['n.year']
            SecondaryType = '电影'
            SecondaryName = 's.name'

        else:
            return '出错, 未知问题类型'

        final_answer = "{}'{}'的{}是: {}".format(PrimaryType, PrimaryName, SecondaryType,
                                                      ", ".join([answer.get(SecondaryName) for answer in answers]))

        return final_answer
