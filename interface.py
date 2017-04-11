# -*- coding: utf-8 -*-

"""Interface de uso cli para varredor de máquinas compliance linux"""

import sqlalchemy
from prettytable import PrettyTable
import auxiliary

class Menu(object):
    """Menu para selecionar opções"""
    def __init__(self):
        self.validoption = [1,2,3,4,5,6]
        self.alive = 1
        self.logged = 0
        #implementar a sessão do sqlalchemy
        self.Session = auxiliary.ferramenta.dbconnection(22, 33, 44, 55)
        self.userlogged = ''
        self.permissions = 0
        self.user = auxiliary.user_handlers()
        self.machine = auxiliary.machine_handler()

    def criausuario(self):
        usuario = self.user.cria_user(self.Session)

    def menuinicial(self):
        t = PrettyTable(['[+] Option', '[+] Descricao'])
        t.add_row(['[1]', 'Criar um novo usuario'])
        t.add_row(['[2]', 'Logar como um usuario existente'])
        t.add_row(['[3]', 'Verificar tabela de maquinas no DB'])
        t.add_row(['[4]', 'Adicionar nova maquina na tabela de compliance'])
        t.add_row(['[5]', 'Verificar sub-rede'])
        t.add_row(['[6]', 'Aplicar correcoes de compliance em uma maquina'])
        t.add_row(['[7]', 'Deslogar.'])
        while True:
            logado = PrettyTable(['Logado como:'])
            logado.add_row([self.userlogged])
            print logado
            print t
            print "Digite a opcao desejada"
            x = raw_input()
            if x == None:
                pass
            if x == "1":
                self.criausuario()
            if x == "2":
                login = auxiliary.user_handlers()
                self.userlogged = login.login()
                if self.userlogged == "":
                    pass
                else:
                    self.logged = 1
            if x == "3":
                if self.logged == 0:
                    print "Voce nao esta logado para efetuar esta acao"
                else:
                    self.machine.get_all_machines()
            if x == "4":
                pass
            if x == "5":
                pass
            if x == "6":
                pass
            if x == "7":
                pass
            if x == "0":
                break

    def handle_logon(self):
    	print "Digite usuario (algartelecom)"
    	usertry = raw_input()
    	print "Digite senha"
    	passtry = raw_input()
    	founduser = self.Session.query(User).filter_by(user=usertry).first()
    	if not founduser:
    		print "Login incorreto, tente novamente"
    		return False
    	if founduser.user == usertry:
    		if founduser.password == passtry:
    			print "Login efetuado com sucesso como" + founduser.user
    			return founduser.user
    		else:
    			print "Login incorreto, tente novamente"
    			return False
    	else:
    		print "Login incorreto, tente novamente"
    		return False

firstone = Menu()
firstone.menuinicial()
