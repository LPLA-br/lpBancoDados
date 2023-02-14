/*Versão alternativa em SQL puro*/

DROP DATABASE IF EXISTS NotfluxALT;
CREATE DATABASE IF NOT EXISTS NotfluxALT;
USE NotfluxALT;

CREATE TABLE IF NOT EXISTS plano
(
	id INT,
	nome VARCHAR(50) NOT NULL,
	valor INT NOT NULL,
	duracaoDiasUnix VARCHAR(12) NOT NULL,
	PRIMARY KEY(id)
);

INSERT INTO plano(id,nome,valor,duracaoDiasUnix) VALUES
(1,"basico",100,"864000"),
(2,"master",200,"1728000"),
(3,"premium",300,"2592000");

CREATE TABLE IF NOT EXISTS usuarios
(
	id INT AUTO_INCREMENT,
	login VARCHAR(50) NOT NULL,
	senha VARCHAR(50) NOT NULL,
    plano INT,
    dataInicio VARCHAR(20),
	PRIMARY KEY(id),
	UNIQUE( login ),
	UNIQUE( senha ),
    FOREIGN KEY(plano) REFERENCES plano(id)
);

/*
Demostrencio(plano1),Fulazio(plano3) -> estão com planos válidos.
Menocrito(plano1),Democrito(plano3) -> planos inválidos.
 */
INSERT INTO usuarios(login,senha) VALUES
("Demostrencio","silex34"),
("Democrito","Ginoliza78"),
("Fulazio","ui89"),
("Menocrito","septNoct"),
("Secondio","74dg"),
("Selonio","3hd8k"),
("Tercio","jfjhs"),
("Terculus","jjf63");

CREATE TABLE IF NOT EXISTS videos
(
	id INT AUTO_INCREMENT,
	titulo VARCHAR(50) NOT NULL,
	ano INT,
	categoria VARCHAR(50),
	PRIMARY KEY(id)
);

INSERT INTO videos(titulo,ano,categoria) VALUES
("Bem Vindo a Notflux", 2023,"APRESENTAÇÃO"),
("Serra do Boró", 2019, "COMÉDIA,AÇÃO"),
("Nao Resisti a sogra", 2003, "COMÉDIA,ROMANCE"),
("As desaventuras de um pistoleiro na cachaça", 1969, "TIROTEIO,AÇÃO"),
("Luta na cachaçaria", 1972,"AÇÃO"),
("Visitei a prima", 1969,"COMÉDIA,ROMANCE");

/*#########################SETOR DOS RELACIONAMENTOS#########################*/

CREATE TABLE IF NOT EXISTS assistiu
(
	id INT AUTO_INCREMENT,
	data VARCHAR(20),
	idUsuario INT NOT NULL,
	idVideo INT NOT NULL,
	FOREIGN KEY (idUsuario) REFERENCES usuarios(id),
	FOREIGN KEY (idVideo) REFERENCES videos( id ),
	PRIMARY KEY(id)
);

/*#########################SETOR DAS QUESTÕES#########################*/
/*---Comandos puros e isolados----*/

/*cadastro de assinatura*/


UPDATE usuarios SET plano = 1, dataInicio = UNIX_TIMESTAMP() WHERE id = 1;

/*21 dias atrás. atrasado*/
UPDATE usuarios SET plano = 1, dataInicio = (UNIX_TIMESTAMP() - 1814419) WHERE id = 2;

/*31 dias atrás. atrasado*/
UPDATE usuarios SET plano = 1, dataInicio = (UNIX_TIMESTAMP() - 2678405) WHERE id = 3;

/*181 segundos atrás. joia*/
UPDATE usuarios SET plano = 1, dataInicio = (UNIX_TIMESTAMP() - 181) WHERE id = 4;

/*21 dias atrás. atrasado*/
UPDATE usuarios SET plano = 2, dataInicio = (UNIX_TIMESTAMP() - 1814419) WHERE id = 5;

UPDATE usuarios SET plano = 2, dataInicio = UNIX_TIMESTAMP() WHERE id = 6;

/*40 dias atrás. atrasado*/
UPDATE usuarios SET plano = 3, dataInicio = (UNIX_TIMESTAMP() - 3455953) WHERE id = 7;

UPDATE usuarios SET plano = 3, dataInicio = UNIX_TIMESTAMP() WHERE id = 8;


/*remoção de assinatura*/
UPDATE usuarios SET plano = NULL, dataInicio = NULL WHERE id = 1;

/*atualização de assinatura*/
UPDATE usuarios SET plano = 1, dataInicio = UNIX_TIMESTAMP() WHERE id = 1;

/*cadastrar o usuario*/
INSERT INTO usuarios(login,senha) VALUES ("Girolamo","6969tx");

/*remover o usuario*/
DELETE FROM usuarios WHERE login = "Girolamo";

/*atualizar o usuario*/
UPDATE usuarios SET login = "Zelatomeris", senha = "mynameisnobody" WHERE id = 3;

/*cadastar o video*/
INSERT INTO videos(titulo,ano,categoria) VALUES ("O programador que enlouqueceu","1998","AÇÃO,SUSPENCE");

/*remover o video*/
DELETE FROM videos WHERE id = 2; /*serra do boró*/

/*atualizar o video*/
UPDATE videos
SET titulo = "Sogra irresistível", ano = "2004", categoria = "ROMANCE" WHERE id = 3;

/*
 Devido à cardinalidade a questão 4 fora omitida.
 Se cada vídeo só pode possuir uma categoria então
 a tabela que o descreve pode absorver a tabela
 que armazenaria as categorias como uma coluna.
*/

/*a renovação de assinatura do usuario*/
UPDATE usuarios SET dataInicio = UNIX_TIMESTAMP() WHERE id = 1;
/* unix_timestamp atual menos o inicial = tempo_desde_assinatura_em_segundos
   se tempo_desde_assinatura_em_segundos for maior que plano.duracaoDiasUnix
   então tu estás com a assinatura atrasada. Em outras palavras, podes renovar
   tua assinatura.
*/

/*o usuario assiste ao vídeo. ação esta que é salva no banco de dados.*/
INSERT INTO assistiu(data,idUsuario,idVideo) VALUES (now(),3,4);
INSERT INTO assistiu(data,idUsuario,idVideo) VALUES (now(),2,4);
INSERT INTO assistiu(data,idUsuario,idVideo) VALUES (now(),4,4);
INSERT INTO assistiu(data,idUsuario,idVideo) VALUES (now(),1,4);
INSERT INTO assistiu(data,idUsuario,idVideo) VALUES (now(),3,3);
INSERT INTO assistiu(data,idUsuario,idVideo) VALUES (now(),3,5);


/*o usuario faz uma busca do vídeo pelo nome*/
SELECT titulo FROM videos WHERE titulo = 'As desaventuras de um pistoleiro na cachaça';
/*o usuario não sabe o nome completo do filme*/
SELECT titulo FROM videos WHERE titulo LIKE "%desaventuras%";

/*o usuario procura filmes pelo ano de estreia*/
SELECT titulo,ano FROM videos WHERE ano = 1969;
/*o usuario só gosta de filme novo*/
SELECT titulo,ano FROM videos WHERE ano > 2000;

/*o usuario adora filme de ação*/
SELECT titulo,categoria FROM videos WHERE categoria LIKE "%AÇÃO%";

/*Categoria de vídeo mais assistida pelo usuário em ordem decrescente*/
SELECT count(videos.categoria) AS popularidade, videos.categoria FROM usuarios
INNER JOIN assistiu ON usuarios.id = assistiu.idUsuario
INNER JOIN videos ON videos.id = assistiu.idVideo GROUP BY categoria DESC;

/*O vídeo mais assitido desta plataforma*/
SELECT COUNT(videos.titulo) as visualizacoes, videos.titulo
FROM assistiu INNER JOIN videos ON assistiu.idVideo = videos.id
GROUP BY titulo ORDER BY visualizacoes DESC LIMIT 1;

/*os logins dos usuários com a assinatura atrasada*/
/* O número de segundos entre a timestamp da contratação e
   o timestamp do agora não pode ser maior que os limites
   estipulados para cada plano em "plano".*/
SELECT login FROM usuarios WHERE plano = 1 AND (UNIX_TIMESTAMP() - dataInicio) >
( select duracaoDiasUnix from plano where id = 1 ) UNION
SELECT login FROM usuarios WHERE plano = 2 AND (UNIX_TIMESTAMP() - dataInicio) >
( select duracaoDiasUnix from plano where id = 2 ) UNION
SELECT login FROM usuarios WHERE plano = 3 AND (UNIX_TIMESTAMP() - dataInicio) >
( select duracaoDiasUnix from plano where id = 3 );

/*o número de usuários ativos para cada plano */
SELECT count(login) AS ativos FROM usuarios
WHERE plano = 1 AND (UNIX_TIMESTAMP() - dataInicio) < ( SELECT duracaoDiasUnix from plano where id = 1 )
UNION ALL
SELECT count(login) AS ativos FROM usuarios WHERE plano = 2 AND (UNIX_TIMESTAMP() - dataInicio) < ( SELECT duracaoDiasUnix from plano where id = 2 )
UNION ALL
SELECT count(login) AS ativos FROM usuarios WHERE plano = 3 AND (UNIX_TIMESTAMP() - dataInicio) < ( SELECT duracaoDiasUnix from plano where id = 3 );

/*faturamento. Somatório do valor da assinatura de todos os usuários levando em conta o mês corrente*/
/*quebrei a cara! o unix_timestamp() não é adequado para verificação de tempo de alto nível
 como o "O mês atual, do primeiro dia até agora".*/
 /*Resposta parcial. Somatório das do valor das contas ativas*/
SELECT sum(valor) FROM plano
LEFT JOIN (
    SELECT id, login, plano FROM usuarios WHERE plano = 1 and (UNIX_TIMESTAMP() - dataInicio) < ( SELECT duracaoDiasUnix from plano where id = 1 )
    UNION ALL
        SELECT id, login, plano FROM usuarios WHERE plano = 2 and (UNIX_TIMESTAMP() - dataInicio) < ( SELECT duracaoDiasUnix from plano where id = 2 )
    UNION ALL
        SELECT id, login, plano FROM usuarios WHERE plano = 3 and (UNIX_TIMESTAMP() - dataInicio) < ( SELECT duracaoDiasUnix from plano where id = 3 )
) ativos ON ativos.plano = plano.id;

