
import re

def converter(list_for_convert):
    # print(type(list_for_convert), len(list_for_convert))

    def convert_to_string(data):
        if not data:
            return ""
        try:
            data = str(data)
            data = data.strip()
            data = re.sub(r"\s+", " ", data)
            return data
        except (TypeError, ValueError):
            return ""
        
    
    metres, times, firm, name, uwagi, przebieg, tel, wenz = list_for_convert

    times = times.strftime("%H:%M")
    if tel:
        if isinstance(tel, float):
            tel = str(int(tel)).strip()
        elif isinstance(tel, str):
            tel = tel.strip()
    else:
        tel = ""

    przebieg = convert_to_string(przebieg)
    firm = convert_to_string(firm)
    name = convert_to_string(name)
    tel = convert_to_string(tel)
    uwagi = convert_to_string(uwagi)
    metres = convert_to_string(metres)
            
    return [metres, times, firm, name, uwagi, przebieg, tel, wenz]


def compare_lists_by_tuples(del_lista, add_lista):
    matching_indices = []
    
    for index1, tuple1 in enumerate(del_lista):
        for index2, tuple2 in enumerate(add_lista):
            if tuple1[:3] == tuple2[:3] and tuple1[6] == tuple2[6]:
                matching_indices.append((index1, index2))
    del_lista, add_lista = make_list_with_teg(del_lista, add_lista, matching_indices)
    return del_lista, add_lista

def make_list_with_teg(del_lista, add_lista, matching_indices):
    del_lista_with_teg = del_lista
    add_lista_without_change = add_lista
    del_elem_from_add_lista = [tup[1] for tup in matching_indices]
    crossed_out_elements_in_del_lista = [tup[0] for tup in matching_indices]
    

    for matching in matching_indices:
        item_del = del_lista[matching[0]]
        item_add = add_lista[matching[1]]

        for index, (elem1, elem2) in enumerate(zip(item_del, item_add)):
            if elem1 != elem2:
                change_elem = f"<s>{elem1}</s> <u>{elem2}</u>"
                del_lista_with_teg[matching[0][index]] =  change_elem

    
    del_elem_from_add_lista.sort(reverse=True)
    for index in del_elem_from_add_lista:
        if 0 <= index < len(add_lista_without_change):
            del add_lista_without_change[index]
    
    for index, item in enumerate(del_lista):
        if index not in crossed_out_elements_in_del_lista:
            new_item = []
            for elem in item:
                change_elem = f"<s>{elem}</s>"
                new_item.append(change_elem)

            del_lista_with_teg[index] = new_item

    

    return del_lista_with_teg, add_lista_without_change
