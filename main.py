import work_db


class Post(work_db.TabelsModel):
    '''
    Переменная для занесения ее в БД должны быть в виде:
    var_name = {'var':12, 'unique':'False', 'FK':None},
    где var_name - имя переменной, сама переменная должна быть в виде списка, где есть три обязательных поля
    var - значение переменной
    unique - уникальное или нет значение в БД(True/False)
    FK - внешний ключ на другой класс
    '''

    def __init__(self, title='title', user_id=1):
        self.title = {'var': title, 'unique': 'False', 'FK': None}
        self.user_id = {'var': user_id, 'unique': 'False', 'FK': 'User_id'}
        self.wrong_var = 1
        super().__init__()


class User(work_db.TabelsModel):
    #
    #
    '''
    Переменная для занесения ее в БД должны быть в виде:
    var_name = {'var':12, 'unique':'False', 'FK':None},
    где var_name - имя переменной, сама переменная должна быть в виде списка, где есть три обязательных поля
    var - значение переменной
    unique - уникальное или нет значение в БД(True/False)
    FK - внешний ключ на другой класс
    '''

    def __init__(self, name, age):
        self.name = {'var': name, 'unique': 'False', 'FK': None}
        self.age = {'var': age, 'unique': 'False', 'FK': None}
        self.simple = 4
        super().__init__()


# создание объектов
post1 = Post(title='Первый пост', user_id=1)
post2 = Post(title='Второй пост', user_id=3)
ivan = User(name='Ivan', age=25)
petr = User(name='Petr', age=38)
elena = User(name='Elena', age=22)
# # создание таблиц-вызвать хотя бы один раз для каждого класса
post1.create()
ivan.create()
# # создание или обновление записи
id = post1.update()
id = post2.update()
id = ivan.update()
id = petr.update()
id = elena.update()
# проверка обновления записи
post1.title['var'] = 'Исправленный первый пост'
id = post1.update()
petr.name['var'] = 'Petr Petrovich'
petr.age['var'] = 41
id = petr.update()

# Получение записи по шв
i = Post.get('Post', 3, 'User', 'Post.title', 'Post.id', 'User.name')
print(i)
i = Post.get('Post', 3, None, 'Post.title', 'Post.id', 'Post.user_id')
print(i)
