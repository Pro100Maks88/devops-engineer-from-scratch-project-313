### Hexlet tests and linter status:
[![Actions Status](https://github.com/Pro100Maks88/devops-engineer-from-scratch-project-313/actions/workflows/hexlet-check.yml/badge.svg)](https://github.com/Pro100Maks88/devops-engineer-from-scratch-project-313/actions)
[![CI](https://github.com/Pro100Maks88/devops-engineer-from-scratch-project-313/actions/workflows/ci.yml/badge.svg)](https://github.com/Pro100Maks88/devops-engineer-from-scratch-project-313/actions/workflows/ci.yml)

## Link Shortener (Project DevOps)

Сокращатель ссылок на базе **FastAPI** и **SQLModel**. Проект разработан в рамках курса DevOps-инженера на Hexlet и демонстрирует навыки проектирования архитектуры, контейнеризации и деплоя облачных приложений.

## :closed_book: Требования
- **Docker** & **Docker Compose**
- **Make** (для удобного управления командами)
- **uv** (менеджер пакетов Python)

## :desktop_computer: Запуск

### Основной способ (Docker Compose)
Рекомендуется для проверки работоспособности и деплоя. 

1. Склонируйте репозиторий:
   ```bash
   git clone git@github.com:Pro100Maks88/devops-engineer-from-scratch-project-313.git
   cd devops-engineer-from-scratch-project-313
   ```

2. Запуск проекта через Docker Compose (автоматически поднимет БД, бэкенд и Nginx):
   ```bash
   make dev
   ```
Приложение будет доступно на http://localhost:8080

### Доступные команды

| Команда | Цель в Makefile | Описание |
| --- | --- | --- |
| `make dev` | `dev` | Поднимает контейнеры (приложение + БД) в фоновом режиме. Автоперезагрузка включена. |
| `make test` | `test` | Запускает тесты внутри контейнера с правильной переменной окружения DATABASE_URL. |
| `make lint` | `lint` | Проверяет код через ruff. |
| `make fix` | `fix` | Автоматически исправляет стилистические ошибки через ruff. |
| `make clean` | `clean` | Останавливает контейнеры, удаляет тома и очищает uv.lock. |

## :gear: Тестирование

Тесты покрывают основные CRUD-операции и логику редиректов. Перед каждым запуском база данных очищается, что гарантирует независимость тестов.

## :package: Деплой

Приложение развернуто на Render с использованием Docker-контейнеров:
[Демо-версия проекта]: https://devops-engineer-from-scratch-project-313-4tvi.onrender.com/


Проект выполнен в учебных целях на платформе [Hexlet](https://ru.hexlet.io/pages/about)
