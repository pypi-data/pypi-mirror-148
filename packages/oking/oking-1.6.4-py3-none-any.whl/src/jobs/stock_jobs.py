from datetime import datetime
import logging
import src.database.connection as database
import src.database.utils as utils
from src.database.utils import DatabaseConfig
import src.api.okvendas as api_okvendas
from src.api import slack
from src.database import queries
import src
import time
from src.entities.log import Log

logger = logging.getLogger()


def job_insert_stock_semaphore(job_config_dict: dict):
    """
    Job para inserir estoques no banco semáforo
    Args:
        job_config_dict: Configuração do job
    """
    db_config = utils.get_database_config(job_config_dict)
    if db_config.sql is None:
        logger.warning(job_config_dict.get('job_name') + ' | Comando sql para inserir estoques no semaforo nao encontrado')
    else:
        db = database.Connection(db_config)
        conn = db.get_conect()
        cursor = conn.cursor()

        try:
            logger.info(job_config_dict.get('job_name') + ' | Inserindo estoques no banco semaforo')
            logger.info(db_config.sql)
            cursor.execute(db_config.sql)
            logger.info(job_config_dict.get('job_name') + f' | {cursor.rowcount} estoques inseridos no banco semaforo')
        except Exception as ex:
            logger.error(job_config_dict.get('job_name') + ' | Erro ' + str(ex))
            api_okvendas.post_log(Log(job_config_dict.get('job_name') + ' | Erro ao inserir estoques no banco semaforo' + str(ex), datetime.now().isoformat(), '', 'ESTOQUE'))

        cursor.close()
        conn.commit()
        conn.close()


def job_send_stocks(job_config_dict: dict):
    """
    Job para realizar a atualização dos estoques padrão
    Args:
        job_config_dict: Configuração do job
    """
    db_config = utils.get_database_config(job_config_dict)
    stocks = query_stocks(db_config)
    atualizados = []
    if len(stocks) or 0 > 0:
        logger.info(job_config_dict.get('job_name') + f" | Total de estoques a serem atualizados: {len(stocks)}")
        for stock in stocks:
            try:
                time.sleep(1)
                response, status_code = api_okvendas.send_stocks(src.client_data.get('url_api') + '/catalogo/estoque', stock, src.client_data.get('token_api'))

                if response is not None:
                    conexao = database.Connection(db_config)
                    conn = conexao.get_conect()
                    cursor = conn.cursor()

                    codigo_erp = response['codigo_erp']
                    if response['Status'] == 1 or response['Status'] == 'Success':
                        cursor.execute(queries.get_stock_protocol_command(db_config.db_type), queries.get_command_parameter(db_config.db_type, [codigo_erp]))
                        atualizados.append(response['codigo_erp'])
                    elif (response['Status'] == 'Error' or response['Status'] == 3) and response['Message'] == "Erro ao atualizar o estoque. Produto não existente":
                        logger.warning(job_config_dict.get('job_name') + f' | Erro ao atualizar estoque para o sku {codigo_erp}: {response["Message"]}')
                        api_okvendas.post_log(Log(job_config_dict.get('job_name') + f' | Erro ao atualizar estoque para o sku {codigo_erp}', datetime.now().isoformat(), codigo_erp, 'ESTOQUE'))
                        cursor.execute(queries.get_stock_protocol_command(db_config.db_type), queries.get_command_parameter(db_config.db_type, [codigo_erp]))
                    else:
                        logger.warning(job_config_dict.get('job_name') + f' | Erro ao atualizar estoque para o sku {codigo_erp}: {response["Message"]}')
                        api_okvendas.post_log(Log(job_config_dict.get('job_name') + f' | Erro ao atualizar estoque para o sku {codigo_erp}', datetime.now().isoformat(), codigo_erp, 'ESTOQUE'))

                    cursor.close()
                    conn.commit()
                    conn.close()
            except Exception as e:
                logger.error(job_config_dict.get('job_name') + f' | Erro ao atualizar estoque para o sku {stock.get("codigo_erp")}: {str(e)}')
                api_okvendas.post_log(Log(
                    job_config_dict.get('job_name') + f' | Erro ao atualizar estoque do sku {stock.get("codigo_erp")}: {str(e)}', datetime.now().isoformat(), stock.get('codigo_erp'), 'ESTOQUE'))

        logger.info(job_config_dict.get('job_name') + f' | Atualizado estoques no semaforo: {len(atualizados) or 0}')
    else:
        logger.warning(job_config_dict.get('job_name') + " | Nao ha produtos para atualizar estoque no momento")


def job_send_stocks_ud(job_config_dict: dict):
    """
    Job para realizar a atualização dos estoques por unidade de distribuição
    Args:
        job_config_dict: Configuração do job
    """
    db_config = utils.get_database_config(job_config_dict)
    stocks = query_stocks_ud(db_config)
    p_size = len(stocks) if stocks is not None else 0

    if p_size > 0:
        time.sleep(0.5)
        logger.debug(job_config_dict.get('job_name') + f' | Total de produtos para atualizar estoque: {p_size}')
        count = 0
        for stock in stocks:
            codigo_erp = stock["codigo_erp"]
            try:
                response = api_okvendas.send_stocks_ud(src.client_data.get('url_api') + '/catalogo/estoqueUnidadeDistribuicao', [stock], src.client_data.get('token_api'))
                for res in response:
                    if res.status == 1:
                        protocol_stock(job_config_dict, db_config, codigo_erp)
                        count = count + 1
                    elif (res.status == 'Error' or res.status > 1) and res.message.__contains__("não encontrado"):
                        logger.warning(job_config_dict.get('job_name') + f' | Erro ao atualizar estoque {codigo_erp} erro da api: ' + res.message)
                        protocol_stock(job_config_dict, db_config, codigo_erp)
                    else:
                        logger.error(job_config_dict.get('job_name') + f' | Erro ao atualizar estoque {codigo_erp} erro da api: ' + res.message)
                        api_okvendas.post_log(
                            Log(job_config_dict.get('job_name') + f' | Erro ao atualizar estoque do sku {codigo_erp}: {res.message}', datetime.now().isoformat(), stock.get('codigo_erp'), 'ESTOQUE'))
            except Exception as e:
                logger.error(job_config_dict.get('job_name') + f' | Erro ao atualizar estoque para o sku {stock.get("codigo_erp")}: {str(e)}')
                api_okvendas.post_log(
                    Log(job_config_dict.get('job_name') + f' | Erro ao atualizar estoque do sku {codigo_erp}: {str(e)}', datetime.now().isoformat(), stock.get('codigo_erp'), 'ESTOQUE'))

        logger.info(job_config_dict.get('job_name') + f' | Produtos protocolados no semaforo: {count}')
    else:
        logger.warning(job_config_dict.get('job_name') + f' | Nao ha produtos para atualizar estoque')


def query_stocks_ud(db_config: DatabaseConfig):
    """
    Consulta no banco de dados os estoques pendentes de atualização por unidade de distribuição
    Args:
        db_config: Configuração do banco de dados

    Returns:
    Lista de estoques para realizar a atualização
    """
    stocks = None
    if db_config.sql is None:
        slack.register_warn("Query estoque de produtos nao configurada!")
    else:
        try:
            conexao = database.Connection(db_config)
            conn = conexao.get_conect()
            cursor = conn.cursor()

            # print(db_config.sql)
            cursor.execute(db_config.sql)
            rows = cursor.fetchall()
            # print(rows)
            columns = [col[0] for col in cursor.description]
            results = [dict(zip(columns, row)) for row in rows]

            cursor.close()
            conn.close()
            if len(results) > 0:
                stocks = stock_ud_dict(results)

        except Exception as ex:
            logger.error(str(ex), exc_info=True)

    return stocks


def query_stocks(db_config: DatabaseConfig):
    """
    Consulta no banco de dados os estoques pendentes de atualização padrão
    Args:
        db_config: Configuração do banco de dados

    Returns:
    Lista de estoques para realizar a atualização
    """
    produtos = None
    if db_config.sql is None or db_config.sql == '':
        slack.register_warn("Query estoque de produtos nao configurada!")
    else:
        try:
            conexao = database.Connection(db_config)
            conn = conexao.get_conect()
            cursor = conn.cursor()

            # print(db_config.sql)
            cursor.execute(db_config.sql)
            rows = cursor.fetchall()
            # print(rows)
            columns = [col[0] for col in cursor.description]
            results = [dict(zip(columns, row)) for row in rows]

            cursor.close()
            conn.close()
            if len(results) > 0:
                produtos = stock_dict(results)

        except Exception as ex:
            logger.error(str(ex), exc_info=True)

    return produtos


def stock_dict(produtos):
    lista = []
    for row in produtos:
        pdict = {
            'codigo_erp': str(row['CODIGO_ERP']),
            'quantidade': int(row['QUANTIDADE'])
        }
        lista.append(pdict)

    return lista


def stock_ud_dict(produtos):
    lista = []
    for row in produtos:
        pdict = {
            'unidade_distribuicao': row['CODIGO_UNIDADE_DISTRIBUICAO'],
            'codigo_erp': row['CODIGO_ERP'],
            'quantidade_total': int(row['QUANTIDADE']),
            'parceiro': 1
        }
        lista.append(pdict)

    return lista


def protocol_stock(job_config_dict, db_config: DatabaseConfig, codigo_erp):
    try:
        logger.info(job_config_dict.get('job_name') + f' | Protocolando produto {codigo_erp} no semaforo')
        conn = database.Connection(db_config).get_conect()
        cursor = conn.cursor()
        cursor.execute(queries.get_stock_protocol_command(db_config.db_type), queries.get_command_parameter(db_config.db_type, [codigo_erp]))
        cursor.close()
        conn.commit()
        conn.close()
    except Exception as e:
        logger.error(job_config_dict.get('job_name') + f' | Erro ao protocolar estoque do sku {codigo_erp}: {str(e)}')
