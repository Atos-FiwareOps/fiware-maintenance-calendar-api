class Validator():
    def __init__(self, schema_file, error=Exception):
        self.schema_file = schema_file
        self.error = error
    
    def validate(self, data):
        raise Exception("Not implemented")