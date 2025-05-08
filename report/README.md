# Анализ файлов

Микросервисная система для анализа текстовых отчетов с функцией сравнения файлов.

## Структура проекта

```
File_Tracking/
├── api_gateway/                   # API Gateway: маршрутизация запросов
│ ├── app/
│ │ ├── init.py
│ │ ├── main.py                    # Точка входа
│ │ └── routes.py                  # Эндпоинты
│ ├── Dockerfile
│ └── requirements.txt
├── file_analysis_service/         # Сервис анализа файлов
│ ├── app/
│ │ ├── init.py                    
│ │ ├── main.py                    # Точка входа
│ │ ├── utils.py                   # ??
│ │ ├── models.py                  
│ │ ├── routers.py                 # Эндпоинты
│ │ └── database.py                # Взаимодействие с PostgreSQL
│ ├── Dockerfile
│ └── requirements.txt
├── file_storing_service/          # Хранилище файлов 
│ ├── app/
│ │ ├── storage/                   # Папка для хранения добавленных файлов
│ │ ├── init.py                    
│ │ ├── main.py                    # Точка входа
│ │ ├── models.py                  
│ │ ├── routers.py                 # Эндпоинты
│ │ └── database.py                # Взаимодействие с PostgreSQL
│ ├── Dockerfile
│ └── requirements.txt
├── postgres/                    
│ └── init.sql               
├── tests/                         # Юнит-тесты и интеграционные тесты
├── docker-compose.yml             # Оркестрация контейнеров
├── README.md                      # Эта документация
└── requirements.txt               # Общие зависимости
```

## Основные компоненты

### Микросервисы
1. **API Gateway** (порт 8000):
   - Маршрутизация запросов к другим сервисам
   - Обработка ошибок (например, если сервис недоступен)
   - Пример эндпоинта: `POST /api/upload`

2. **File Analysis Service** (порт 8001):
   - Сравнение файлов на схожесть (по хешу)
   - Интеграция с WordCloudAPI для генерации облака слов (доп. функционал) ?? 
   - Ведение метаданных в PostgreSQL

3. **File Storing Service** (порт 8002):
   - Сохранение файлов в файловую систему
   - Выдача файлов по ID
   - Ведение метаданных в PostgreSQL

### База данных
- **PostgreSQL**: таблицы `files` (id, location, hash) и `statistics` (id, hash, content).

## Запуск проекта

### Требования
- Docker 20.10+
- Docker Compose 2.0+

### Инструкция
1. Клонировать репозиторий:
   ```bash
   git clone https://github.com/your-repo/text-scanner.git
   cd text-scanner
   ```
   
2. Переходим в папку проекта

```bash
   C:\Users\Acer\Desktop\Repositories\File_Tracking> 
```

3. Запускаем контейнер

```bash
    docker-compose up --build
```
Во время запуска `docker-compose.yml` будет написано очень много строк), в которых будет запускаться 4 образа: `postgres`, `DockerFile` для каждого сервиса и api.
В конце должно выйти такие строки: 

![img.png](for _the_report/img.png)
![img_1.png](for _the_report/img_1.png)

На фотографиях видно, что успешно мы запустили `postgres`, создав две бд (фото 2), а также успешно запустили два сервиса (`file-storing-1`, `file-analysis-1`) и маршрутизатор для них (`api-gateway-1`).

Далее в этом терминале нам будут приходить логи от запросов `get`, `post`

4. Переходим по [link](http://localhost:8000/docs#/) 

И можем тестировать наши запросы: 

![img_2.png](for _the_report/img_2.png)

Добавим три файла формата `.txt` (находятся в папке `for_the_report`), где два одинаковых и один нет.


5. В отдельном терминале можно проверить сохранение загруженных файлов, наличие созданных бд: 

```bash
    PS C:\Users\Acer> docker exec file_tracking-file-storing-1 ls /app/storage    #мой запрос на просмотр добавленных файлов
    196ce1e5-7496-473b-beca-d475f0be4fc6.txt                                      #вывод
    27c4c22a-ed49-4f6b-a088-f7f2af6a82e8.txt 
    9c6e9857-dd81-457e-a1b0-e32aba4a3ae5.txt
    fcdf3e9f-6cdf-46bf-abc6-3a743b4d251c.txt
```
Название файлов соотвествует их `file_id` из таблицы `files`