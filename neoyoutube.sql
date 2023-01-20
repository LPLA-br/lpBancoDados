DROP DATABASE IF EXISTS NEOYOUTUBE;
CREATE DATABASE IF NOT EXISTS NEOYOUTUBE;

USE NEOYOUTUBE;

CREATE TABLE IF NOT EXISTS Usuarios
(
	id INT AUTO_INCREMENT,
	login VARCHAR(20) NOT NULL UNIQUE,
	senha VARCHAR(20) NOT NULL,
	PRIMARY KEY(id),
	UNIQUE(login)
);

CREATE TABLE IF NOT EXISTS Videos
(
	id INT AUTO_INCREMENT,
	titulo VARCHAR(50) NOT NULL,
	descr TEXT NOT NULL,
	id_usuario INT NOT NULL,
	PRIMARY KEY (id),
	FOREIGN KEY (id_usuario) REFERENCES Usuarios(id)
);

CREATE TABLE IF NOT EXISTS Gostinhas
(
	id_usuario INT,
	id_video INT,
	Gostou BOOLEAN NOT NULL,
	PRIMARY KEY(id_usuario, id_video),
	FOREIGN KEY (id_usuario) REFERENCES Usuarios(id),
	FOREIGN KEY (id_video) REFERENCES Videos(id)
);

INSERT INTO Usuarios(login, senha)
VALUES ("Genivaldo", "7fHsG43"),("Mercolino","jj5JjbCg3K"),("Anne Freeman","dHdJk4u777");

INSERT INTO Videos(titulo, descr, id_usuario)
VALUES ("Review cachaca rapariga","Cachaca boa",1),
("Review marlboro red","O clássico",1),
("Como amolar foice","Confira como amolar foice de verdade",2),
("Limpando espingarda","Confira as habilidades do mestre Mercolino",2),
("Teste A-24","Testando o reator elétrico de baixa ocilação AT6345.",3),
("SDMBP TESTE 04","Teste do sistema de distorção magnética de baixa proximidade modelo mark04.",3);


INSERT INTO Gostinhas(id_usuario, id_video, Gostou)
VALUES (1,1,true),
(1,2,true),
(1,3,false),
(1,4,true),
(2,3,true),
(2,4,true);

---------------------------------------------JOIN


---------------------------------------------INNER JOIN
--	_______
--	|_|X|_|

-- Trazer dados de duas ou mais tabelas relacionadas: INNER JOIN
-- INNER JOIN selects records that have matching values in both
-- tables.

--SELECT Nome_Prod, Nome_Fornec
--FROM Fornecedores
--INNER JOIN Produtos
--ON Fornecedores.Cod_Fornec = Produtos.Cod_Fornec;

---------------------------------------------LEFT JOIN
--	_______
--	|X|X|_|

---------------------------------------------RIGHT JOIN
--	_______
--	|_|X|X|

---------------------------------------------FULL OUTER JOIN
--	_______
--	|X|X|X|
