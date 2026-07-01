### Hexlet tests and linter status:
[![Actions Status](https://github.com/Pro100Maks88/devops-engineer-from-scratch-project-313/actions/workflows/hexlet-check.yml/badge.svg)](https://github.com/Pro100Maks88/devops-engineer-from-scratch-project-313/actions)
[![CI](https://github.com/Pro100Maks88/devops-engineer-from-scratch-project-313/actions/workflows/ci.yml/badge.svg)](https://github.com/Pro100Maks88/devops-engineer-from-scratch-project-313/actions/workflows/ci.yml)

## Link Shortener (Project DevOps)

Сокращатель ссылок на базе **FastAPI** и **SQLModel**. Проект разработан в рамках курса DevOps-инженера на Hexlet и демонстрирует навыки проектирования архитектуры, контейнеризации и деплоя облачных приложений.

## Требования
- **Docker** & **Docker Compose**
- **Make** (для удобного управления командами)
- **uv** (менеджер пакетов Python)

## Запуск

### Основной способ (Docker Compose)
Рекомендуется для проверки работоспособности и деплоя. 

1. Склонируйте репозиторий:
   ```bash
   git clone git@github.com:Pro100Maks88/devops-engineer-from-scratch-project-313.git
   cd devops-engineer-from-scratch-project-313
   ```
2. Запустите проект через Docker Compose (автоматически поднимет БД, бэкенд и Nginx):
   ```bash
   make up
   ```
Приложение будет доступно на http://localhost:8080

## Деплой

Приложение развернуто на Render с использованием Docker-контейнеров:
[Демо-версия проекта]: https://devops-engineer-from-scratch-project-313-4tvi.onrender.com/


Проект выполнен в учебных целях на платформе [Hexlet](https://ru.hexlet.io/pages/about)
