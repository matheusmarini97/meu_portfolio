-- QUERY QUE SELECIONA QUANTOS INSCRITOS TEM POR CURSO
SELECT tb23.no_curso, COUNT(DISTINCT tb10.co_user) AS inscritos
FROM tb10_inscricao_apresentacao tb10
INNER JOIN tb02_user tb02 ON (tb10.co_user = tb02.co_user)
INNER JOIN tb08_apresentacao tb08 ON (tb10.co_apresentacao = tb08.co_apresentacao)
INNER JOIN tb22_aluno_curso tb22 ON (tb22.co_user = tb10.co_user)
INNER JOIN tb23_tipo_curso tb23 ON (tb22.co_tipo_curso = tb23.co_tipo_curso)
WHERE tb08.co_evento = 2
GROUP BY tb23.no_curso;


-- CADASTRA OS USUARIOS COM TIPO CURSO 22 NAS APRESENTACOES DO co_evento 2
INSERT INTO tb10_inscricao_apresentacao (co_user, ic_apresentacao, ic_pago, ic_pago_configmado, co_apresentacao, co_cadastro, ic_ativo)
SELECT u.co_user, 0 AS ic_apresentacao, 0 AS ic_pago, 0 AS ic_pago_configmado, a.co_apresentacao, 15 AS co_cadastro, 1 AS ic_ativo
FROM (
SELECT tb02.co_user
FROM tb02_user tb02
INNER JOIN tb22_aluno_curso tb22 ON (tb02.co_user = tb22.co_user)
WHERE tb22.co_tipo_curso = 22
) u
CROSS JOIN (
SELECT tb08.co_apresentacao FROM tb08_apresentacao tb08 WHERE tb08.co_evento = 2
) a;


-- ALTERA OS ALUNOS QUE ESTÃO COM co_curso = 7 PARA co_curso = 17
REPLACE INTO tb22_aluno_curso
SELECT tb22.co_aluno_curso, tb22.co_user, 17 AS co_tipo_curso FROM tb10_inscricao_apresentacao tb10
LEFT JOIN tb08_apresentacao tb08 ON (tb08.co_apresentacao = tb10.co_apresentacao)
LEFT JOIN tb22_aluno_curso tb22 ON (tb22.co_user = tb10.co_user)
LEFT JOIN tb23_tipo_curso tb23 ON (tb23.co_tipo_curso = tb22.co_tipo_curso)
WHERE tb08.co_evento = 2 AND tb23.no_curso = "TI - Tecnólogos - FAP";


-- CALCULA QUANTOS INSCRITOS TEM EM CADA APRESENTAÇÃO
SELECT sexta.*, sabado_manha.*, sabado_tarde.* FROM (
SELECT count(*) AS inscritos_sexta_noite
FROM tb10_inscricao_apresentacao tb10
INNER JOIN tb08_apresentacao tb08 ON (tb08.co_apresentacao = tb10.co_apresentacao)
WHERE tb08.co_evento = 2 AND tb08.co_apresentacao = 198
GROUP BY tb10.co_apresentacao
) AS sexta, (
SELECT count(*) AS inscritos_sabado_manha
FROM tb10_inscricao_apresentacao tb10
INNER JOIN tb08_apresentacao tb08 ON (tb08.co_apresentacao = tb10.co_apresentacao)
WHERE tb08.co_evento = 2 AND tb08.co_apresentacao = 199
GROUP BY tb10.co_apresentacao
) AS sabado_manha, (
SELECT count(*) AS inscritos_sabado_tarde
FROM tb10_inscricao_apresentacao tb10
INNER JOIN tb08_apresentacao tb08 ON (tb08.co_apresentacao = tb10.co_apresentacao)
WHERE tb08.co_evento = 2 AND tb08.co_apresentacao = 200
GROUP BY tb10.co_apresentacao
) AS sabado_tarde;


-- INSCREVE O USUARIO 15 NAS APRESENTACOES DO co_evento = 2
INSERT INTO tb14_checkin_apresentacao 
SELECT 
	NULL AS co_checkin, 
	tb08.co_apresentacao, 
	tb10.co_user, 
	NULL AS co_hora, 
	15 AS co_staff, 
	CURRENT_TIMESTAMP() AS dt_create, 
	0 AS ic_sincronismo, 
	tb10.co_inscricao_apresentacao 
FROM tb10_inscricao_apresentacao tb10
INNER JOIN tb08_apresentacao tb08 ON (tb10.co_apresentacao = tb08.co_apresentacao)
WHERE tb08.co_evento = 2 AND tb10.co_user = 15


-- LISTA OS CHECKINS DO co_evento = 2
SELECT * FROM tb14_checkin_apresentacao tb14
INNER JOIN tb08_apresentacao tb08 ON (tb08.co_apresentacao = tb14.co_apresentacao)
WHERE tb08.co_evento = 2


-- EXTRAI OS DADOS PARA OS CERTIFICADOS DO SIMPÓSIO
WITH sexta AS (
SELECT DISTINCT tb02.co_user, tb02.no_user, 2 AS horas
FROM tb14_checkin_apresentacao tb14
INNER JOIN tb02_user tb02 ON (tb14.co_user = tb02.co_user)
INNER JOIN tb10_inscricao_apresentacao tb10 ON (tb10.co_apresentacao = tb14.co_apresentacao)
INNER JOIN tb08_apresentacao tb08 ON (tb08.co_apresentacao = tb10.co_apresentacao)
WHERE tb08.co_evento = 2 AND tb10.co_apresentacao = 198
), sabado_manha AS (
SELECT DISTINCT tb02.co_user, tb02.no_user, 3 AS horas
FROM tb14_checkin_apresentacao tb14
INNER JOIN tb02_user tb02 ON (tb14.co_user = tb02.co_user)
INNER JOIN tb10_inscricao_apresentacao tb10 ON (tb10.co_apresentacao = tb14.co_apresentacao)
INNER JOIN tb08_apresentacao tb08 ON (tb08.co_apresentacao = tb10.co_apresentacao)
WHERE tb08.co_evento = 2 AND tb10.co_apresentacao = 199
), sabado_tarde AS (
SELECT DISTINCT tb02.co_user, tb02.no_user, 5 AS horas
FROM tb14_checkin_apresentacao tb14
INNER JOIN tb02_user tb02 ON (tb14.co_user = tb02.co_user)
INNER JOIN tb10_inscricao_apresentacao tb10 ON (tb10.co_apresentacao = tb14.co_apresentacao)
INNER JOIN tb08_apresentacao tb08 ON (tb08.co_apresentacao = tb10.co_apresentacao)
WHERE tb08.co_evento = 2 AND tb10.co_apresentacao = 200
), inscritos AS (
SELECT DISTINCT tb02.co_user, tb02.no_user, tb02.no_email
FROM tb10_inscricao_apresentacao tb10
INNER JOIN tb08_apresentacao tb08 ON (tb10.co_apresentacao = tb08.co_apresentacao)
INNER JOIN tb02_user tb02 ON (tb10.co_user = tb02.co_user)
WHERE tb08.co_evento = 2
)
SELECT 
	inscritos.co_user, 
	inscritos.no_user,
	inscritos.no_email,
	COALESCE(sexta.horas, 0) + COALESCE(sabado_manha.horas, 0) + COALESCE(sabado_tarde.horas, 0) AS horas_totais
FROM sexta 
INNER JOIN sabado_manha ON (sexta.co_user = sabado_manha.co_user)
INNER JOIN sabado_tarde ON (sabado_tarde.co_user = sexta.co_user)
RIGHT JOIN inscritos ON (sexta.co_user = inscritos.co_user)
WHERE (COALESCE(sexta.horas, 0) + COALESCE(sabado_manha.horas, 0) + COALESCE(sabado_tarde.horas, 0)) > 0
ORDER BY no_user;


-- LISTA OS USUARIOS QUE TEM ALGUM CHECKIN NO EVENTO 2
SELECT DISTINCT tb02.co_user, tb02.no_user, tb02.no_email, 12 AS horas_totais
FROM tb14_checkin_apresentacao tb14
INNER JOIN tb02_user tb02 ON (tb14.co_user = tb02.co_user)
INNER JOIN tb10_inscricao_apresentacao tb10 ON (tb10.co_apresentacao = tb14.co_apresentacao)
INNER JOIN tb08_apresentacao tb08 ON (tb08.co_apresentacao = tb10.co_apresentacao)
WHERE tb08.co_evento = 2 AND tb14.co_apresentacao IN (198, 199, 200)


-- LISTA E SOMA OS USUARIOS E STAFFS QUE TEM ALGUM CHECKIN NO EVENTO 2
WITH nao_staff AS (
SELECT DISTINCT tb02.co_user, tb02.no_user, tb02.no_email, 12 AS horas_totais
FROM tb14_checkin_apresentacao tb14
INNER JOIN tb02_user tb02 ON (tb14.co_user = tb02.co_user)
INNER JOIN tb10_inscricao_apresentacao tb10 ON (tb10.co_apresentacao = tb14.co_apresentacao)
INNER JOIN tb08_apresentacao tb08 ON (tb08.co_apresentacao = tb10.co_apresentacao)
WHERE tb08.co_evento = 2 
AND	tb14.co_apresentacao IN (198, 199, 200)
), staff AS ( 
SELECT DISTINCT tb14.co_staff AS co_user, tb02.no_user, tb02.no_email, 12 AS horas_totais
FROM tb14_checkin_apresentacao tb14
INNER JOIN tb02_user tb02 ON (tb14.co_staff = tb02.co_user)
INNER JOIN tb10_inscricao_apresentacao tb10 ON (tb10.co_apresentacao = tb14.co_apresentacao)
INNER JOIN tb08_apresentacao tb08 ON (tb08.co_apresentacao = tb10.co_apresentacao)
WHERE tb08.co_evento = 2 
AND tb14.co_apresentacao IN (198, 199, 200)
)
SELECT 
	DISTINCT ns.co_user,
	ns.no_user,
	ns.no_email,
	COALESCE(s.horas_totais, 0) + COALESCE(ns.horas_totais, 0) AS horas_totais
	FROM nao_staff ns
LEFT JOIN staff s ON (s.co_user = ns.co_user);


-- INSERIR 2 PESSOAS COMO STAFF DO EVENTO
INSERT tb35_staff 
SELECT 
	NULL AS nu_staff, 
	co_user AS co_staff, 
	2 AS co_evento, 
	15 AS co_create,
	CURRENT_TIMESTAMP() AS dt_create
FROM tb02_user 
WHERE no_email IN ('julianysiqueirafalcao@gmail.com', 'geovannafap2024@gmail.com');


-- ATRIBUI OS STAFFS AS APRESENTACOES DO EVENTO 2
REPLACE INTO tb28_staff_apresentacao
SELECT 
	NULL AS co_staff_apresentacao, a.*, b.*, CURRENT_TIMESTAMP() AS dt_create
FROM (
(SELECT tb08.co_apresentacao FROM tb08_apresentacao tb08 WHERE tb08.co_evento = 2) a
CROSS JOIN
(SELECT nu_staff FROM tb35_staff WHERE co_evento = 2) b
);


-- FAZ CHECKIN DO USUARIO 15 NA APRESENTACAO 200
INSERT INTO tb14_checkin_apresentacao 
SELECT 
	NULL AS co_checkin, 
	co_apresentacao, 
	co_user, 
	NULL AS co_hora, 
	15 AS co_staff, 
	CURRENT_TIMESTAMP() AS dt_create,
	0 AS ic_sincronismo,
	co_inscricao_apresentacao 
FROM tb10_inscricao_apresentacao WHERE co_user = 15 AND co_apresentacao = 200;


-- PEGA A METRICA DE INSCRITOS E CHECKINS POR APRESENTAÇÃO NO EVENTO 2
WITH inscritos AS(
SELECT 
	CASE 
		WHEN tb08.co_apresentacao = 198 THEN 'Sexta a noite'
		WHEN tb08.co_apresentacao = 199 THEN 'Sábado pela manhã'
		WHEN tb08.co_apresentacao = 200 THEN 'Sábado pela tarde'
		ELSE tb08.co_apresentacao 
	END AS apresentacao,
	 COUNT(*) AS qt_inscritos
FROM tb10_inscricao_apresentacao tb10
INNER JOIN tb08_apresentacao tb08 ON (tb10.co_apresentacao = tb08.co_apresentacao)
WHERE tb10.co_apresentacao IN (198, 199, 200)
GROUP BY tb10.co_apresentacao 
), checkin AS (
SELECT 
	CASE 
		WHEN tb08.co_apresentacao = 198 THEN 'Sexta a noite'
		WHEN tb08.co_apresentacao = 199 THEN 'Sábado pela manhã'
		WHEN tb08.co_apresentacao = 200 THEN 'Sábado pela tarde'
		ELSE tb08.co_apresentacao 
	END AS apresentacao,
	 COUNT(tb14.co_user) AS qt_checkin
FROM tb08_apresentacao tb08
LEFT JOIN tb14_checkin_apresentacao tb14 ON (tb14.co_apresentacao = tb08.co_apresentacao)
WHERE tb08.co_apresentacao IN (198, 199, 200)
GROUP BY tb08.co_apresentacao 
)
SELECT c.apresentacao, i.qt_inscritos, c.qt_checkin, COALESCE(c.qt_inscritos, 0)
FROM inscritos i
INNER JOIN checkin c ON (c.apresentacao = i.apresentacao)


-- TIRANDO RELATÓRIO DOS CHECKINS QUE CADA STAFF FEZ EM CADA APRESENTACAO
WITH sexta AS(
SELECT tb02.co_user, tb02.no_user, COUNT(DISTINCT tb14.co_user) AS checkins_sexta
FROM tb14_checkin_apresentacao tb14 
INNER JOIN tb02_user tb02 ON (tb02.co_user = tb14.co_staff)
WHERE tb14.co_apresentacao = 198
GROUP BY tb14.co_staff
), sabado_manha AS(
SELECT tb02.co_user, tb02.no_user, COUNT(DISTINCT tb14.co_user) AS checkins_sabado_manha
FROM tb14_checkin_apresentacao tb14 
INNER JOIN tb02_user tb02 ON (tb02.co_user = tb14.co_staff)
WHERE tb14.co_apresentacao = 199
GROUP BY tb14.co_staff
), sabado_tarde AS(
SELECT tb02.co_user, tb02.no_user, COUNT(DISTINCT tb14.co_user) AS checkins_sabado_tarde
FROM tb14_checkin_apresentacao tb14 
INNER JOIN tb02_user tb02 ON (tb02.co_user = tb14.co_staff)
WHERE tb14.co_apresentacao = 200
GROUP BY tb14.co_staff
), staffs AS (
SELECT co_user, no_user FROM tb02_user tb02
INNER JOIN tb35_staff tb35 ON (tb02.co_user = tb35.co_staff)
WHERE tb35.co_evento = 2
)
SELECT 
	s.no_user, 
	COALESCE(sn.checkins_sexta, 0) AS sexta, 
	COALESCE(sm.checkins_sabado_manha, 0) AS sabado_manha,
	COALESCE(st.checkins_sabado_tarde, 0) AS sabado_tarde
FROM staffs s
LEFT JOIN sexta sn ON (s.co_user = sn.co_user)
LEFT JOIN sabado_manha sm ON (s.co_user = sm.co_user)
LEFT JOIN sabado_tarde st ON (s.co_user = st.co_user)
ORDER BY no_user;