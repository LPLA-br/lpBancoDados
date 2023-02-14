import mysql.connector
from time import sleep
from data import UnixTimestampNotflux


class Sessao:

    def __init__(self):

        CONFIGURACAO = {
            "host": "localhost",
            "user": "root",
            "password": "mo69om"
        }

        self.conexao = mysql.connector.connect(** CONFIGURACAO)
        self.cursor = self.conexao.cursor()

        self.cursor.execute('CREATE DATABASE IF NOT EXISTS Notflux')
        self.cursor.execute('USE Notflux')
        self.conexao.commit()

    def encerrarConex(self):
        self.conexao.close()


class Notflux( Sessao ):

    def __init__(self):
        super().__init__()
        self.login=""
        self.senha=""
        self.idSessao=""
        self.planoCorrente = ""
        self.dataInicio = 0
        
        self.tempo = UnixTimestampNotflux()

    def __verificarExistenciaSenha(self, Senha):
        sql="""SELECT senha FROM usuarios WHERE senha = %s"""
        self.cursor.execute(sql,(Senha,))
        for (senha) in self.cursor:
            if Senha == senha[0]:
                return True
            else:
                continue
        return False

    def __verificarExistenciaLogin(self, Login):
        sql="""SELECT login FROM usuarios WHERE login = %s"""
        self.cursor.execute(sql,(Login,))
        for (login) in self.cursor:
            if Login == login[0]:
                return True
            else:
                continue
        return False

    def __salvarIdDoUsuarioEmSessaoIniciada(self):
        sql="""SELECT id FROM usuarios WHERE senha = %s"""
        self.cursor.execute(sql,(self.senha,))
        for (id) in self.cursor:
            if id != None:
                if True:
                    #debug
                    print( id[0] )
                self.idSessao = id[0]
            else:
                self.idSessao = None

    def __obterPlanoEDataInicialDoUsuarioCorrente(self):
        sql = """SELECT plano,dataInicio FROM usuarios WHERE senha = %s"""
        self.cursor.execute(sql,(self.senha,))
        for (plano, dataInicio) in self.cursor:
            if type(plano) != type(None) and type(dataInicio) != type(None):
                self.planoCorrente = int(plano)
                self.dataInicio = int(dataInicio)
            else:
                print(f'{self.login} não contratou plano válido')
                self.planoCorrente = None
                self.dataInicio = None
            break

    def ajuda(self,root):
        if root == False:
            aj="""
            ajuda
            cadastrarAssinatura
            atualizarAssinatura
            removerAssinatura
            atualizarSenhaLogin
            deletarMinhaConta
            procurarFilme
            assistirFilme
            sair
            """
            print(aj)
        elif root == True:
            aj="""
            Sair
            """
            print(aj)

    def __sessaoRoot(self):
        print("ROOT-MODE digite 'ajuda' para ajuda.")
        while True:
            commando = input('root#')
            match commando:
                case 'ajuda':
                    self.ajuda(False)
                case 'atualizarAssinatura':
                    self.atualizarAssinatura()
                case 'atualizarSenhaLogin':
                    pass
                case 'sair':
                    print(f'Chau {self.login}')
                    if self.encerrarSessao():
                        break
                case other:
                    print('NOP')



    def sessao(self, modo):
        print('"ajuda" para ajuda')
        match modo:
            case 'comun':
                while True:
                    comando=input(f"{self.login}>")
                    match comando:
                        case 'ajuda':
                            self.ajuda(False)
                        case 'cadastrarAssinatura':
                            self.cadastarAssinatura()
                        case 'atualizarAssinatura':
                            self.atualizarAssinatura()
                        case 'removerAssinatura':
                            self.removerAssinatura()
                        case 'atualizarSenhaLogin':
                            self.atualizarUsuario()
                        case 'deletarMinhaConta':
                            if self.removerUsuario():
                                self.encerrarSessao()
                                break
                        case 'procurarFilme':
                            selecao = input('por qual critério(1 2 ou 3)?\n1- nome\n2- ano\n3-categoria\n6-tudo\n>')
                            match selecao:
                                case '1':
                                    busca = input("Nome ou parte do nome>")
                                    self.buscarVideoPeloNome( busca )
                                case '2':
                                    busca = input("Ano>")
                                    self.buscarVideoPeloAno( busca )
                                case '3':
                                    busca = input("Categoria ou parte da categoria>")
                                    self.buscarVideoPelaCategoria( busca )
                                case '6':
                                    self.mostrarTodosVideos()
                                case other:
                                    print('Opção inválida. Voltando para o menu')

                        case 'assitirFilme':
                            identificador = 0
                            while True:
                                try:
                                    identificador = int( input('idDoVideo>') )
                                    break
                                except ValueError:
                                    print('erro: entrada inválida. re-insira o id de um vídeo pesquisado anteriormente.')
                                    continue
                            self.assistirAoVideo(identificador)
                        case 'sair':
                            print(f'Chau {self.login}')
                            if self.encerrarSessao():
                                break
                        case 'teste':
                            print(self.planoCorrente, self.dataInicio)
                            if self.__verificarValidadeDoPlano():
                                print('no prazo')
                            else:
                                print('não está no prazo')
                        case other:
                            print('NOP')
            case 'root':
                self.__sessaoRoot()
            case other:
                print('Erro Critico: sessao() sem modo válido')
                self.encerrarSessao()
                exit()

    def iniciarSessao(self):
        criarOuLogar=input('1-Criar Conta\n2-Logar\n\n>')
        if criarOuLogar == '1':
            self.cadastarUsuario()
        elif criarOuLogar == '2':
            self.login=input('login>')
            self.senha=input('senha>')
            if( self.__verificarExistenciaLogin(self.login) and self.__verificarExistenciaSenha(self.senha) ):
                print(f'Olá {self.login}')
                self.__salvarIdDoUsuarioEmSessaoIniciada()
                self.__obterPlanoEDataInicialDoUsuarioCorrente()
                match self.login:
                    case 'root':
                        self.sessao('root')
                    case other:
                        self.sessao('comun')
            else:
                print('Erro: Erraste login ou senha. Tente novamente.')
        else:
            print('NOP')


    #Zona da assinatura. Usuário comum controla

    def cadastarAssinatura(self):
        plano=1
        print("Selecione um plano abaixo\n1-básico(10dias)\n2-master(20dias)\n3-premium(30dias)")
        while True:
            try:
                plano=int(input('número do plano>'))
            except ValueError:
                print('valor inválido.')
                continue
            if plano >=1 or plano <= 3:
                sql=f"UPDATE usuarios SET plano = %s, dataInicio=UNIX_TIMESTAMP() WHERE login = %s"
                self.cursor.execute(sql,(plano,self.login))
                self.conexao.commit()
                match plano:
                    case 1:
                        print(f'{plano} foi contratado. Gastaste 100 reais')
                    case 2:
                        print(f'{plano} foi contratado. Gastaste 200 reais')
                    case 3:
                        print(f'{plano} foi contratado. Gastaste 300 reais')
                break
            else:
                print('Opção inválida. R E P E T E')
                continue


    #O usuário deleta sua assinatura.
    def removerAssinatura(self):
        tentativas=0
        while True:
            senha=input("confirmarSenha>")
            if senha == self.senha:
                break
            else:
                print("senha errada.")
                tentativas+=1
                if tentativas == 3:
                    return False
        sql = """UPDATE usuarios SET plano=NULL, dataInicio=NULL WHERE senha = %s"""
        self.cursor.execute(sql,(self.senha))
        self.conexao.commit()
        print('Removeste sua assinatura corrente.')
        return True

    #atualização de assinatura por parte do usuario
    def atualizarAssinatura(self):
        sql = """UPDATE usuarios SET plano=%s, dataInicio=UNIX_TIMESTAMP() WHERE senha = %s"""
        
        plano = input('plano 1 2 ou 3>')

        try:
            int(plano)
        except:
            print('valor inválido. Cancelado')
            return False

        if int(plano) >= 1 or int(plano) <= 3:
            self.cursor.execute(sql,(plano,self.senha))
            self.conexao.commit()
            match plano:
                case 1:
                    print(f'{plano} foi contratado. Gastaste 100 reais')
                case 2:
                    print(f'{plano} foi contratado. Gastaste 200 reais')
                case 3:
                    print(f'{plano} foi contratado. Gastaste 300 reais')


    def __cadastroUsuario(self,login,senha):
        sql = """INSERT INTO usuarios(login,senha) VALUES (%s,%s)"""
        self.cursor.execute(sql,(login,senha))
        self.conexao.commit()
        print('cadastrado. REBOOT')
        self.encerrarSessao()
        exit()


    def cadastarUsuario(self):
        while True:
            login = input('loginNovoUsuario>')
            senha = input('senhaNovoUsuario>')
            if self.__verificarExistenciaLogin(login) == False and self.__verificarExistenciaSenha(senha) == False:
                print(f'Bem vindo ao Notflux, {self.login}')
                sleep(1)
                self.__cadastroUsuario(login,senha)
                opt=("cadastre uma assinatura paga?(sim|não)")
                match opt:
                    case 'sim':
                        self.cadastarAssinatura()
                    case 'não':
                        print('cancelado')
                        return
                    case other:
                        print('cancelado')
                        return
            else:
                print('Erro! R E P E T E')
                continue


    #usuario logado deleta sua conta (mata a sessão).
    # True ou False Fazem parte de um sinal emitido para fora.
    def removerUsuario(self):
        senha = input('senha>')
        if self.__verificarExistenciaSenha(senha) == False:
            print('Ação negada: senha errada')
        else:
            while True:
                alerta=input('QUERES DELETAR SUA CONTA MESMO (sim|não)?')
                if alerta == "sim":
                    sql = """DELETE FROM usuarios WHERE login = %s"""
                    self.cursor.execute(sql, (self.login,) )
                    self.conexao.commit()
                    print('Conta deletada. Adeus')
                    return True
                elif alerta == 'não' or alerta == "nao":
                    print('cancelado')
                    return False
                else:
                    print(f'opção "{alerta}" inválida. R E P E T E')
                    continue


    #usuario logado (alteração de nome e senha)
    def atualizarUsuario(self):
        login = input('Novologin>')
        senha = input('NovaSenha>')
        while True:
            if login == self.login:
                if self.__verificarExistenciaSenha(senha):
                    sql = """UPDATE TABLE usuarios WHERE login = %s SET senha = %s"""
                    self.cursor.execute(sql, (self.login, login, senha) )
                    self.conexao.commit()
                    return True
                else:
                    #Sistema bom é aquele que indica que sua senha é igual a de outro usuário kkk
                    print('Erro. Escolha outra senha')
                    continue
            else:
                if self.__verificarExistenciaLogin(login) and self.__verificarExistenciaSenha(senha):
                    print('Novo login ou senha negados. Tente novamente.')
                    continue
                else:
                    sql = """UPDATE TABLE usuarios WHERE login = %s AND senha = %s SET login = %s, senha= %s"""
                    self.cursor.execute(sql, (self.login, self.senha, login, senha) )
                    self.conexao.commit()
                    return True

    def encerrarSessao(self):
        self.encerrarConex()
        return True

    #Zona de ação do usuário
    #verificações de validade do plano

    def buscarVideoPeloNome(self, Nome):
        sql = f"""SELECT id,titulo,ano,categoria FROM videos WHERE titulo LIKE '%{Nome}%'"""
        self.cursor.execute(sql)
        print( f"Resultados para {Nome}\n" )
        for (id,titulo,ano,categoria) in self.cursor:
            print(f'{id} -> {titulo} {ano} {categoria}')

    def buscarVideoPeloAno(self, Ano):
        sql = f"""SELECT id,titulo,ano,categoria FROM videos WHERE ano = %s"""
        self.cursor.execute(sql,(Ano,))
        print( f"Resultados para {Ano}\n" )
        for (id,titulo,ano,categoria) in self.cursor:
            print(f'{id} -> {titulo} {ano} {categoria}')

    def buscarVideoPelaCategoria(self, Categoria):
        sql = f"""SELECT id,titulo,ano,categoria FROM videos WHERE categoria LIKE '%{Categoria}%'"""
        self.cursor.execute(sql)
        print( f"Resultados para {Categoria}\n" )
        for (id,titulo,ano,categoria) in self.cursor:
            print(f'{id} -> {titulo} {ano} {categoria}')

    def mostrarTodosVideos(self):
        sql = "SELECT id,titulo,ano,categoria FROM videos"
        self.cursor.execute(sql)
        for (id,titulo,ano,categoria) in self.cursor:
            print(f'{id} {titulo} {ano} {categoria}')

    def __videoExiste(self,Id):
        sql = "SELECT id FROM videos"
        self.cursor.execute(sql)
        for (id) in self.cursor:
            if id == Id:
                return True
            else:
                continue
        return False

    #True ou false
    def __planoExiste(self):
        if self.planoCorrente == None:
            return False
        else:
            return True

    # string | boolean
    def __verificarValidadeDoPlano(self):
        self.__obterPlanoEDataInicialDoUsuarioCorrente()
        print( self.dataInicio, self.planoCorrente )

        sql = "SELECT duracaoDiasUnix FROM plano WHERE id = %s"

        if self.__planoExiste():
            match self.planoCorrente:
                case 1:
                    if self.tempo.estaValido(self.dataInicio, 1):
                        return True
                    else:
                        return False
                case 2:
                    if self.tempo.estaValido(self.dataInicio, 2):
                        return True
                    else:
                        return False
                case 3:
                    if self.tempo.estaValido(self.dataInicio, 3):
                        return True
                    else:
                        return False
                case other:
                    return False
        else:
            return False





    def assistirAoVideo(self, IdVideo):
        if not self.__videoExiste(IdVideo):
            print(f'video de id {IdVideo} não existe nesta plataforma.\nvoltando ao menu')
        else:
            #verificar validade do plano aqui
            sql = """INSERT INTO assistiu(data,idUsuario,idVideo) VALUES (NOW(),%s,%s)"""
            self.cursor.execute(sql,( self.idSessao, str(IdVideo) ) )
            self.conexao.commit()
            print('\n###assitiste ao filme ####\n')

    #-----------Zona do Vídeo para o root ROOT--------------.

    def __mostrarListaDeCategoriasPreExistentes(self):
        sql = "SELECT categoria FROM videos"
        self.cursor.execute(sql)
        print('-------Categorias pré definidas--------')
        for (categoria) in self.cursor:
            print(categoria)
        print('-------Categorias pré definidas--------')

    def cadastarVideo(self, Titulo, Categoria):
        sql="""INSERT INTO videos(titulo,ano,categoria) VALUES (%s,DATE(NOW()),%s)"""
        self.cursor.execute(sql,(Titulo,Categoria))
        self.conexao.commit()
        print(f'ROOT LOG - Video "{Titulo}" foi inserido na plataforma.')

    def removerVideo(self, Id):
        sql="""DELETE FROM videos WHERE id = %i"""
        self.cursor.execute(sql,(Id,))
        self.conexao.commit()
        print(f'ROOT LOG - Video "{Id}" foi deletado da plataforma.')

    def atualizarVideo(self, idVideo):
        sql = """UPDATE TABLE videos SET titulo = %s, ano = %s, categoria = %s WHERE id=%s"""
        if not self.__videoExiste( idVideo ):
            print(f'Vídeo {idVideo} não existe.')
        else:
            self.cursor.execute('SELECT titulo,ano,categoria FROM videos WHERE id = %s',(idVideo,))
            for (titulo,ano,categoria) in self.cursor:
                print('editando: {titulo} {ano} {categoria}')

            t = input('novoTitulo>')
            a = input('novoAno>') 
            c = input('novaCategoria>')

            self.cursor.execute(sql,(t,a,c,idVideo))
            self.conexao.commit()
            print('modificado.')

    def calculoDeTimestampTESTE(self):
        #timestamp atual menos o antigo (365dias atrás)
        sql = "SELECT UNIX_TIMESTAMP() - 1643719171"
        self.cursor.execute(sql)


    #cadastrar Remover Atualizar Categoria?
