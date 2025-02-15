
# Импортируем необходимые компоненты из библиотеки SQLAlchemy
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Указываем URL для подключения к базе данных SQLite
# В данном случае база данных будет находиться в файле `itproger.db` в текущей директории
SQL_DB_URL = 'sqlite:///./itproger.db'

# Создаем движок (engine) для работы с базой данных
# `create_engine` создает соединение с базой данных
# Параметр `connect_args={"check_same_thread": False}` позволяет использовать соединение в многопоточных приложениях
engine = create_engine(SQL_DB_URL, connect_args={"check_same_thread": False})

# Создаем фабрику сессий (sessionmaker) для работы с базой данных
# `sessionmaker` создает объекты сессий, которые используются для взаимодействия с базой данных
# Параметры:
# - `autoflush=False` — отключает автоматическую синхронизацию изменений с базой данных
# - `autocommit=False` — отключает автоматическое подтверждение транзакций
# - `bind=engine` — связывает сессии с созданным движком
session_local = sessionmaker(autoflush=False, autocommit=False, bind=engine)

# Создаем базовый класс для объявления моделей (таблиц) базы данных
# `declarative_base` возвращает базовый класс, от которого наследуются все модели
# Этот класс используется для создания таблиц и работы с ними через ORM
Base = declarative_base()