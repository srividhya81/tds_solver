import json

def sort_json_array(json_array=None, primary_key=None, secondary_key=None):
    """
    Sort a JSON array of objects by the value of the primary key field.
    In case of a tie, sort by the secondary key field if provided.

    Args:
        json_array (list, optional): List of JSON objects to sort. Defaults to the predefined array.
        primary_key (str): The primary key to sort by.
        secondary_key (str, optional): The secondary key to sort by in case of a tie.

    Returns:
        list: Sorted JSON array.
    """
    if json_array is None:
        json_array = [
            {"name": "Alice", "age": 66},
            {"name": "Bob", "age": 83},
            {"name": "Charlie", "age": 84},
            {"name": "David", "age": 37},
            {"name": "Emma", "age": 48},
            {"name": "Frank", "age": 33},
            {"name": "Grace", "age": 66},
            {"name": "Henry", "age": 93},
            {"name": "Ivy", "age": 18},
            {"name": "Jack", "age": 53},
            {"name": "Karen", "age": 94},
            {"name": "Liam", "age": 78},
            {"name": "Mary", "age": 42},
            {"name": "Nora", "age": 93},
            {"name": "Oscar", "age": 32},
            {"name": "Paul", "age": 32}
        ]

    return sorted(json_array, key=lambda x: (x[primary_key], x[secondary_key]) if secondary_key else x[primary_key])

json_data = [
        {"name": "Alice", "age": 66},
        {"name": "Bob", "age": 83},
        {"name": "Charlie", "age": 84},
        {"name": "David", "age": 37},
        {"name": "Emma", "age": 48},
        {"name": "Frank", "age": 33},
        {"name": "Grace", "age": 66},
        {"name": "Henry", "age": 93},
        {"name": "Ivy", "age": 18},
        {"name": "Jack", "age": 53},
        {"name": "Karen", "age": 94},
        {"name": "Liam", "age": 78},
        {"name": "Mary", "age": 42},
        {"name": "Nora", "age": 93},
        {"name": "Oscar", "age": 32},
        {"name": "Paul", "age": 32}
    ]

sorted_data = sort_json_array(json_data, "age", "name")
print(json.dumps(sorted_data, separators=(",", ":")))