# -*- coding: utf-8 -*-

"""Interface de uso cli para varredor de máquinas compliance linux"""

import sqlalchemy
from prettytable import PrettyTable


class Menu(object):
    """Menu para selecionar opções"""
    def __init__(self):
        self.validoption = [1,2,3,4,5,6]
        self.alive = 1
        self.logged = 0
        #implementar a sessão do sqlalchemy
        self.Session = None
        self.userlogged = ''

    def menuinicial(self):
        t = PrettyTable(['[+] Option', '[+] Descricao'])
        t.add_row(['[1]', 'Criar um novo usuario'])
        t.add_row(['[2]', 'Logar como usuario do sistema'])
        t.add_row(['[3]', 'Verificar maquinas ja escaneadas no DB'])
        t.add_row(['[4]', 'Escanear nova maquina'])
        t.add_row(['[5]', 'Escanear sub-rede'])
        t.add_row(['[6]', 'Aplicar correcoes de compliance em uma maquina'])
        t.add_row(['[7]', 'Deslogar.'])
        logado = PrettyTable(['Logado como:'])
        logado.add_row([self.userlogged])
        print logado
        print t

firstone = Menu()
firstone.menuinicial()
