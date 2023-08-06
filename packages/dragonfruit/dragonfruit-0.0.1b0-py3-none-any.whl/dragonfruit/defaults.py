__all__ = ("DEFAULT_SETTINGS",)

DEFAULT_SETTINGS = {
    "rabbitmq": {
        "connection_params": "amqp://guest:guest@localhost",
        "task_timeout": 30,
        "task_queue": "dragonfruit-tasks",
    },
    "mongodb": {
        # These get passed directly to pymongo.MongoClient's constructor, see, e.g.:
        # https://api.mongodb.com/python/current/examples/authentication.html
        # should be a URI with the database to use
        "connection_params": "mongodb://127.0.0.1:27017/dragonfruit",
    },
}
