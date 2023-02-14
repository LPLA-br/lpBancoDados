DROP DATABASE IF EXISTS Notflux;
CREATE DATABASE IF NOT EXISTS Notflux;
USE Notflux;

CREATE TABLE IF NOT EXISTS plano
(
	id INT,
	nome VARCHAR(50) NOT NULL,
	valor INT NOT NULL,
	duracaoDiasUnix VARCHAR(12) NOT NULL,
	PRIMARY KEY(id)
);

/*UNIX_TIMESTAMP()*/
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

INSERT INTO usuarios(id,login,senha) VALUES
(0,"root","rinoceteio");

INSERT INTO usuarios(login,senha) VALUES
("Demostrencio","pitu51"),
("Jeremias","20lascar"),
("luiz","123");

CREATE TABLE IF NOT EXISTS videos
(
	id INT AUTO_INCREMENT,
	titulo VARCHAR(50) NOT NULL,
	ano VARCHAR(4),
	categoria VARCHAR(50),
	PRIMARY KEY(id)
);

INSERT INTO videos(titulo,ano,categoria) VALUES
("Bem Vindo a Notflux", YEAR(NOW()),"apresentação"),
("Serra do Boró", "2019", "comédia,ação"),
("Nao Resisti a sogra", "2003", "comédia,romance"),
("As desaventuras de um pistoleiro na cachaça", "1969", "tiroteio,ação"),
("Luta na cachaçaria", "1972","ação"),
("Visitei a prima", "1969","comédia,romance");

/*anulado: cardinalidade
CREATE TABLE IF NOT EXISTS categorias
(
    id INT AUTO_INCREMENT,
    nome VARCHAR(30) NOT NULL,
    idVideo INT,
    idCateg INT,
    PRIMARY KEY(id)
);


INSERT INTO categorias(nome) VALUES
("terror"),
("susto"),
("documentario"),
("educacional"),
("ação"),
("tiroteiro");
*/

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

/*anulado: cardinalidade
CREATE TABLE IF NOT EXISTS assinatura
(
	idUsuario INT NOT NULL,
	idPlano INT NOT NULL,
	inicioContrato VARCHAR(50) NOT NULL,
	FOREIGN KEY (idUsuario) REFERENCES usuarios(id),
	FOREIGN KEY (idPlano) REFERENCES plano(id)
);*/


/*anulado: cardinalidade
CREATE TABLE IF NOT EXISTS videopossuicategs
(
    id INT AUTO_INCREMENT,
    idVideo INT NOT NULL,
    idCateg INT NOT NULL,
    PRIMARY KEY( id ),
    FOREIGN KEY(idVideo) REFERENCES videos(id),
    FOREIGN KEY(idCateg) REFERENCES categorias(id)
);
*/

