def isPredictDataValid(data):
    required_fields = ['video','url']
    for field in required_fields:
        if field not in data:
            return False
    return True