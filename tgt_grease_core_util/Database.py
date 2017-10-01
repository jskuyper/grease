import psycopg2
import psycopg2.extras
import os
import pymongo
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


class Connection(object):
    @staticmethod
    def create():
        return Connection()

    def __init__(self):
        if os.getenv('GREASE_DSN') is not None:
            self._connection = psycopg2.connect(dsn=os.getenv('GREASE_DSN'))
        else:
            raise EnvironmentError("Failed to find Grease database DSN")
        self._cursor = self._connection.cursor(cursor_factory=psycopg2.extras.DictCursor)

    def _reload(self):
        self._connection.close()
        self._connection = psycopg2.connect(dsn=os.getenv('GREASE_DSN'))
        self._cursor = self._connection.cursor(cursor_factory=psycopg2.extras.DictCursor)

    def execute(self, sql, parameters=None):
        # type: (str, tuple) -> None
        self._reload()
        if parameters:
            self._cursor.execute(sql, parameters)
        else:
            self._cursor.execute(sql)
        self._connection.commit()

    def query(self, sql, parameters=None):
        # type: (str, tuple) -> dict
        self._reload()
        if parameters:
            self._cursor.execute(sql, parameters)
        else:
            self._cursor.execute(sql)
        return self._cursor.fetchall()


SAEngine = None
SAsession = None


class SQLAlchemyConnection(object):
    """
        Provide access to PostgreSQL database created via SQLAlchemy
    """
    _config = None
    _engine = None
    _session = None

    def __init__(self, config):
        global SAEngine
        self._config = config
        if SAEngine is None:
            SAEngine = create_engine("{0}://{1}:{2}@{3}:{4}/{5}".format(
                self._config.get("GREASE_DB_ENGINE", "postgresql"),
                self._config.get("GREASE_DB_USER", "dev"),
                self._config.get("GREASE_DB_PASSWORD", "dev"),
                self._config.get("GREASE_DB_HOST", "localhost"),
                self._config.get("GREASE_DB_PORT", "5432"),
                self._config.get("GREASE_DB_DB", "")
            ))

    @staticmethod
    def get_engine():
        global SAEngine
        return SAEngine

    @staticmethod
    def get_session():
        global SAsession
        if not SAsession:
            session = sessionmaker(bind=SQLAlchemyConnection.get_engine())
            SAsession = session()
        return SAsession


class MongoConnection(object):
    def __init__(self):
        if not os.getenv('GREASE_MONGO_USER') and not os.getenv('GREASE_MONGO_PASSWORD'):
            self._client = pymongo.MongoClient(
                host=os.getenv('GREASE_MONGO_HOST', 'localhost'),
                port=os.getenv('GREASE_MONGO_PORT', 27017)
            )
        else:
            self._client = pymongo.MongoClient(
                "mongodb://{0}:{1}@{2}:{3}/{4}".format(
                    os.getenv('GREASE_MONGO_USER', ''),
                    os.getenv('GREASE_MONGO_PASSWORD', ''),
                    os.getenv('GREASE_MONGO_HOST', 'localhost'),
                    os.getenv('GREASE_MONGO_PORT', 27017),
                    os.getenv('GREASE_MONGO_DB', 'grease')
                )
            )

    def client(self):
        # type: () -> pymongo.MongoClient
        return self._client
