# GDSC_dataset
# Этот репозиторий служит минимальным руководством по чтению датасета.  
Набор данных представляет информацию о реакции на лекарственные препараты с геномными профилями линий раковых клеток, это позволит исследователям изучать взаимосвязь между генетическими особенностями и чувствительностью к лекарственным препаратам.

Датасет доступен по ссылке: https://drive.google.com/drive/folders/1uyqS7bjqjAx7Fq_IT6OwHj-81zvFAFfB?usp=sharing 

## Требования:
- miniconda
- Python 3.12
- poetry
- jupyterlab
- pandas 
- matplotlib 
- wget

## Работа со скриптом:
Создайте переменное окружение с помощью:  
```conda create -n my_env python=3.12 pip```

Активируйте переменное окружение:  
```conda activate my_env```

Установите менеджер зависимостей и виртуальных окружений:  
```pip install poetry```

Создайте новый проект:  
```poetry new my_project```

Перейдите в созданную папку проекта:  
```cd my_project```

Добавьте следующие зависимости в проект:  
```poetry add jupyterlab pandas matplotlib wget```  
```poetry install —no-root```   

Активируйте скрипт data_loader.py:   
```python3 data_loader.py```


Результат работы скрипта:

![photo_2025-09-20_09-18-36](https://github.com/user-attachments/assets/34a67b1c-ff51-4bc3-bc4e-b74fa711be1b)
![photo_2025-09-20_09-18-36 (2)](https://github.com/user-attachments/assets/47539ec9-cb47-48e9-814a-4cff94bb7d82)

#Визуализация EDA
Полный разведочный анализ данных можно посмотреть здесь: https://nbviewer.org/github/itsmearinak/GDSC_dataset/blob/main/notebooks/EDA_1.ipynb 
