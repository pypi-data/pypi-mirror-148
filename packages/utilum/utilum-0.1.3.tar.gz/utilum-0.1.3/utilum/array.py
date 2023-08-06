def merge(current_array, new_array):
    for na in new_array:
        current_array.append(na)
    return current_array


def subtract(element, array):
    while element in array: array.remove(element)
    return array