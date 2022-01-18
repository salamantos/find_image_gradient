### Установка
Желательно выполнять в virtualenv:
```
pip install -r requirements.txt
```

### Запуск
С поиском координат прямоугольников: `python main.py -f images/many_gradients.png --coordinates --plot`
Только вывод маски: `python main.py -f images/small_gradients.png --plot`
Не отображать результат через matplotlib, только запись в файл: `python main.py -f images/small_gradients.png`
Маска сохраняется в `images/small_gradients.png_mask.png`
