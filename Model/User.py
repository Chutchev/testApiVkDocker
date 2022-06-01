user_json_scheme = {
    "type": ["object", "null"],
    "properties": {
        "first_name": {"type": "string"},
        "last_name": {"type": ["string", "null"]},
        "country": {"type": ["string", "null"]},
        "city": {"type": ["string", "null"]},
        "address": {"type": ["string", "null"]},
        "phone": {"type": ["string", "null"], "pattern": r"^((8|\+7)[\- ]?)?(\(?\d{3}\)?[\- ]?)?[\d\- ]{7,10}$"},
        "email": {"type": "string", "pattern": r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)"}
    }
}

users_json_scheme = {
    "type": "array",
    "items": user_json_scheme
}

