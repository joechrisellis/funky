
class CConstruct:
    """Superclass."""
    pass

class CProgram(CConstruct):

    def __init__(self, c_statements):
        super().__init__(self)
        self.c_statements = c_statements

class CDeclaration(CConstruct):
    
    def __init__(self, typ, name):
        super().__init__(self)
        self.name = 

class CStruct(CConstruct):
    
    def __init__(self, identifier, declarations):
        super().__init__(self)
