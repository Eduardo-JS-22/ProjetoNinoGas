from database.connection import *
from functions.billing_functions import *
from functions.client_functions import *
from functions.database_functions import *
from utils.date_utils import *

def main():
    print("Lista de Clientes: \n")
    list_clients()
    print("\nLista de Cobranças: \n")
    list_bills()

if __name__ == "__main__":
    main()