from modules.operative.models import RequestStatus, OperativeRequest
    
def run():
    RequestStatus.init_table()
    OperativeRequest.init_table()
    print("Operative Data Added!")
