#!/usr/bin/env python3
""" models user session module """

from datetime import datetime
from models.base import Base


class UserSession(Base):
    """ user session class """
    def __init__(self, *args: list, **kwargs: dict):
        """ Init method """
        self.user_id = kwargs.get('user_id', None)
        self.session_id = kwargs.get('session_id', None)
        super().__init__(*args, **kwargs)

    def save(self):
        """ Save UserSession to the file-based database """
        # Implementation
        pass

    def delete(self):
        """ Delete UserSession from the file-based database """
        # implementation
        pass
