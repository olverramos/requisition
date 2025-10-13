from modules.authentication.models import Genre, Role, Account
    
def run():
    Genre.init_table()
    Role.init_table()
    Account.init_table()
    print("Authentication Data Added!")    