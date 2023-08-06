from datetime import datetime, date
import typing
import iso8601
import json
from bson import ObjectId


def is_jsonable(x):
    try:
        json.dumps(x)
        return True
    except (TypeError, OverflowError):
        return False


def datetime_parser(obj: typing.Union[dict, list, str]) -> typing.Union[dict, list, str]:
    """ Parsear las fechas de un diccionario a formato iso 8601

    :param obj: Diccionario, lista o string a parsear
    :type obj: Diccionario, lista o string
    :return: Diccionario, lista o string parseado
    :rtype: Diccionario, lista o string
    """
    if isinstance(obj, dict):
        for k, v in obj.items():
            if isinstance(v, dict) or isinstance(v, list):
                obj[k] = datetime_parser(v)
            if isinstance(v, str) and len(v) > 12:
                try:
                    obj[k] = iso8601.parse_date(v)
                except:
                    pass
    if isinstance(obj, list):
        for i, v in enumerate(obj):
            if isinstance(v, dict):
                obj[i] = datetime_parser(v)
            if isinstance(v, str) and len(v) > 12:
                try:
                    obj[i] = iso8601.parse_date(v)
                except:
                    pass
    return obj


def json_serial(dct: typing.Union[dict, list]) -> typing.Union[dict, list]:
    for k, v in dct.items():
        if isinstance(v, dict):
            dct[k] = json_serial(v)
        elif isinstance(v, (datetime, date)):
            dct[k] = v.isoformat()
        elif isinstance(v, list):
            dct[k] = list()
            for e in v:
                if isinstance(e, dict) or isinstance(e, list):
                    dct[k].append(json_serial(e))
                elif is_jsonable(e):
                    dct[k].append(e)
                else:
                    dct[k].append(str(e))
        else:
            if not is_jsonable(v):
                dct[k] = str(v)
    return dct


def format_ids(dct: dict) -> dict:
    """ Cambiar las claves de diccionario "_id" a "id"

    :param dct: diccionario con claves "_id"
    :type dct: dict
    :return: Diccionario modificado
    :rtype: dict
    """    
    r = dict()
    for k, v in dct.items():
        if k == "_id":
            r["id"] = v
        else:
            r[k] = v
    return r


def format_object_ids(dct: dict) -> dict:
    """ Crear un diccionario igual al que se recibe por parametro pero las \
        claves "id" se actualizan a "_id" y los valores de estas claves se \
        convierten a ObjectId

    :param dct: diccionario original
    :type dct: dict
    :return: diccionario actualizado
    :rtype: dict
    """    
    r = dict()
    for k, v in dct.items():
        if k == "id":
            r["_id"] = ObjectId(v)
        else:
            r[k] = v
    return r
