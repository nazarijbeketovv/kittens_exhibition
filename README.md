# Онлайн выставка котят API

## Установка 

### Предварительные требования
- Установленный Docker
- Установленный Docker Compose

### Предварительные требования
- БД заполнена тестовыми данными:

У каждого юзера логин: user_x (0 <= x <= 49), пароль: password123


### Шаги для установки и запуска

1. **Клонируйте репозиторий**
   ```bash
   git clone https://github.com/nazarijbeketovv/kittens_exhibition
   cd kittens_exhibition
   ```

2. **Запустите Docker контейнеры**
   ```bash
   docker-compose up --build
   ```

3. **Создайте суперпользователя**
   ```bash
   docker-compose exec -ti web-app python manage.py createsuperuser 
   ```

## Запуск тестов

```bash
docker-compose exec web-app pytest -v
```

## Документация

- Документация API будет доступна по адресу: http://localhost:8000/swagger/