### Подготовка
Перед запуском парсера нужно установить 1 зависимость. Имя ее `requests`.
В командной строке windows вызвать команду:
`pip list`
В списке посмотреть наличие `requests`.
Если нет то устанавить командой
`pip install requests`

### Инициализация парсера
1. Создать рабочую директорию для 1 парсера. Поместить туда парсер.
2. Посмотреть в файл конфига. Думаю там понятно, что монять и как. Переменные сами за себя говорят.
3. Открыть командную строку Windows.
4. Перейти в рабочию директорию командой `cd C:\Users\login\Desktop\parser\Name`. Если на диске D
то такая команда `d:` и `cd D:\parser\Name`
4. Запуск парсера командой `python main.py`
5. Остановка парсера сочетание клавишь `Ctrl + C`

Что бы создать копию парсера нужно повторить инструкцию выше **Инициализация парсера**.
Важно в конфиге `result_path` изменить файл для записи, для того что бы не было конфликтов.

Внимательно будь если указываешь путь для сохранения результатов. То такая папка должны быть заранее созданна.

Так можно создать много парсеров и под разные сайты. Главное, что бы ответ от сайта был в формате json.


### Как добавлять формулы
Формулы находятся в файле `custom.py`.
Первая формула находится в функции `func01`. Вычисление и логика все происходит в функции.

Функция на вход принимает те данные которые приходят с сайта в переменой `data` и далее ты можешь с этими данными выполнять любые вычесления.

Допустим нужно добавить новую формулу. То это нужно создать новую функцию.
пример:
```
def func04(data):
    summ = 0
    for row in data['bids']:
        price  = float( row['price'] )
        summ  += price
    result = summ
    return result
```
и добавить ее в исполнительный лист `functions`

`functions = [ func01, func02, func03, func04]`

если расчет из func04 нужно подставить в результат первой то просто поменяй их местами.

`functions = [ func04, func01, func02, func03]`

это самый простой интерфейс из всех возможных.
добавил время рассчета формулы