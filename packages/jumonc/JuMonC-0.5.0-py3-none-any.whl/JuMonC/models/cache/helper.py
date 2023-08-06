from typing import Union

from JuMonC.models.cache.database import db_session
import JuMonC.models.cache.dbmodel as cache_model


def add_cache_entry(API_path:str) -> int:
    entry = cache_model.CacheEntry(API_path)
    db_session.add(entry)
    db_session.commit()
    
    return entry.cache_id


def addParameter(cache_id:int, parameter_name:str, parameter_value:str) -> None:
    parameter = cache_model.Parameter(cache_id, parameter_name, parameter_value)
    db_session.add(parameter)
    db_session.commit()

    
def addResult(cache_ID:int, result_name:str, result:Union[int,float,str]) -> None:
    
    if isinstance(result, int):
        result_entry = cache_model.ResultInt(cache_ID, result_name, result)
    elif isinstance(result, float):
        result_entry = cache_model.ResultFloat(cache_ID, result_name, result)
    elif isinstance(result, str):
        result_entry = cache_model.ResultStr(cache_ID, result_name, result)
    else:
        return
    db_session.add(result_entry)
    db_session.commit()