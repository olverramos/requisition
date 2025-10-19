from modules.parameters.models import Ramo, FieldType
    
def run():
    FieldType.init_table()
    Ramo.init_table()
    print("Parameters Data Added!")
