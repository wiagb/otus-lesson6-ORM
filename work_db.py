# Модуль содержит функции(создание-удаление таблиц, создание-удаление записей) для работы с БД sqlite
import sqlite3


class TabelsModel:
    # Имя базы данных
    name_db = 'db.sqlite3'

    def __init__(self):
        self.id_in_db = None

    def create(self):
        with sqlite3.connect(TabelsModel.name_db) as conn:
            try:
                cursor = conn.cursor()
                class_name = self.__class__.__name__  # получаю имя класса для создания имени таблицы
                good_vars = []
                add_fk = []

                for key_var in self.__dict__:
                    # для каждой переменной класса проверяю что она словарь (состоит из 3 объектов),
                    # объекты построены по определенному правилу (присутствуют ключи var, unique, FK)
                    attr = self.__dict__[key_var]  # attr - dict {'var':'', 'unique':'', 'FK':''}
                    if isinstance(attr, dict):  # переменная объекта соответствует для создания столбца в БД
                        if ('var' in attr) & ('unique' in attr) & ('FK' in attr) & (len(attr) == 3):
                            good_vars.append(key_var)
                            # если FK!=None создаем FOREIGN KEY
                            if attr['FK']:  # ключ получает название имякласса_id
                                # получаем список из 2 элементов ИмяТаблицы и НомерЗаписи
                                table_and_id = (str(attr['FK'])).split('_')
                                if len(table_and_id) > 2:
                                    print("Неверный формат FK.")
                                add_fk = ' FOREIGN KEY ({fk}_id) REFERENCES {fk}(id)'.format(fk=table_and_id[0])
                    else:
                        # атрибут не соответствует правилам для создания таблиц
                        pass

                # Хотя бы одна переменная объекта соответствует для создания столбца в БД
                if good_vars:
                    column = ','.join(good_vars)  # получаю перечень переменных через ',' для создания столбцов
                    column = column + ' ,id INTEGER PRIMARY KEY '  # все PRIMARY_KEY по умолчанию носят названия id
                    if add_fk:
                        sql = 'CREATE TABLE if not exists {table_name}({column}, {add_fk})'. \
                            format(table_name=class_name, column=column, add_fk=add_fk)
                    else:
                        sql = 'CREATE TABLE if not exists {table_name}({column})'. \
                            format(table_name=class_name, column=column)
                    cursor.execute(sql)
            finally:
                cursor.close()

    def update(self):

        with sqlite3.connect(TabelsModel.name_db) as conn:
            try:
                cursor = conn.cursor()
                class_name = self.__class__.__name__  # получаю имя класса для создания имени таблицы
                column = []
                value = []
                for_update = []

                for key_var in self.__dict__:
                    # для каждой переменной класса проверяю что она словарь (состоит из 3 объектов),
                    # объекты построены по определенному правилу (присутствуют ключи var, unique, FK)
                    attr = self.__dict__[key_var]  # attr - dict {'var':'', 'unique':'', 'FK':''}
                    if isinstance(attr, dict):  # переменная объекта соответствует для записи в БД
                        # print(key_var)
                        # print(attr['var'])
                        if ('var' in attr) & ('unique' in attr) & ('FK' in attr) & (len(attr) == 3):
                            # Для создания записи
                            column.append(key_var)
                            value.append(str(attr['var']))
                            # Для обновления записи
                            for_update.append(key_var + "='" + str(attr['var']) + "'")
                    else:
                        # атрибут не соответствует правилам для вставки
                        pass

                # Хотя бы одна переменная объекта соответствует для записи в БД
                if column:
                    # Такая запись есть-обновляем
                    if self.id_in_db:
                        for_update = ','.join(for_update)
                        sql = "UPDATE {table_name} SET {column} WHERE id={id_in_db}". \
                            format(table_name=class_name, column=for_update, id_in_db=self.id_in_db)
                        cursor.execute(sql)

                    # Такой записи нет-создаем
                    else:
                        column_ok = ','.join(column)  # столбцы
                        value_ok = "','".join(value)  # значения
                        sql = "INSERT INTO {table_name}({column}) VALUES('{values}')". \
                            format(table_name=class_name, column=column_ok, values=value_ok)
                        cursor.execute(sql)
                        conn.commit()
                        self.id_in_db = cursor.lastrowid
            finally:
                cursor.close()
        return self.id_in_db

    @staticmethod
    def get(main_table, id, join_table, *column):
        column_ok = []
        with sqlite3.connect(TabelsModel.name_db) as conn:
            try:
                cursor = conn.cursor()
                for key in column:
                    column_ok.append(key)  # столбцы
                column_ok = ','.join(column_ok)
                if join_table:  # запрос к таблице с FK и join
                    sql = "SELECT {column_ok} FROM {main_table} " \
                          "LEFT JOIN {join_table} ON {join_table}.id ={main_table}.{join_table}_id " \
                          "WHERE {main_table}.id={id_in_db}". \
                        format(column_ok=column_ok, main_table=main_table, join_table=join_table, id_in_db=id)
                else:  # запрос без join
                    sql = "SELECT {column_ok} FROM {main_table} WHERE {main_table}.id={id_in_db}". \
                        format(column_ok=column_ok, main_table=main_table, join_table=join_table, id_in_db=id)
                cursor.execute(sql)
                result = cursor.fetchone()
                return result

            finally:
                cursor.close()
