from modules.parameters.models import Ramo, FieldType, RamoField, DocumentClass
    
def run():
    FieldType.init_table()
    RamoField.init_table()
    DocumentClass.init_table()
    Ramo.init_table()
    print("Parameters Data Added!")
