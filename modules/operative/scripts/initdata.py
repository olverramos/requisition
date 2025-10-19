from modules.operative.models import RequestStatus, Request
    
def run():
    RequestStatus.init_table()
    Request.init_table()
    print("Operative Data Added!")
