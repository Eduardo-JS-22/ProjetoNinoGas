import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from functions.client_functions import *
from functions.billing_functions import *

def main():
    print("Lista de Clientes: \n")
    list_clients()
    print("\nLista de Cobranças: \n")
    list_bills()

if __name__ == "__main__":
    main()