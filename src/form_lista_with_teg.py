
import re
from src.setting import inf

def converter(list_for_convert):
    """Convert a list of data into a formatted list for display.

    Args:
        list_for_convert (list): A list containing the following elements:
            - metres (str or None): The distance in metres.
            - times (datetime): The time of the event.
            - firm (str or None): The name of the firm.
            - name (str or None): The name of the person.
            - uwagi (str or None): Additional notes.
            - przebieg (str or None): The route taken.
            - tel (str or None): The telephone number.
            - wenz (str or None): Additional information.
    Returns:
        tuple of list: A list containing the formatted data:
        - metres (str): The distance in metres, formatted as a string.
        - times (str): The time of the event, formatted as "HH:MM".
        - firm (str): The name of the firm, formatted as a string.
        - name (str): The name of the person, formatted as a string.
        - uwagi (str): Additional notes, formatted as a string.
        - przebieg (str): The route taken, formatted as a string.
        - tel (str): The telephone number, formatted as a string.
        - wenz (str): number of wenz, formatted as a string. 
    """    

    def convert_to_string(data):
        """Convert data to a cleaned string.

        Args:
            data (str or None): The data to be converted.

        Returns:
            str: A cleaned string representation of the data, or an empty string if the data is None or cannot be converted.
        """        
        if not data:
            return ""
        try:
            data = str(data)
            data = data.strip()
            data = re.sub(r"\s+", " ", data)
            data = re.sub(r"\s*\bNone\b", "", data)
            return data
        except (TypeError, ValueError):
            return ""
        
    
    metres, times, firm, name, uwagi, przebieg, tel, wenz, *_ = list_for_convert

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
    """Compare two lists of tuples and return modified lists with differences highlighted.

    Args:
        del_lista (list of tuples): The list of tuples to be deleted, where each tuple contains
        add_lista (list of tuples): The list of tuples to be added, where each tuple contains

    Returns:
        tuple: A tuple containing two lists:
            - del_lista_with_teg (list of lists): The modified list of tuples to be deleted, with differences highlighted.
            - add_lista_without_change (list of tuples): The modified list of tuples to be added, with matching elements removed.   
    """    
    matching_indices = []
    
    for index1, tuple1 in enumerate(del_lista):
        for index2, tuple2 in enumerate(add_lista):
            if tuple1[:3] == tuple2[:3]:
                matching_indices.append((index1, index2))
    del_lista, add_lista = make_list_with_teg(del_lista, add_lista, matching_indices)
    return del_lista, add_lista

def make_list_with_teg(del_lista, add_lista, matching_indices):
    """Create lists with highlighted differences and removed matching elements.

    Args:
        del_lista (list of tuples): The list of tuples there elements were deleted
        add_lista (list of tuples): The list of tuples there elements were added
        matching_indices (list of tuple): A list of tuples containing indices of matching elements in del_lista and add_lista.

    Returns:
        tuple: A tuple containing two lists:
            - del_lista_with_teg (list of lists): The modified list of tuples there elements were deleted, with differences highlighted and changed elements
            - add_lista_without_change (list of tuples): The modified list of tuples there were added
    """    
    del_lista_with_teg = del_lista
    add_lista_without_change = add_lista
    del_elem_from_add_lista = [tup[1] for tup in matching_indices]
    crossed_out_elements_in_del_lista = [tup[0] for tup in matching_indices]
    

    for matching in matching_indices: # added crossed out elements in del and bold elements in add
        item_del = del_lista[matching[0]]
        item_add = add_lista[matching[1]]

        for index, (elem1, elem2) in enumerate(zip(item_del, item_add)):
            if elem1 != elem2:
                change_elem = f"<b><s>{elem1}</s></b> <b><u>{elem2}</u></b>"
                del_lista_with_teg[matching[0]][index] =  change_elem # edded formatted element in del_lista_with_teg

    
    del_elem_from_add_lista.sort(reverse=True) # delete elements from add_lista without change
    for index in del_elem_from_add_lista:
        if 0 <= index < len(add_lista_without_change):
            del add_lista_without_change[index]
    
    for index, item in enumerate(del_lista): # cross out elements in del_lista_with_teg 
        if index not in crossed_out_elements_in_del_lista:
            new_item = []
            for elem in item:
                change_elem = f"<s>{elem}</s>"
                new_item.append(change_elem)

            del_lista_with_teg[index] = new_item

    

    return del_lista_with_teg, add_lista_without_change
