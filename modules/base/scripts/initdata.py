from modules.base.models import Ramo, FieldType
    
def run():
    FieldType.init_table()
    Ramo.init_table()
    print("Base Data Added!")
