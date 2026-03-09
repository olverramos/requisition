from modules.parameters.models import Ramo, FieldType, RamoField, \
    DocumentClass, DocumentClassType
    
def run():
    FieldType.init_table()
    DocumentClassType.init_table()
    DocumentClass.init_table()
    Ramo.init_table()
    print("Parameters Data Added!")
