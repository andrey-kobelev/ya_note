# YaNote  
  
> YaNote - электронная записная книжка для тех, кто не хочет ничего забыть и поэтому всё записывает.


## Как развернуть проект локально

Клонировать репозиторий и перейти в него в командной строке:

```
git clone https://github.com/andrey-kobelev/ya_note.git
```

```
cd ya_note
```

Cоздать и активировать виртуальное окружение:

```
python3 -m venv env  
```

```
source env/bin/activate  
```

Установить зависимости из файла requirements.txt:

```
python3 -m pip install --upgrade pip  
```

```
pip install -r requirements.txt  
```

Выполнить миграции:

```
python3 manage.py migrate  
```

Запустить проект:

```
python3 manage.py runserver  
```


## Запуск тестов: unittest

Чтобы увидеть развёрнутый список пройденных и проваленных тестов — запустите тесты с параметром `-v 2`

```
python manage.py test -v 2
```

