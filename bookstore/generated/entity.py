
from sqlalchemy import Column, Index, Table, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql.sqltypes import *
from sqlalchemy.orm import declarative_base
from sqlalchemy.ext.associationproxy import association_proxy

Base = declarative_base()
metadata = Base.metadata


class Model(Base):
    """
    The base model for this project.
    """
    __tablename__ = 'Model'

    uid = Column(Integer(), primary_key=True, autoincrement=True , nullable=False )
    id = Column(Text(), nullable=False )
    created_at = Column(DateTime(), nullable=False )
    

    def __repr__(self):
        return f"Model(uid={self.uid},id={self.id},created_at={self.created_at},)"



    


class UserHasBought(Base):
    """
    None
    """
    __tablename__ = 'User_has_bought'

    User_uid = Column(Integer(), ForeignKey('User.uid'), primary_key=True)
    has_bought_uid = Column(Integer(), ForeignKey('Book.uid'), primary_key=True)
    

    def __repr__(self):
        return f"User_has_bought(User_uid={self.User_uid},has_bought_uid={self.has_bought_uid},)"



    


class Person(Model):
    """
    The base class of a human being.
    """
    __tablename__ = 'Person'

    uid = Column(Integer(), primary_key=True, autoincrement=True , nullable=False )
    name = Column(Text(), nullable=False )
    gender = Column(Text())
    date_of_birth = Column(Date())
    id = Column(Text(), nullable=False )
    created_at = Column(DateTime(), nullable=False )
    

    def __repr__(self):
        return f"Person(uid={self.uid},name={self.name},gender={self.gender},date_of_birth={self.date_of_birth},id={self.id},created_at={self.created_at},)"



    
    # Using concrete inheritance: see https://docs.sqlalchemy.org/en/14/orm/inheritance.html
    __mapper_args__ = {
        'concrete': True
    }
    


class Book(Model):
    """
    A book sold by the bookstore.
    """
    __tablename__ = 'Book'

    uid = Column(Integer(), primary_key=True, autoincrement=True , nullable=False )
    title = Column(Text(), nullable=False )
    ISBN = Column(Text(), nullable=False )
    genre = Column(Enum('Sci-fi', 'Fantasy', 'Crime', 'Thriller', 'Non-fiction', 'Biography', name='Genre'), nullable=False )
    id = Column(Text(), nullable=False )
    created_at = Column(DateTime(), nullable=False )
    

    def __repr__(self):
        return f"Book(uid={self.uid},title={self.title},ISBN={self.ISBN},genre={self.genre},id={self.id},created_at={self.created_at},)"



    
    # Using concrete inheritance: see https://docs.sqlalchemy.org/en/14/orm/inheritance.html
    __mapper_args__ = {
        'concrete': True
    }
    


class User(Person):
    """
    A customer of the bookstore.
    """
    __tablename__ = 'User'

    uid = Column(Integer(), primary_key=True, autoincrement=True , nullable=False )
    email = Column(Text())
    name = Column(Text(), nullable=False )
    gender = Column(Text())
    date_of_birth = Column(Date())
    id = Column(Text(), nullable=False )
    created_at = Column(DateTime(), nullable=False )
    
    
    # ManyToMany
    has_bought = relationship( "Book", secondary="User_has_bought")
    

    def __repr__(self):
        return f"User(uid={self.uid},email={self.email},name={self.name},gender={self.gender},date_of_birth={self.date_of_birth},id={self.id},created_at={self.created_at},)"



    
    # Using concrete inheritance: see https://docs.sqlalchemy.org/en/14/orm/inheritance.html
    __mapper_args__ = {
        'concrete': True
    }
    

