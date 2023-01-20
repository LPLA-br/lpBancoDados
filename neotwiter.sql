--execute apenas se não houver a tabela.
CREATE DATABASE IF NOT EXISTS NEOTWITER;
USE NEOTWITER;

CREATE TABLE IF NOT EXISTS Usuarios(
	id INT AUTO_INCREMENT,
	login VARCHAR(20) NOT NULL UNIQUE,
	senha VARCHAR(20) NOT NULL,
	PRIMARY KEY(id),
	UNIQUE(login)
);

CREATE TABLE IF NOT EXISTS Mensagens(
	id INT AUTO_INCREMENT,
	texto VARCHAR(1000) NOT NULL,
	data_post VARCHAR(50) NOT NULL,
	id_usuario INT NOT NULL,
	PRIMARY KEY (id),
	FOREIGN KEY (id_usuario) REFERENCES Usuarios(id)
);

INSERT INTO Usuarios(login, senha)
VALUES ("bucefalus", "gelin"),("morlin","neck3");

INSERT INTO Mensagens(texto, data_post, id_usuario)
VALUES ("Devo explodir o ifrn.",now(), 1);

-- Operações de UPDATE e DELETE
-- podem são afetadas por: PK ←→ PF
