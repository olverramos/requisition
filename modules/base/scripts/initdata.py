from modules.base.models import PersonType, DocumentType, Applicant
    
def run():
    PersonType.init_table()
    DocumentType.init_table()
    Applicant.init_table()
    print("Base Data Added!")
