from typing import Dict, List


def sort_dict(dict_obj: Dict, descending=False):
    sorted_dict_obj = {k: v for k, v in
                       sorted(dict_obj.items(), key=lambda item: item[1],
                              reverse=descending)}
    return sorted_dict_obj


def sort_dict_list(dict_list: Dict, descending=False):
    sorted_dict_obj = {}
    for item in dict_list:

        # dicts
        list_data = dict_list[item][0]
        list_data = sort_dict(list_data, descending)

        sorted_dict_obj[item] = list_data

        # sort the list
    return sorted_dict_obj
