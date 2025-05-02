import ijson

def get_nested_value(record, attribute):
    keys = attribute.split(".")
    for key in keys:
        key = key.strip(":")
        if isinstance(record, dict):
            record = record.get(key)
        else:
            return None
    return record

def match_condition(record, attributes, operators, constants):
    if len(attributes) != len(operators) or len(attributes) != len(constants):
        raise ValueError("The number of attributes, operators, and constants must be the same.")
    
    for attribute, operator, constant in zip(attributes, operators, constants):
        value = get_nested_value(record, attribute)
        if value is None:
            return False
        
        if isinstance(value, list):

            if operator == "=":
                found = False
                for section in value:
                    for cat in section:
                        if(constant == cat):
                            found = True
                            continue
                    if found:
                        break
                if not found:
                    return False
            continue
        
        try:
            value = float(value)
            constant = float(constant)
        except ValueError:
            pass
        
        if operator == ">":
            if value <= constant:
                return False
        elif operator == ">=":
            if value < constant:
                return False
        elif operator == "=":
            if value != constant:
                return False
        elif operator == "<":
            if value >= constant:
                return False
        elif operator == "<=":
            if value > constant:
                return False
        else:
            return False
    return True


def query_top_k(file_path, attributes, operators, constants, k):
    results = []
    with open(file_path, 'r', encoding='utf-8') as f:
        items = ijson.items(f, 'item')
        for record in items:
            if match_condition(record, attributes, operators, constants):
                results.append(record)
                if len(results) >= k:
                    break
    return results[:k]

# #Example
# top_books = query_top_k(
#     "output.json",
#     attributes=["reviews_summary.avg_rating", "salesrank","categories"],
#     operators=["=", ">=", "="],
#     constants=[5.0, 100000,"Criticism & Theory[10207]"],
#     k=10,
# )

# for book in top_books:
#     print(book.get("title")+str(book.get("Id")))
