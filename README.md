### Запуск контейнеров в Docker
```
docker-compose up   # стандартный запуск всех тестов по умолчанию
docker-compose up --build  # запуск тестов с пересборкой docker-образа (при внесении изменений в Dockerfile)
docker-compose run tests -m smoke # запуск тестов с определённым маркером 
```
После запуска тестов результаты будут доступны вне контейнера в папке /allure-results
#### Получение доступа к allure-отчёту
```
allure serve # просмотр на локальном сервере
allure generate -c allure-results -o allure-report allure-results # генерация файлов с отчётами
```
---


### Примеры запуска тестов на разных окружениях

- **Dev окружение:**  
  `pytest -s --env=dev`

- **Stage окружение:**  
  `pytest -s --env=stage`

### Как открыть Allure-отчёт

После выполнения тестов в корне проекта появится папка `allure-results`.  
Для генерации и открытия отчёта выполнить:

`allure serve`