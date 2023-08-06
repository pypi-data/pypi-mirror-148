"""TAD Fila"""
from typing import List
fila = []

def limpar_tela()-> None:
    print('\n' * 100) #limpa a tela
    
def is_empty()-> bool:
    """Devolver True ou False se a fila estiver vazia"""
    resultado = True
    if fila == []:
        resultado = True
    else:
        resultado = False
    return resultado

def push(cliente)-> None:
    """Adiciona um cliente à lista de espera"""
    fila.append(cliente)
    
def get_elements()-> List:
	  """Retorna os clientes da lista de espera"""
	  return fila
	  
def atender()-> None:
	  """Atender o cliente da fila"""
	  cliente = int(input(f'Insira o cliente a ser atendido (1-{len(fila)})= '))
	  fila.remove(cliente - 1)
