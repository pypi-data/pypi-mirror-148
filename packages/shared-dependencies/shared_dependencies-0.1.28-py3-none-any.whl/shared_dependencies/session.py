import json
from typing import Optional
from abc import ABC, abstractmethod
from redis import Redis

class SessionDb(ABC):
    def __init__(self):
        pass

    @abstractmethod
    def get(self):
        pass

    @abstractmethod
    def set(self):
        pass


class RedisSessionDb(SessionDb):
    def __init__(self, redis_client: Redis):
        self.redis_client = redis_client

    def get(self, id: str):
        return self.redis_client.get(id)

    def set(self, id: str, content: str, expiration_delay: int):
        return self.redis_client.set(id, content, expiration_delay)


class SessionManager:
    def __init__(self, session_id: str, session_db_client: SessionDb):
        self.session_id = session_id
        self.session_db_client = session_db_client

    def start_or_update_session(self, expiration_delay: int = 604800):
        return self.session_db_client.set(self.session_id, "True", expiration_delay)

    def get_session_status(self, refresh_session: bool = True):
        session_status = self.session_db_client.get(self.session_id)

        if session_status is not None:
            session_status_str = session_status.decode("utf-8")
            session_status_bool = json.loads(session_status_str.lower())

            if session_status_bool and refresh_session:
                # Refresh expiration delay
                self.start_or_update_session()

            return session_status_str

        else:
            return session_status

    def kill_session(self):
        return self.session_db_client.set(self.session_id, "False", 604800)