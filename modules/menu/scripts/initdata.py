from modules.menu.models import Option, Section
    
def run():
    Section.init_table()
    Option.init_table()
    print("Menu Data Added!")