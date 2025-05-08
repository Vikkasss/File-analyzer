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
