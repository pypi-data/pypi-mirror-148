import logging

import datetime
from sqlalchemy import Column, Integer, String, DATETIME, ForeignKey, Float
from sqlalchemy.orm import relationship


from JuMonC.models.cache.database import Base


logger = logging.getLogger(__name__)

class CacheEntry(Base):
    __tablename__ = 'cache_entry'
    cache_id = Column(Integer, primary_key=True)
    time = Column(DATETIME, unique=False)
    API_path = Column(String(120), unique=False)
    
    parameters = relationship("Parameter",
                                  back_populates="cache_entry",
                                  cascade="all, delete",
                                  passive_deletes=True
                             )
    
    results_int = relationship("ResultInt",
                                  back_populates="cache_entry",
                                  cascade="all, delete",
                                  passive_deletes=True
                             )
    
    results_float = relationship("ResultFloat",
                                  back_populates="cache_entry",
                                  cascade="all, delete",
                                  passive_deletes=True
                             )
    
    results_str = relationship("ResultStr",
                                  back_populates="cache_entry",
                                  cascade="all, delete",
                                  passive_deletes=True
                             )

    def __init__(self, API_path:str) -> None:
        """DB class!"""
        self.time = datetime.datetime.now()
        self.API_path = API_path

    def __repr__(self) -> str:
        """DB to string method."""
        return f'<cache_id {self.cache_id!r}, time {self.time!r}, API_path {self.API_path!r}>'

    
class Parameter(Base):
    __tablename__ = 'parameter'
    parameter_id = Column(Integer, primary_key=True)
    cache_id = Column(Integer, ForeignKey('cache_entry.cache_id', ondelete="CASCADE"))
    parameter_name = Column(String(60), unique=False)
    parameter_value = Column(String(40), unique=False)
    
    cache_entry = relationship("CacheEntry", back_populates="parameters")

    def __init__(self, cache_id:int, parameter_name:str, parameter_value:str) -> None:
        """DB class!"""
        self.cache_id = cache_id
        self.parameter_name = parameter_name
        self.parameter_value = parameter_value

    def __repr__(self) -> str:
        """DB to string method."""
        return (f'<parameter_id {self.parameter_id!r}, cache_id {self.cache_id!r}, '
                f'parameter_name {self.parameter_name!r}, parameter_value {self.parameter_value!r}>')

    
class ResultInt(Base):
    __tablename__ = 'results_int'
    result_int_id = Column(Integer, primary_key=True)
    cache_id = Column(Integer, ForeignKey('cache_entry.cache_id', ondelete="CASCADE"))
    result_name = Column(String(60), unique=False)
    result = Column(Integer, unique=False)
    
    cache_entry = relationship("CacheEntry", back_populates="results_int")

    def __init__(self, cache_id:int, result_name:str, result:int) -> None:
        """DB class!"""
        self.cache_id = cache_id
        self.result_name = result_name
        self.result = result

    def __repr__(self) -> str:
        """DB to string method."""
        return f'<result_int_id {self.result_int_id!r}, cache_id {self.cache_id!r}, result_name {self.result_name!r}, result {self.result!r}>'

    
class ResultFloat(Base):
    __tablename__ = 'results_float'
    result_float_id = Column(Integer, primary_key=True)
    cache_id = Column(Integer, ForeignKey('cache_entry.cache_id', ondelete="CASCADE"))
    result_name = Column(String(60), unique=False)
    result = Column(Float, unique=False)
    
    cache_entry = relationship("CacheEntry", back_populates="results_float")

    def __init__(self, cache_id:int, result_name:str, result:float) -> None:
        """DB class!"""
        self.cache_id = cache_id
        self.result_name = result_name
        self.result = result

    def __repr__(self) -> str:
        """DB to string method."""
        return f'<result_float_id {self.result_float_id!r}, cache_id {self.cache_id!r}, result_name {self.result_name!r}, result {self.result!r}>'

    
class ResultStr(Base):
    __tablename__ = 'results_str'
    result_str_id = Column(Integer, primary_key=True)
    cache_id = Column(Integer, ForeignKey('cache_entry.cache_id', ondelete="CASCADE"))
    result_name = Column(String(60), unique=False)
    result = Column(String(60), unique=False)
    
    cache_entry = relationship("CacheEntry", back_populates="results_str")

    def __init__(self, cache_id:int, result_name:str, result:str) -> None:
        """DB class!"""
        self.cache_id = cache_id
        self.result_name = result_name
        self.result = result

    def __repr__(self) -> str:
        """DB to string method."""
        return f'<result_str_id {self.result_str_id!r}, cache_id {self.cache_id!r}, result_name {self.result_name!r}, result {self.result!r}>'
    
def log_load() -> None:
    logging.info("Package containing the DB model loaded")