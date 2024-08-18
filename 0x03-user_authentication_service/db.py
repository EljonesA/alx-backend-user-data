#!/usr/bin/env python3
"""
DB module
"""

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.session import Session
from sqlalchemy.exc import InvalidRequestError
from sqlalchemy.orm.exc import NoResultFound
from user import Base, User


class DB:
    """DB class
    """

    def __init__(self) -> None:
        """Initialize a new DB instance
        """
        self._engine = create_engine("sqlite:///a.db", echo=False)
        Base.metadata.drop_all(self._engine)
        Base.metadata.create_all(self._engine)
        self.__session = None

    @property
    def _session(self) -> Session:
        """Memoized session object
        """
        if self.__session is None:
            DBSession = sessionmaker(bind=self._engine)
            self.__session = DBSession()
        return self.__session

    def add_user(self, email: str, hashed_password: str) -> User:
        """Add a new user to the database

        Args:
            email (str): The user's email address.
            hashed_password (str): The user's hashed password.

        Returns: User-> The created User object.
        """
        new_user = User(email=email, hashed_password=hashed_password)
        self._session.add(new_user)
        self._session.commit()
        return new_user

    def find_user_by(self, **kwargs) -> User:
        """Find a user in the database by given keyword arguments.

        Args:
            **kwargs: Keyword arguments for filtering users.

        Returns: User - The found User object.

        Raises:
            NoResultFound: If no user is found with the given filters.
            InvalidRequestError: If the query has invalid arguments.
        """
        try:
            user = self._session.query(User).filter_by(**kwargs).one()
        except NoResultFound:
            raise NoResultFound("No user found with the provided filters.")
        except Exception as e:
            raise InvalidRequestError(f"Invalid query: {e}")
        return user

    def update_user(self, user_id: int, **kwargs) -> None:
        """Update the user's attributes in the database.

        Args:
            user_id (int): The ID of the user to update.
            **kwargs: Keyword arguments for updating user attributes.

        Returns: None

        Raises:
            ValueError - If an invalid attribute is passed in the keyword
            arguments.
        """
        # find user by user_id
        user = self.find_user_by(id=user_id)

        # get all valid attributes
        valid_attributes = {attr.key for attr in User.__table__.columns}

        # update user attributes
        for key, value in kwargs.items():
            if key not in valid_attributes:
                raise ValueError(f"Invalid attribute: {key}")
            setattr(user, key, value)

        # commit changes to the database
        self._session.commit()
