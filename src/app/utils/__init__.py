from flask_jwt_extended import create_access_token

def is_table_empty(query, table):
    if query == None:
        print(f"Populating {table}...")
        return True
    else:
        print(f"{table} is populated!")
        return False

def generate_jwt(payload):
    token = create_access_token(identity=str(payload["id"]), additional_claims=payload)

    return token
