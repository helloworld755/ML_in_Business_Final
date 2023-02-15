# ML in business - Final project
Итоговый проект по курсу "Машинное обучение в бизнесе"

Стек:

ML: sklearn, pandas, numpy
API: flask
Данные: с kaggle - https://www.kaggle.com/datasets/adityakadiwal/water-potability

Step 1: https://colab.research.google.com/drive/1bpU2ryS9r-80sleVhPyeBlp_fxpqjevC

Step 2: https://colab.research.google.com/drive/1Tf37Yd4feHamOqpXvOM1gBHJ-dtzIrjg

Step 3: Jupyter Notebook

Все файлы из проекта: https://drive.google.com/drive/folders/1ZN41uFUEPByhPxvvlf0MqiOX0s1cqbKe?usp=share_link


Задача: определить, является ли вода пригодной для питья. Бинарная классификация

Используемые признаки:

- ph (float)
- Hardness (float)
- Solids (float)
- Chloramines (float)
- Sulfate (float)
- Conductivity (float)
- Organic_carbon (float)
- Trihalomethanes (float)
- Turbidity (float)

Целевая: Potability (int)

Модель: logreg
В рамках проекта были рассмотрены 13 моделей (см. файл Colab по ссылке выше).

### Клонируем репозиторий и создаем образ
```
$ git clone https://github.com/fimochka-sudo/GB_docker_flask_example.git
$ cd GB_docker_flask_example
$ docker build -t fimochka/gb_docker_flask_example .
```

### Запускаем контейнер

Здесь Вам нужно создать каталог локально и сохранить туда предобученную модель (<your_local_path_to_pretrained_models> нужно заменить на полный путь к этому каталогу)
```
$ docker run -d -p 8180:8180 -p 8181:8181 -v <your_local_path_to_pretrained_models>:/app/app/models fimochka/gb_docker_flask_example
```

### Переходим на localhost:8181
