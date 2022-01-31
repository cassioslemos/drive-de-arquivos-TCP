from socket import *
import base64
import os
import shutil
import time
serverPort = 12000
serverSocket = socket(AF_INET,SOCK_STREAM)
serverSocket.bind(('25.78.211.38',serverPort))
serverSocket.listen(1)
print ("The server is ready to receive")
while 1:
        connectionSocket, addr = serverSocket.accept()


        aux_byte = connectionSocket.recv(1024)
        aux = base64.b64decode(aux_byte)
        comando=aux[0:3].decode("utf-8")
        #print(comando)
        if comando==('CRI'):
                message=aux.decode("utf-8")
                criar,email,user,senha=message.split(" ")
                arquivo=open('usuarios.txt', 'r')
                flag=0
                linha=arquivo.readline()
                while(linha != ''):
                        linha=linha.encode("utf-8")
                        linha = base64.b64decode(linha)
                        linha=linha.decode("utf-8")
                        auxemail,auxuser,auxsenha = linha.split(" ")
                        if(auxemail==email):
                                flag=1
                                break
                        if(auxuser==user):
                                flag=2
                                break
                        linha=arquivo.readline()
                arquivo.close()
                if(flag==1):
                        message="\nEmail já utilizado! Tente novamente\n"
                elif(flag==2):
                        message="\nNome de usuário já utilizado! Tente novamente\n"
                else:
                        arquivo=open('usuarios.txt', 'r')
                        conteudo=arquivo.readlines()
                        novalinha=(email+" "+user+" "+senha)
                        novalinha=novalinha.encode("utf-8")
                        novalinha = base64.b64encode(novalinha)
                        novalinha=novalinha.decode("utf-8")
                        novalinha=(novalinha+"\n")
                        conteudo.append(novalinha)
                        os.mkdir(user)
                        arquivo.close()
                        arquivo=open('usuarios.txt', 'w')
                        arquivo.writelines(conteudo)
                        arquivo.close()
                        message="\nLogin criado com sucesso!\n"
                connectionSocket.send(message.encode("utf-8"))
        elif comando==('LOG'):
                message=aux.decode("utf-8")
                login,email,senha=message.split(" ")
                arquivo=open('usuarios.txt', 'r')
                flag=0
                linha=arquivo.readline()
                while(linha != ''):
                        linha=linha.encode("utf-8")
                        linha = base64.b64decode(linha)
                        linha=linha.decode("utf-8")
                        auxemail,auxuser,auxsenha = linha.split(" ")
                        if(auxemail==email and auxsenha==senha):
                                flag=1
                                break
                        linha=arquivo.readline()
                arquivo.close()
                if (flag==1):
                        message=("\nLogin efetuado com sucesso! Bem-vindo, "+auxuser+"!\n")
                else:
                        message="\nEmail e/ou senha inválidos!\n"
                connectionSocket.send(message.encode("utf-8"))
        elif comando==('USU'):
                message=aux.decode("utf-8")
                login, email=message.split(" ")
                arquivo=open('usuarios.txt', 'r')
                linha=arquivo.readline()
                while(linha != ''):
                        linha=linha.encode("utf-8")
                        linha = base64.b64decode(linha)
                        linha=linha.decode("utf-8")
                        auxemail,auxuser,auxsenha = linha.split(" ")
                        if(auxemail==email):
                                break
                        linha=arquivo.readline()
                arquivo.close()
                message=auxuser
                message=message.encode("utf-8")
                message=base64.b64encode(message)
                message=message.decode("utf-8")
                connectionSocket.send(message.encode("utf-8"))
        elif comando==('LIS'):
                message=aux.decode("utf-8")
                listar, usuario=message.split(" ")
                message=os.listdir("./"+usuario)
                message=str(message).encode("utf-8")
                message=base64.b64encode(message)
                message=message.decode("utf-8")
                connectionSocket.send(message.encode("utf-8"))
        elif comando==('DUS'):
                message=aux.decode("utf-8")
                deletar, email=message.split(" ")
                arquivo=open('usuarios.txt', 'r')
                linha=arquivo.readline()
                novoconteudo=''
                while(linha != ''):
                        linha=linha.encode("utf-8")
                        linha = base64.b64decode(linha)
                        linha=linha.decode("utf-8")
                        auxemail,auxuser,auxsenha = linha.split(" ")
                        if(auxemail!=email):
                                linha=linha.encode("utf-8")
                                linha = base64.b64encode(linha)
                                linha=linha.decode("utf-8")
                                novoconteudo=novoconteudo+linha+"\n"
                        else:
                                shutil.rmtree(auxuser)
                        linha=arquivo.readline()
                arquivo.close()
                arquivo=open('usuarios.txt', 'w')
                arquivo.writelines(novoconteudo)
                arquivo.close()
                message="\nLogin deletado com sucesso!\n"
                connectionSocket.send(message.encode("utf-8"))
        elif comando==('ENV'):
                filename=aux[3:].decode("utf-8")
                #i=0
                with open(filename, 'wb') as arquivo:
                        while True:
                                aux=connectionSocket.recv(1000000)
                                if not aux:
                                        break
                                #print(i)
                                #i=i+1
                                arquivo.write(aux)
                arquivo.close()
                message="\nArquivo recebido com sucesso!\n"
                message=message.encode("utf-8")
                message = base64.b64encode(message)
                connectionSocket.send(message)
        elif comando==('BAI'):
                filename=aux[3:].decode("utf-8")
                with open(filename,"rb") as arquivo:
                        for dados in arquivo.readlines():
                                connectionSocket.sendall(dados)
                                time.sleep(0.001)
                arquivo.close()
                connectionSocket.shutdown(SHUT_WR)
        elif comando==('DEL'):
                filename=aux[3:].decode("utf-8")
                os.remove(filename)
                message="\nArquivo deletado com sucesso!\n"
                message=message.encode("utf-8")
                message = base64.b64encode(message)
                connectionSocket.send(message)
        else:
               message="\nNão foi possível executar essa ação\n"
               connectionSocket.send(message.encode("utf-8"))
        connectionSocket.close()
