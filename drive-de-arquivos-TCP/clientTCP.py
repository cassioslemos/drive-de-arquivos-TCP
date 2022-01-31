from socket import *
from tkinter import Tk
from tkinter.filedialog import askopenfilename
import base64
import ftplib
import time

teste="ENV".encode("utf-8")
op=1
serverName='25.78.211.38'
serverPort= 12000
while (op!="0"):
        op=input( 'Escolha uma opção:\n\n1- Criar Login\n2- Fazer Login\n0- Sair\n\nOpção: ' )
        if op=="1":
                email=input('Digite seu email: ')
                while(email.find(" ")!=-1 or email.find("@")==-1):
                        print("\nInsira um endereço de email válido!\n")
                        email=input('Digite seu email: ')
                user=input('Escolha um nome de usuário (não conter espaço \ /|<>*:"): ')
                while(user.find(" ")!=-1 or user.find("\\")!=-1 or user.find("/")!=-1 or user.find("|")!=-1 or user.find("<")!=-1 or user.find(">")!=-1 or user.find("*")!=-1 or user.find(":")!=-1 or user.find('"')!=-1):
                        print("\nInsira um nome de usuário válido!\n")
                        user=input('Escolha um nome de usuário (não conter espaço \ /|<>*:"): ')
                senha=input('Digite sua senha(não utilizar espaço): ')
                while(senha.find(" ")!=-1):
                        print("\nSenha inválida! escolha uma senha sem espaço!\n")
                        senha=input('\nDigite sua senha(não utilizar espaço): ')
                confsenha=input('Digite sua senha novamente: ')
                while(senha!=confsenha):
                        print("\nas senhas não batem! Digite novamente!\n")
                        senha=input('\nDigite sua senha(não utilizar espaço): ')
                        while(senha.find(" ")!=-1):
                                print("\nSenha inválida! escolha uma senha sem espaço!\n")
                                senha=input('\nDigite sua senha(não utilizar espaço): ')
                        confsenha=input('Digite sua senha novamente: ')
                aux=("CRI "+email+" "+user+" "+senha)
                aux_byte=aux.encode("utf-8")
                message=base64.b64encode(aux_byte)
                clientSocket = socket(AF_INET, SOCK_STREAM)
                clientSocket.connect((serverName,serverPort))
                clientSocket.send(message)
                resultado = clientSocket.recv(1024)
                print(resultado.decode("utf-8"))
                clientSocket.close()
        elif op=="2":
                email=input('Digite seu email: ')
                senha=input('Digite sua senha: ')
                if email.find(" ")==-1 and senha.find(" ")==-1 :
                        aux=("LOG "+email+" "+senha)
                        aux_byte=aux.encode("utf-8")
                        message=base64.b64encode(aux_byte)
                        clientSocket = socket(AF_INET, SOCK_STREAM)
                        clientSocket.connect((serverName,serverPort))
                        clientSocket.send(message)
                        resultado = clientSocket.recv(1024)
                        clientSocket.close()
                        print(resultado.decode("utf-8"))
                        if(resultado.decode("utf-8")!="\nEmail e/ou senha inválidos!\n"):
                                op=1
                                while(op!=0):
                                        op=input( '\nEscolha uma opção:\n\n1- Enviar arquivo\n2- Baixar Arquivo\n3- Deletar arquivo do servidor\n4- Listar arquivos\n5- Deletar Login\n0- Logoff\n\nOpção: ' )
                                        if(op=="1"):
                                                filename = ''
                                                root = Tk()
                                                root.attributes("-topmost",True)
                                                root.withdraw()
                                                filename = askopenfilename()
                                                if(filename!=''):
                                                        clientSocket = socket(AF_INET, SOCK_STREAM)
                                                        clientSocket.connect((serverName,serverPort))
                                                        message="USU "+email
                                                        message=message.encode("utf-8")
                                                        message=base64.b64encode(message)
                                                        clientSocket.send(message)
                                                        usuario = clientSocket.recv(1024)
                                                        clientSocket.close()
                                                        i=filename.rfind('/')
                                                        nome=filename[i:]
                                                        usuario=base64.b64decode(usuario)
                                                        usuario=usuario.decode("utf-8")
                                                        clientSocket = socket(AF_INET, SOCK_STREAM)
                                                        clientSocket.connect((serverName,serverPort))
                                                        message="ENV".encode("utf-8")+usuario.encode("utf-8")+nome.encode("utf-8")
                                                        message=base64.b64encode(message)
                                                        clientSocket.send(message)
                                                        print("\nEnviando...\n")
                                                        with open(filename,"rb") as arquivo:
                                                                #i=0
                                                                for dados in arquivo.readlines():
                                                                        clientSocket.sendall(dados)
                                                                        time.sleep(0.001)
                                                                        #print(i)
                                                                        #i=i+1
                                                        arquivo.close()
                                                        clientSocket.shutdown(SHUT_WR)
                                                        resultado=clientSocket.recv(1024)
                                                        resultado=base64.b64decode(resultado)
                                                        resultado=resultado.decode("utf-8")
                                                        clientSocket.close()
                                                        print()
                                                else:
                                                        print("\nOperação cancelada!\n")
                                        elif(op=="2"):
                                                clientSocket = socket(AF_INET, SOCK_STREAM)
                                                clientSocket.connect((serverName,serverPort))
                                                message="USU "+email
                                                message=message.encode("utf-8")
                                                message=base64.b64encode(message)
                                                clientSocket.send(message)
                                                usuario = clientSocket.recv(1024)
                                                clientSocket.close()
                                                usuario=base64.b64decode(usuario)
                                                usuario=usuario.decode("utf-8")
                                                message=("LIS "+usuario)
                                                message= message.encode("utf-8")
                                                message=base64.b64encode(message)
                                                clientSocket = socket(AF_INET, SOCK_STREAM)
                                                clientSocket.connect((serverName,serverPort))
                                                clientSocket.send(message)
                                                resultado = clientSocket.recv(1024)
                                                clientSocket.close()
                                                resultado=base64.b64decode(resultado)
                                                resultado=resultado.decode("utf-8")
                                                if(resultado==''):
                                                        print("\nNão há arquivos a serem baixados!\n")
                                                else:
                                                        print("\n"+resultado)
                                                        nomearquivo=input( '\n\nDigite o nome.extensão do arquivo que deseja baixar: ' )
                                                        if(nomearquivo not in resultado):
                                                                print("\nNome inválido!\n\n")
                                                        else:
                                                                clientSocket = socket(AF_INET, SOCK_STREAM)
                                                                clientSocket.connect((serverName,serverPort))
                                                                message="BAI".encode("utf-8")+usuario.encode("utf-8")+"/".encode("utf-8")+nomearquivo.encode("utf-8")
                                                                message=base64.b64encode(message)
                                                                clientSocket.send(message)
                                                                print("\nRecebendo arquivo...\n")
                                                                with open(nomearquivo,"wb") as arquivo:
                                                                        while True:
                                                                                dados=clientSocket.recv(1000000)
                                                                                if not dados:
                                                                                        break
                                                                                arquivo.write(dados)
                                                                arquivo.close()
                                                                clientSocket.close()
                                                                print("\nArquivo baixado com sucesso!\n")
                                        elif(op=="3"):
                                                clientSocket = socket(AF_INET, SOCK_STREAM)
                                                clientSocket.connect((serverName,serverPort))
                                                message="USU "+email
                                                message=message.encode("utf-8")
                                                message=base64.b64encode(message)
                                                clientSocket.send(message)
                                                usuario = clientSocket.recv(1024)
                                                clientSocket.close()
                                                usuario=base64.b64decode(usuario)
                                                usuario=usuario.decode("utf-8")
                                                message=("LIS "+usuario)
                                                message= message.encode("utf-8")
                                                message=base64.b64encode(message)
                                                clientSocket = socket(AF_INET, SOCK_STREAM)
                                                clientSocket.connect((serverName,serverPort))
                                                clientSocket.send(message)
                                                resultado = clientSocket.recv(1024)
                                                clientSocket.close()
                                                resultado=base64.b64decode(resultado)
                                                resultado=resultado.decode("utf-8")
                                                if(resultado==''):
                                                        print("\nNão há arquivos a serem deletados!\n")
                                                else:
                                                        print("\n"+resultado)
                                                        nomearquivo=input( '\n\nDigite o nome.extensão do arquivo que deseja deletar: ' )
                                                        if(nomearquivo not in resultado):
                                                                print("\nNome inválido!\n\n")
                                                        else:
                                                                message="DEL"+usuario+"/"+nomearquivo
                                                                message=message.encode("utf-8")
                                                                message=base64.b64encode(message)
                                                                clientSocket = socket(AF_INET, SOCK_STREAM)
                                                                clientSocket.connect((serverName,serverPort))
                                                                clientSocket.send(message)
                                                                resultado = clientSocket.recv(1024)
                                                                clientSocket.close()
                                                                resultado=base64.b64decode(resultado)
                                                                resultado=resultado.decode("utf-8")
                                                                print(resultado)
                                        elif(op=="4"):
                                                clientSocket = socket(AF_INET, SOCK_STREAM)
                                                clientSocket.connect((serverName,serverPort))
                                                message="USU "+email
                                                message=message.encode("utf-8")
                                                message=base64.b64encode(message)
                                                clientSocket.send(message)
                                                usuario = clientSocket.recv(1024)
                                                clientSocket.close()
                                                usuario=base64.b64decode(usuario)
                                                usuario=usuario.decode("utf-8")
                                                message=("LIS "+usuario)
                                                message= message.encode("utf-8")
                                                message=base64.b64encode(message)
                                                clientSocket = socket(AF_INET, SOCK_STREAM)
                                                clientSocket.connect((serverName,serverPort))
                                                clientSocket.send(message)
                                                resultado = clientSocket.recv(1024)
                                                clientSocket.close()
                                                resultado=base64.b64decode(resultado)
                                                resultado=resultado.decode("utf-8")
                                                if(resultado==''):
                                                        print('\nDiretório vazio!\n')
                                                else:
                                                        print("\n"+resultado)
                                        elif(op=="5"):
                                                message=("DUS "+email)
                                                message= message.encode("utf-8")
                                                message=base64.b64encode(message)
                                                clientSocket = socket(AF_INET, SOCK_STREAM)
                                                clientSocket.connect((serverName,serverPort))
                                                clientSocket.send(message)
                                                resultado = clientSocket.recv(1024)
                                                clientSocket.close()
                                                op=0
                                                print("\nLogin deletado com sucesso!\n")
                                        elif(op=="0"):
                                                print("\nSaindo da sua conta...\n\n")
                                                op="1"
                                                break
                                        else:
                                                print("\nOpção inválida!")
                else:
                        print("\nEmail teste e/ou senha inválidos!\n")        
        elif op=="0":
                print("Saindo do programa...")
        else:
                print("Opção inválida!\n\n")
