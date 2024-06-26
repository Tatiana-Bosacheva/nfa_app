# Как собрать docker-образ

Docker создает образ на основе файла Dockerfile, в котором описываются необходимые команды.

Инструкция FROM задает базовый образ

  ```
  FROM python:3.11-alpine
  ```

Инструкция WORKDIR задаёт рабочую директорию для следующей инструкции
  
  ```
  WORKDIR /application
  ```

Инструкция RUN выполняет команду и создаёт слой образа (в данном случае мы обновляем pip)
  
  ```
  RUN python -m pip install --upgrade pip
  ```

Инструкция COPY копирует в контейнер файлы и папки (в данном случае мы добавляем файл с зависимостями в рабочую дирректорию)
  
  ```
  COPY requirements.txt /application
  ```

Инструкция RUN выполняет команду и создаёт слой образа (в данном случае мы устанавливаем все необходимые зависимости)
  
  ```
  RUN pip install -r requirements.txt
  ```

Инструкция COPY копирует в контейнер файлы и папки (в данном случае мы добавляем все файлы в рабочую дирректорию)
  
  ```
  COPY . /application
  ```

Инструкция CMD описывает команду с аргументами, которую нужно выполнить когда контейнер будет запущен
  
  ```
  CMD ["python", "liq_rates.py"]
  ```


Для того, чтобы собрать docker-образ, необходимо выполнить следующую команду 

```
docker build --tag nfa_app .    
```
где nfa_app - название нашего образа



# Как запустить docker-образ

Чтобы запустить образ, нелбходимо выполнить команду run с названием нашего образа

```
docker run nfa_app   
```
