import uuid

def generate_uuid():
    try:
        return str(uuid.uuid4())
    except Exception as e:
        return{
            "message":f"{str(e)}"
        }