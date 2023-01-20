DROP DATABASE IF EXISTS aula_boletim;
CREATE DATABASE IF NOT EXISTS aula_boletim;

use aula_boletim;

create table boletim (
	id integer auto_increment,
	nome_aluno varchar(50),
	disciplina varchar(50),
	nota_final numeric(4,2),
	primary key(id)
);

INSERT INTO boletim
(nome_aluno, disciplina, nota_final)
VALUES
('geronio', 'Banco de Dados', 9.5),
('geronio', 'Filosofia', 3.8),
('geronio', 'Fisica', 5.5),
('Mercio', 'Banco de Dados', 7),
('Mercio', 'Filosofia', 10),
('Lidaneida', 'Banco de Dados', 6),
('Lidaneida', 'Fisica', 5.5);

select disciplina, nota_final from boletim where nome_aluno = 'geronio';

select nome_aluno, disciplina, nota_final from boletim
where nota_final < 7 and disciplina = 'Banco de Dados';

select disciplina, avg(nota_final) as media_notas from boletim
group by disciplina
order by media_notas desc;

select nome_aluno, avg(nota_final) as 'Media' from boletim
group by nome_aluno
order by Media desc;

select disciplina, count(nome_aluno) as total_alunos from boletim
group by disciplina
order by total_alunos desc;

select disciplina, count(nome_aluno) as recuperacao from boletim
where nota_final < 7
group by disciplina
order by recuperacao desc;
