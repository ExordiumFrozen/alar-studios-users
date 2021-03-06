## Task 1
---

### Общие сведения
Задача решена с помощью POST и FORMS.  

Роли:

- 0 - admin;
- 1 и выше - regular user

Первый пользователь с id=1 - первый административный пользователь с полными правами.  
В проекте запрещено его удаление и редактирование даже другими администраторами, в том числе, и ему самому.  

Другие создаваемые администраторы имеют полные права за исключением прав на операции с первым администратором.

Живое и работающее демо доступно здесь:  
http://alar-studios-users.holocron.io

Данные для входа:  
```
username admin@example.com
password nthvbyfnjh

username user@example.com
password 12345678
```

### Окружение, установка и запуск
Задача решена с помощью python 3.4.

Подразумевается, что проект будет запускаться на Ubuntu 14.04 x64.

Установка необходимых пакетов
```
sudo apt-get install libmysqlclient-dev python3-pip libffi-dev
```

```
sudo pip3 install virtualenv
```

Клонируем проект
```
git clone git@github.com:ExordiumFrozen/alar-studios-users.git
cd alar-studios-users
```

Подразумевается, что mysql уже установлен и готов к работе.
Если нет, то:
```
sudo apt-get install mysql-server
```

Создаем базу для работы:
```
mysql -u root -p
create database task1_exordium;
grant all privileges on task1_exordium.* to 'task1_exordium'@'%' identified by 'task1_exordium'
flush privileges
```

Настраиваем окружение, инициируем базу и выполняем миграцию для создания таблиц:
```
virtualenv .
source bin/activate
pip install -r requirements.txt
python migrate.py db init
python migrate.py db migrate
python migrate.py db upgrade
```

Создаем первого пользователя:
```
mysql -u task1_exordium -ptask1_exordium task1_exordium

INSERT INTO user (username,password,name,role) VALUES ('admin@example.com','pbkdf2:sha1:1000$5WwSX60G$0574ef2734fc0deb05312dd20255dffba381f68e','Admin',0);
```

Запускаем проект:
```
gunicorn -w 2 -b 127.0.0.1:8000 app:app
```

После этого можно зайти по адресу http://127.0.0.1:8000, ввести приведенные выше учетные данные и начать использование сервиса.

Все описанные здесь действия приведены в файлах проекта:
```
seed.txt
install txt
requirements.txt
```

В каталоге `system_configs` приведены файлы для nginx и upstart, которые используются на живом демо.


### Описание решения задачи
Все условия, поставленные в задаче, выполнены.  

1. Есть первый администратор с полными правами.
1.1. С этим администратором из интерфейса и кода проекта ничего нельзя сделать.  Другим администраторам при попытке сделать можификацию вернется 403;
2. Можно создавать, редактировать и удалять пользователей.
3. Страницы проекта:
    - /login - вход
    - /logout - выход
    - /, /index, /index/NUMBER - корневая страница, пагинация
    - /add - добавление нового пользователя с помощью FORM
    - /add-with-request - добавление новго пользователя с помощью request
    - /edit/ID - редактирование пользователя (кнопка Edit)
    - /delete/ID - удаление пользователя (кнопка Remove)
    - /test500page - страница для тестирования 5xx ошибок
4. Все действия доступны только залогиненным пользователям.
5. Использована sqlalchemy и mysql.
6. Сид базы:
    - создание базы вручную;
    - создание таблиц - с помощью миграции;
    - создание первого проектного пользователя вручную.

Для решения был выбраны:
- python 3.4;
- flask;
- bootstrap;

Все модели, формы, контроллеры и шаблоны написаны с нуля.  
Из готового использовался только голый Bootstrap, с помощью которого построены все страницы.  
Старался выдержать их в одном стиле.  


### Что можно было сделать лучше в данной реализации
Я специально не пишу все подробности реализации, по коду их видно.  

Если бы было доступно больше времени, а также при наличии большего опыта, в данной реализации сделал бы еще вот что:
- улучшил валидацию и обработку ошибок во всех важных местах;
- улучшил валидацию форм;
- улучшил отображение пользовательских ошибок (введение неправильных данных и тому подобное). Например, не очевидно, что поле пароля при редактировании пользователя является необязательным.
- написал тесты;
- пользовательские сессии в redis/mysql;
- кеширование select запросов в redis/memcached и инвалидация кеша при обнолении/удалении записей.


### Как бы я решил задачу при наличии чуть большего количества опыта в разработке:
1. rest api;
2. frontend в виде single page application на основе react;
3. авторизация с помощью oauth2 (в первую очередь со своим провайдером).
4. адекватная работа приложения на основных типах устройств, включая мобильные устройства и планшеты (в текущей реализации просто не хватило времени на то, чтобы сделать это).


### Дополнительные сведения
Это первое мое web-приложение на python.  
Это первое мое web-приложение на flask.  
Это первое мое web-приложение в принципе.  

До этого момента мой опыт в разработке заключался в написании вспомогательных скпритов для выполнения задач системного администрирования и devops.  

К задаче подошел с багажом в виде прочитанной документации по flask и своим опытом в смежной деятельности.  

На решение этой задачи потрачено 13 часов.


