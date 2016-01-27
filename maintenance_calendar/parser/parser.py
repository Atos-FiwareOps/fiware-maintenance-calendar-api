class Parser(object):
    def to_dict(self, xml_data):
        raise NotImplementedError("Unrecognized mimetype or model type")
    
    def from_model(self, infrastructure):
        raise NotImplementedError("Unrecognized mimetype or model type")