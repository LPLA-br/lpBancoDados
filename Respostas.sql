USE DESCONTOS;
-- $ mysql -u USUARIODB -t -p < Respostas.sql

-- abc def ghi jk

SELECT 'A - Não visível após execução da questão C' AS 'QUESTÃO';
-- Sem desconto.
SELECT Id_nf, Id_item, Cod_prod, Valor_unit FROM Descontos WHERE Desconto IS NULL;

-------------------------------------------------------------------------------------------

SELECT 'B' AS 'QUESTÃO';
-- Valor_vendido - Unidade do produto com desconto.
SELECT Id_item ,Cod_prod, Valor_unit,
TRUNCATE( Valor_unit - (Valor_unit*(Desconto/100)) ,2) AS Valor_vendido
FROM Descontos WHERE Desconto IS NOT NULL;
-- NOTA:
-- Valor_vendido é um exemplo de valor derivado de valores armazenados
-- obtidos por operação matemática.

-------------------------------------------------------------------------------------------

SELECT 'C - update' AS 'QUESTÃO';
-- NULL nem é gente! substituir NULL por 0 !!!
UPDATE Descontos SET Desconto = 0 WHERE Desconto IS NULL;

-------------------------------------------------------------------------------------------

SELECT 'D' AS 'QUESTÃO';
--Valor_vendido - Unidade do produto com desconto.

SELECT  Id_nf, Id_item, Cod_prod, Valor_unit,
Quantidade * Valor_unit AS Valor_total,
Desconto,
TRUNCATE( Valor_unit - ( Valor_unit*( Desconto/100 ) ) ,2) AS Valor_vendido
FROM Descontos;

/*
SELECT  Valor_unit,
Quantidade * Valor_unit AS Valor_total_SemDesconto,
Desconto,
TRUNCATE( Valor_unit - ( Valor_unit*( Desconto/100 ) ) ,2) AS Valor_vendido,
Quantidade * TRUNCATE( Valor_unit - ( Valor_unit*( Desconto/100 ) ) ,2) AS Valor_total_ComDesconto
FROM Descontos ORDER BY Valor_unit DESC;
*/

-------------------------------------------------------------------------------------------

SELECT 'E' AS 'QUESTÃO';

SELECT Id_nf, sum( Quantidade * Valor_unit ) AS Valor_total
FROM Descontos GROUP BY Id_nf ORDER BY Valor_total DESC;

-------------------------------------------------------------------------------------------

SELECT 'F' AS 'QUESTÃO';

SELECT Id_nf,
sum( TRUNCATE( Valor_unit - ( Valor_unit * ( Desconto / 100 ) ), 2) ) AS Valor_vendido
FROM Descontos GROUP BY Id_nf ORDER BY Valor_vendido DESC;

-------------------------------------------------------------------------------------------

SELECT 'G' AS 'QUESTÃO';

SELECT Cod_prod, sum(Quantidade) AS Quantidade FROM Descontos GROUP BY Cod_prod;


-------------------------------------------------------------------------------------------

SELECT 'H' AS 'QUESTÃO';

SELECT Id_nf, Cod_prod, Quantidade FROM Descontos WHERE Quantidade > 10
ORDER BY Quantidade DESC;

-------------------------------------------------------------------------------------------

SELECT 'I' AS 'QUESTÃO';

SELECT Id_nf, sum( Quantidade * Valor_unit ) AS Valor_tot
FROM Descontos GROUP BY Id_nf HAVING Valor_tot > 500;

-------------------------------------------------------------------------------------------

SELECT 'J' AS 'QUESTÃO';
SELECT Cod_prod ,max(Desconto) AS Maior, min(Desconto) AS Menor, TRUNCATE( avg(Desconto) ,2) AS Media FROM Descontos GROUP BY Cod_prod;

-------------------------------------------------------------------------------------------

SELECT 'K' AS 'QUESTÃO';
select Id_nf, Id_item, Cod_prod, Quantidade from Descontos;
-- Observações lógicas

-- 256
-- id_nf com mais de tres itens diferentes vendidos(min de 4).
-- Id_item nunca se repete por id_nf
-- Cod_prod nunca  se repete por id_nf na tabelas?
-- 5 produtos, 7 nf's 

SELECT Id_nf, count(Cod_prod) AS Qtd_itens FROM Descontos GROUP BY Id_nf
HAVING Qtd_itens > 3;

-------------------------------------------------------------------------------------------


