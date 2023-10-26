import os
import ahocorasick

class MovieQuestionClassifier:
    def __init__(self):
        # 特征词路径
        base_path = "F:\\Vscode_Project\\Testpro_chat\\dict\\"
        self.movie_name_path = os.path.join(base_path, "movie_name.txt")
        self.movie_type_path = os.path.join(base_path, "movie_type.txt")
        self.actor_path = os.path.join(base_path, "actor.txt")
        self.director_path = os.path.join(base_path, "director.txt")
        self.release_date_path = os.path.join(base_path, "release_date.txt")
        self.introduction_path = os.path.join(base_path, "synopsis.txt")

        
        # 加载特征词
        with open(self.movie_name_path, 'r', encoding='utf-8') as f:
            self.movie_name_wds = [i.strip() for i in f if i.strip()]

        with open(self.movie_type_path, 'r', encoding='utf-8') as f:
            self.movie_type_wds = [i.strip() for i in f if i.strip()]

        with open(self.actor_path, 'r', encoding='utf-8') as f:
            self.actor_wds = [i.strip() for i in f if i.strip()]

        with open(self.director_path, 'r', encoding='utf-8') as f:
            self.director_wds = [i.strip() for i in f if i.strip()]

        with open(self.release_date_path, 'r', encoding='utf-8') as f:
            self.release_date_wds = [i.strip() for i in f if i.strip()]

        with open(self.introduction_path, 'r', encoding='utf-8') as f:
            self.introduction_wds = [i.strip() for i in f if i.strip()]

        
        self.region_words = set(self.movie_name_wds + self.movie_type_wds + self.actor_wds + self.director_wds + self.release_date_wds + self.introduction_wds)
        
        # 构造领域actree
        self.region_tree = self.build_actree(list(self.region_words))
        
        # 构建词典
        self.wdtype_dict = self.build_wdtype_dict()

        # 问句疑问词
        self.movie_name_qwds = ['什么电影', '哪部电影', '电影名字', '电影名称']
        self.type_qwds = ['什么类型', '哪种类型', '是什么风格', '属于哪个类别','是什么类型','是什么种类','的分类是']
        self.actor_qwds = ['谁主演', '哪些演员', '主要演员', '男主', '女主', '主演是谁']
        self.director_qwds = ['谁导演', '导演是谁', '哪位导演','是谁导的','是这部电影的导演','执导了']
        self.release_date_qwds = ['什么时候上映', '的上映时间', '什么时候发布', '什么时候', '哪一年', '哪年']
        self.introduction_qwds = ['主要剧情', '剧情简介', '讲了什么', '剧情', '简介', '内容']
        self.actor_movie_qwds = ['演了什么电影','演的','演过','参与','的所有电影','出现过']
        self.director_movie_qwds = ['导过','执导','导演过','导演的','担任过导演',]
        self.type_movie_qwds = ['这个类型','类型的','风格的','这个风格','这个类别','类别的','这个分类','分类的','种类的','这个种类']
        self.release_date_movie_qwds = ['上映的','有哪些电影上映','有什么电影上映','上映了','年的电影','年的作品','']

        print('model init finished ......')
        return

    '''分类主函数'''
    def classify(self, question):
        ## 收集问句当中所涉及到的实体类型
        data = {}
        movie_dict = self.check_movie(question)
        # print(movie_dict)
        if not movie_dict:
            return {}
        data['args'] = movie_dict

        # 收集问句当中所涉及到的实体类型
        types = []
        for type_ in movie_dict.values():
            types += type_
        question_type = 'others'

        question_types = []

    # 查询电影的类型
        if self.check_words(self.type_qwds, question) and 'movie_name' in types:
            question_type = 'movie_type'
            question_types.append(question_type)

    # 查询电影的主演
        if self.check_words(self.actor_qwds, question) and 'movie_name' in types:
            question_type = 'movie_actor'
            question_types.append(question_type)

    # 查询电影的导演
        if self.check_words(self.director_qwds, question) and 'movie_name' in types:
            question_type = 'movie_director'
            question_types.append(question_type)

    # 查询电影的上映时间
        if self.check_words(self.release_date_qwds, question) and 'movie_name' in types:
            question_type = 'movie_release_date'
            question_types.append(question_type)

        # 查询电影的剧情简介
        if self.check_words(self.introduction_qwds, question) and 'movie_name' in types:
            question_type = 'movie_introduction'
            question_types.append(question_type)

    # 查询某演员主演的电影
        if self.check_words(self.actor_movie_qwds, question) and 'actor' in types:
            question_type = 'actor_movie'
            question_types.append(question_type)

    # 查询某导演执导的电影
        if self.check_words(self.director_movie_qwds, question) and 'director' in types:
            question_type = 'director_movie'
            question_types.append(question_type)

    # 查询某类型的电影
        if self.check_words(self.type_movie_qwds, question) and 'movie_type' in types:
            question_type = 'type_movie'
            question_types.append(question_type)

        if self.check_words(self.release_date_movie_qwds, question) and 'release_date' in types:
            question_type = 'release_date_movie'
            question_types.append(question_type)

        if self.check_words(self.movie_name_qwds, question) and 'movie_name' in types:
            question_type = 'movie_error'
            question_types.append(question_type)

    # 若没有查到相关的外部查询信息，那么则将该电影的描述信息返回
        if question_types == [] and 'movie_name' in types:
            question_types = ['movie_error']

    # 将多个分类结果进行合并处理，组装成一个字典
        data['question_types'] = question_types

        return data


    '''构造词对应的类型'''
    def build_wdtype_dict(self):
        wd_dict = dict()
        for wd in self.region_words:
            wd_dict[wd] = []
            if wd in self.movie_name_wds:
                wd_dict[wd].append('movie_name')
            if wd in self.movie_type_wds:
                wd_dict[wd].append('movie_type')
            if wd in self.actor_wds:
                wd_dict[wd].append('actor')
            if wd in self.director_wds:
                wd_dict[wd].append('director')
            if wd in self.release_date_wds:
                wd_dict[wd].append('release_date')
            if wd in self.introduction_wds:
                wd_dict[wd].append('introduction')
        return wd_dict

    '''构造actree，加速过滤'''
    def build_actree(self, wordlist):
        actree = ahocorasick.Automaton()
        for index, word in enumerate(wordlist):
            actree.add_word(word, (index, word))
        actree.make_automaton()
        return actree

    '''问句过滤'''
    def check_movie(self, question):
        region_wds = []
        for i in self.region_tree.iter(question):
            wd = i[1][1]
            region_wds.append(wd)
        stop_wds = []
        for wd1 in region_wds:
            for wd2 in region_wds:
                if wd1 in wd2 and wd1 != wd2:
                    stop_wds.append(wd1)
        final_wds = [i for i in region_wds if i not in stop_wds]
        final_dict = {i: self.wdtype_dict.get(i) for i in final_wds}

        return final_dict

    

    '''基于特征词进行分类'''
    def check_words(self, wds, sent):
        for wd in wds:
            if wd in sent:
                return True
        return False

if __name__ == '__main__':
    handler = MovieQuestionClassifier()
    while 1:
        question = input('input a movie-related question:')
        data = handler.classify(question)
        #print(data)
