class MovieQuestionPaser:

    def build_entitydict(self, args):
        entity_dict = {}
        for arg, types in args.items():
            for type in types:
                if type not in entity_dict:
                    entity_dict[type] = [arg]
                else:
                    entity_dict[type].append(arg)

        return entity_dict

    '''解析主函数'''
    def parser_main(self, res_classify):
        #
        args = res_classify['args']
        entity_dict = self.build_entitydict(args)
        question_types = res_classify['question_types']
        sqls = []
        for question_type in question_types:
            sql_ = {}
            sql_['question_type'] = question_type
            sql = []
            #print(question_type) # 问题类型debug
            if question_type == 'movie_type':
                sql = self.sql_transfer(question_type, entity_dict.get('movie_name'))

            elif question_type == 'movie_actor':
                sql = self.sql_transfer(question_type, entity_dict.get('movie_name'))

            elif question_type == 'movie_director':
                sql = self.sql_transfer(question_type, entity_dict.get('movie_name'))
                # print(sql)
                # print(entity_dict.get('movie_name'),111)

            elif question_type == 'movie_release_date':
                sql = self.sql_transfer(question_type, entity_dict.get('movie_name'))

            elif question_type == 'director_movie':
                sql = self.sql_transfer(question_type, entity_dict.get('director'))

            elif question_type == 'actor_movie':
                sql = self.sql_transfer(question_type, entity_dict.get('actor'))

            elif question_type == 'movie_introduction':
                sql = self.sql_transfer(question_type, entity_dict.get('movie_name'))

            elif question_type == 'type_movie':
                sql = self.sql_transfer(question_type, entity_dict.get('movie_type'))

            elif question_type == 'release_date_movie':
                sql = self.sql_transfer(question_type, entity_dict.get('release_date'))

            elif question_type == 'movie_error':
                sql = self.sql_transfer(question_type, entity_dict.get('movie_name'))

            if sql:
                sql_['sql'] = sql
                sqls.append(sql_)
                #print(sqls)
        return sqls

    '''针对不同的问题，分开进行处理'''
    def sql_transfer(self, question_type, entities):
        if not entities:
            return []

        #print(entities,3)
        #print(question_type,2)

        # 查询语句
        sql = []
        # 查询电影的类型
        if question_type == 'movie_type':
            sql = ["MATCH (n:name)-[:类型]->(s:type) where n.name = '{0}' return n.name, s.type".format(i) for i in entities]

        # 查询电影的主演
        elif question_type == 'movie_actor':
            sql = ["MATCH (n:name)-[:演员]->(s:person) where n.name = '{0}' return n.name, s.person".format(i) for i in entities]

        # 查询电影的导演
        elif question_type == 'movie_director':
            sql = ["MATCH (n:name)-[:导演]->(s:person) where n.name = '{0}' return n.name, s.person".format(i) for i in entities]

        # 查询电影的上映日期
        elif question_type == 'movie_release_date':
            sql = ["MATCH (n:name)-[:上映时间]->(s:year) where n.name = '{0}' return n.name, s.year".format(i) for i in entities]

        # 查询导演的电影
        elif question_type == 'director_movie':
            sql = ["MATCH (n:person)<-[:导演]-(s:name) where n.person = '{0}' return n.person, s.name".format(i) for i in entities]

        # 查询演员的电影
        elif question_type == 'actor_movie':
            sql = ["MATCH (n:person)<-[:演员]-(s:name) where n.person = '{0}' return n.person, s.name".format(i) for i in entities]

        # 查询电影的剧情简介
        elif question_type == 'movie_introduction':
            sql = ["MATCH (n:name)-[:剧情简介]->(s:synopsis) where n.name = '{0}' return n.name, s.synopsis".format(i) for i in entities]

        # 查询某类型的电影
        elif question_type == 'type_movie':
            sql = ["MATCH (n:type)<-[:类型]-(s:name) where n.type = '{0}' return n.type, s.name".format(i) for i in entities]

        # 查询某上映时间的电影
        elif question_type == 'release_date_movie':
            sql = ["MATCH (n:year)<-[:上映时间]-(s:name) where n.year = '{0}' return n.year, s.name".format(i) for i in entities]

        # 查询某电影的错误
        elif question_type == 'movie_error':
            sql = ["MATCH (n:name)-[:剧情简介]->(s:synopsis) where n.name = '{0}' return n.name, s.synopsis".format(i) for i in entities]

        return sql

if __name__ == '__main__':
    handler = MovieQuestionPaser()
