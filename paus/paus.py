import mysql.connector

#Public Administrative Unifield System.

class Paus:

    def __init__(self):

        CONFIGURACAO = {
            "host": "localhost",
            "user": "root",
            "password": "mo69om"
        }

        self.conexao = mysql.connector.connect(** CONFIGURACAO)
        self.cursor = self.conexao.cursor()

        self.cursor.execute('CREATE DATABASE IF NOT EXISTS paus')
        self.cursor.execute('USE paus')
        self.conexao.commit()

        sql_criar_tabela_alunos = """
            CREATE TABLE IF NOT EXISTS alunos (
                id integer auto_increment,
                nome varchar(50) not null,
                matricula varchar(50) unique,
                primary key(id)
            )
        """
        self.cursor.execute(sql_criar_tabela_alunos)

        sql_criar_tabela_disciplinas = """
            CREATE TABLE IF NOT EXISTS disciplinas (
                id int auto_increment,
                nome varchar(50) not null,
                prof varchar(50),
                primary key( id )
            )
        """
        self.cursor.execute(sql_criar_tabela_disciplinas)

        sql_criar_tabela_matriculas = """
            CREATE TABLE IF NOT EXISTS matriculas (
                id int auto_increment,
                idAluno int not null,
                idDisciplina int not null,
                foreign key (idAluno) references alunos(id),
                foreign key (idDisciplina) references disciplinas(id),
                primary key(id)
            )
        """
        self.cursor.execute(sql_criar_tabela_matriculas)
        self.conexao.commit()

    def __obterOMaiorNumeroDeMatricula(self):
        numero=0
        sql = "SELECT max(matricula) AS matricula FROM alunos"
        self.cursor.execute(sql)
        for ( matricula ) in self.cursor:
            if matricula[0] == None:
                return 0
            else:
                numero=matricula[0]
        return int(numero)

    def __verificarExistenciaDisciplina(self, padrao):
        sql = "SELECT nome FROM disciplinas WHERE nome = %s"
        self.cursor.execute(sql,(padrao,))
        for ( nome ) in self.cursor:
            if padrao == nome[0]:
                return True
            else:
                continue
        return False

    def cadastrarAluno(self, novo_nome):
        sql = """INSERT INTO alunos (nome, matricula) VALUES (%s, %s)"""
        novaMatricula = self.__obterOMaiorNumeroDeMatricula() + 1
        self.cursor.execute(sql, (novo_nome, novaMatricula ))
        self.conexao.commit()

    def cadastrarDisciplina(self, nova_disp_nome, prof):
        sql = """INSERT INTO disciplinas (nome, prof) VALUES (%s, %s)"""
        self.cursor.execute(sql,( nova_disp_nome, prof))
        self.conexao.commit()

    def cadastrarAlunoNaDisciplina(self, idaluno, iddisciplina):
        sql = """ INSERT INTO matriculas (idAluno,idDisciplina) VALUES (%s, %s)"""
        self.cursor.execute(sql,(idaluno, iddisciplina))
        self.conexao.commit()

    def listarAlunos(self):
        sql = """SELECT id, nome, matricula FROM alunos"""
        self.cursor.execute(sql)
        print( 'id, nomeDoAluno, matricula' )
        for ( id, nome, matricula) in self.cursor:
            print( f'{id} {nome} {matricula}' )

    def listarDisciplinas(self):
        sql = """SELECT id, nome, prof FROM disciplinas"""
        self.cursor.execute(sql)
        print('id, nomeDisiplina , professorResponsável')
        for ( id, nome, prof ) in self.cursor:
            print( f'{id} {nome} {prof}' )
    
    def listarAlunosMatriculadosNaDisciplina(self, disciplina):
        sql = """SELECT alunos.nome AS aluno, disciplinas.nome AS disciplina
            FROM alunos INNER JOIN matriculas ON alunos.id = matriculas.idAluno
            INNER JOIN disciplinas ON disciplinas.id = matriculas.idDisciplina
            WHERE disciplinas.nome = %s """
        self.cursor.execute(sql,(disciplina,))
        for ( aluno, disciplina ) in self.cursor:
            print(f'{aluno} {disciplina}')

    def listarDisciplinasAlunoMatriculado(self, aluno):
        sql = """SELECT alunos.nome AS aluno, disciplinas.nome AS disciplina FROM 
            disciplinas INNER JOIN matriculas ON disciplinas.id
            = matriculas.idDisciplina INNER JOIN alunos ON
            alunos.id = matriculas.idAluno WHERE alunos.nome = %s;"""
        print(f'aluno, disciplina')
        self.cursor.execute(sql,(aluno,))
        for ( aluno, disciplina ) in self.cursor:
            print( f'{aluno} {disciplina}' )

    def interfaceCli(self):
        while True:
            print( """----\n
                  1.listar alunos cadastrados.
                  2.listar diciplinas cadastradas.
                  3.cadastrar novo aluno.
                  4.cadastrar nova disciplina.
                  5.cadastar aluno em uma disciplina.
                  6.listar alunos matriculados em uma disciplina.
                  7.listar disciplinas em que o aluno esta matriculado.
                  0.sair
                  \n----""" )
            opcao = input( '\nPROMPT>' )
            match opcao:
                case '1':
                    self.listarAlunos()
                case '2':
                    self.listarDisciplinas()
                case '3':
                    nome=input('NomeDoNovoAluno>')
                    self.cadastrarAluno(nome)
                case '4':
                    nomed=input('NomaDaNovaDisciplina>')
                    if self.__verificarExistenciaDisciplina(nomed) == True:
                        print( f'{nomed} já existe. Tua ação foi cancelada.' )
                    else:
                        prof=input('NomeDoProfessorResponsável>')
                        self.cadastrarDisciplina(nomed,prof)
                case '5':
                    print('_______________')
                    self.listarAlunos()
                    print('_______________')
                    self.listarDisciplinas()
                    print('_______________')
                    id=input('IdDoAlunoAlvo>')
                    disciplina=input('IdDisciplinaAlvo>')
                    while True:
                        confirmar = input(f'O aluno de ID {id} será cadastrado na disciplina {disciplina}. Correto? (sim|não)')
                        if confirmar == "sim":
                            self.cadastrarAlunoNaDisciplina(id,disciplina)
                            break
                        elif confirmar == "não":
                            print('C A N C E L A D O')
                            break
                        else:
                            print("sim ou não?")
                            continue
                case '6':
                    dis = input('Disciplina>')
                    if( self.__verificarExistenciaDisciplina(dis) == False ):
                        print(f'{dis} não existe')
                    else:
                        self.listarAlunosMatriculadosNaDisciplina(dis)
                case '7':
                    alu = input('NomeAluno>')
                    self.listarDisciplinasAlunoMatriculado(alu)
                case '0':
                    break 
                case 'dev':
                    print( self.__obterOMaiorNumeroDeMatricula() )
                case 'linux':
                    print( """
                  .88888888:.
                88888888.88888.
              .8888888888888888.
              888888888888888888
              88' _`88'_  `88888
              88 88 88 88  88888
              88_88_::_88_:88888
              88:::,::,:::::8888
              88`:::::::::'`8888
             .88  `::::'    8:88.
            8888            `8:888.
          .8888'             `888888.
         .8888:..  .::.  ...:'8888888:.
        .8888.'     :'     `'::`88:88888
       .8888        '         `.888:8888.
      888:8         .           888:88888
    .888:88        .:           888:88888:
    8888888.       ::           88:888888
    `.::.888.      ::          .88888888
   .::::::.888.    ::         :::`8888'.:.
  ::::::::::.888   '         .::::::::::::
  ::::::::::::.8    '      .:8::::::::::::.
 .::::::::::::::.        .:888:::::::::::::
 :::::::::::::::88:.__..:88888:::::::::::'
  `'.:::::::::::88888888888.88:::::::::'
      `':::_:' -- '' -'-' `':_::::'`""" )
                case other:
                    print('NOP.')

