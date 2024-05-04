def isPredictDataValid(data):
    required_fields = ['video','video_url']
    for field in required_fields:
        if field not in data:
            return False
    return True