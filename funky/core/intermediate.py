
class Module:

    def __init__(self, module_id, body):
        self.module_id  =  module_id
        self.body       =  body

class Statement:
    pass

class TypeDefinition:

    def __init__(self, identifier, typ):
        self.identifier  =  identifier
        self.typ         =  typ
