1. Работает с версией sqlite3 от 2.6.0  
    В БД sqlite должны быть включены внешние ключи: foreign_key=on
2. Файл БД указывается в work_db.py  
nameDB = "db.sqlite3"
    
3. Для создания модели и соответственно таблицы в БД необходимо создать свой класс,
    наследуя его от TablesModel(расположен в work_db.py), например:  
    class User(work_db.TabelsModel)
    
    Чтобы атрибут класса стал столбцом в таблице его необходимо
     записывать в определенном виде:  
     self.name = {'var': name, 'unique': 'False', 'FK': None},  
     где 'var' это имя значение переменной,  
     'FK' ссылка на связанный класс(таблицу)
     FK должен быть записан как ИмяТаблицы_НомерЗаписи (например User_12)  
     ivan = User(name='Ivan')
     
    Для первого создания таблиц необходимо хотя бы у одного объекта вызвать create() 

4. Для получения значения записи необходимо вызвать статический метод
    result=get(main_table, id, join_table, *column)
    и передать имя главной таблицы, id записи, имя таблицы на которую есть FK
      и необходимо сделать JOIN (усли JOIN не нужен передать None) и перечень столбцов
      в виде ИмяТаблицы.ИмяСтолбца
        
    Возвращает кортеж значений запрошенной записи, в том порядке,
     в котором были перечислены столбцы в аргументе

Упрощения:
1. Считаю что таблицы и ключи, указанные в FK существуют
2. Не указываю типы данных, так как SQlite это позволяет
3. Нет защиты от sql injection.
4. Считаю что все FK имеют название ИмяКласса_id

