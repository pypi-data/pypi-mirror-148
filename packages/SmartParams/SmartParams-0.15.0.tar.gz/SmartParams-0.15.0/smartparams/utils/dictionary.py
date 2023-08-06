from typing import Any, Dict, List, Tuple

import smartparams.utils.string as strutil


def flatten_keys(
    obj: Any,
    prefix: str = '',
) -> List[str]:
    if not isinstance(obj, dict):
        return [prefix]

    keys = []
    for k, v in obj.items():
        keys.extend(flatten_keys(v, strutil.join_keys(prefix, k)))

    return keys


def find_nested(
    dictionary: Dict[str, Any],
    key: str,
    set_mode: bool = False,
    required: bool = False,
) -> Tuple[Dict[str, Any], str]:
    *nested_keys, last_key = key.split(strutil.KEY_SEPARATOR)

    key_list = list()
    for k in nested_keys:
        key_list.append(k)
        if k not in dictionary:
            if set_mode:
                dictionary[k] = dict()
            else:
                key_trace = strutil.KEY_SEPARATOR.join(key_list)
                raise KeyError(f"Param '{key_trace}' is not in dictionary.")

        if not isinstance(dictionary[k], dict):
            if set_mode:
                dictionary[k] = dict()
            else:
                key_trace = strutil.KEY_SEPARATOR.join(key_list)
                raise ValueError(f"Param '{key_trace}' is not dictionary.")

        dictionary = dictionary[k]

    if required and last_key not in dictionary:
        key_list.append(last_key)
        key_trace = strutil.KEY_SEPARATOR.join(key_list)
        raise KeyError(f"Param '{key_trace}' is not in dictionary.")

    return dictionary, last_key


def check_key_is_in(
    key: str,
    dictionary: Dict[str, Any],
) -> bool:
    key, _, sub_key = key.partition(strutil.KEY_SEPARATOR)
    if key not in dictionary:
        return False

    if not sub_key:
        return True

    dictionary = dictionary[key]

    if not isinstance(dictionary, dict):
        return True

    return check_key_is_in(
        key=sub_key,
        dictionary=dictionary,
    )
