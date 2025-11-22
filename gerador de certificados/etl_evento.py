import mysql.connector
import pandas as pd
import pandas

class EtlSevenpro:
    def __init__(self):
        self.host = ''
        self.user = ''
        self.password = ''
        self.database = ''


    def __extracao(self, query: str) -> pandas:
        conn = mysql.connector.connect(
            host=self.host,
            user=self.user,
            password=self.password,
            database=self.database,
            ssl_disabled=False,
            ssl_verify_cert=False
        )
        df = pd.read_sql(query, conn)
        conn.close()
        return df
    
    def __transformacao(self, df: pandas) -> pandas:
        df.drop('id', axis=1, inplace=True)
        df['usuario'] = df['usuario'].str.title()
        df['nome_arquivo'] = df['usuario'].str.replace(' ', '')
        df['email'] = df['email'].str.lower()
        return df
    
    def __carga(self, df: pandas) -> None:
        df.to_csv('data.csv', sep=';', encoding='utf-8', header=True, index=False)
        return
    

    def run(self, query: str) -> None:
        dados = self.__extracao(query)
        dados = self.__transformacao(dados)
        self.__carga(dados)
        return
        





if __name__ == '__main__':
    query = '''WITH nao_staff AS (
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
        DISTINCT ns.co_user as id,
        ns.no_user as usuario,
        ns.no_email as email,
        COALESCE(s.horas_totais, 0) + COALESCE(ns.horas_totais, 0) AS horas
        FROM nao_staff ns
    LEFT JOIN staff s ON (s.co_user = ns.co_user)
    ORDER BY ns.no_user;'''

    banco = EtlSevenpro()
    banco.run(query)