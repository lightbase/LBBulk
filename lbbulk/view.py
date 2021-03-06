# -*- coding: utf-8 -*-
import os
import cgi
import sys
import uuid
import json
import ijson
import shutil
import zipfile
import requests
import logging
import datetime
from . import utils
from lbbulk import config
from multiprocessing import Process
from pyramid.view import view_config
from pyramid.response import Response
import psycopg2
from psycopg2.extensions import AsIs

log = logging.getLogger()
orgao_name = ""

@view_config(context=Exception)
def error_view(exc, request):
    """ Customized Exception View
    """
    #l = traceback.extract_tb(request.exc_info[2])
    exc_type, exc_obj, exc_tb = sys.exc_info()
    exc_msg = exc_obj.args
    if len(exc_obj.args) > 0:
        exc_msg = exc_obj.args[0]
    return Response(exc_msg, status=500)


def zip_upload(request):
    """
    Faz upload up arquivo .zip
    :param request: Requisição HTTP
    :return: Resposta json
    """
    global orgao_name
    nome_base = request.params.get('source_name')
    orgao_name = nome_base
    default_value = {
        'attribute_value': request.params.get('default_value'),
        'attribute_name': request.params.get('default_field')
    }

    log.debug("Inserindo coleta para a base %s", nome_base)

    url = config.LIGHTBASE_URL + "/" + nome_base + "/doc"
    log.debug("URL para inserção da base: %s", url)

    file_ = request.params.get('file')

    if not isinstance(file_, cgi.FieldStorage):
        return Response('File is not a zip file', status=500)
    else:
        ext_dir, json_file_path = extract_zip(file_)
        process = Process(target=bulk_upload, args=(ext_dir, json_file_path,
            url, default_value))
        process.start()

    return Response('OK', status=200)


def extract_zip(zfile):
    """
    Extrai arquivo .zip
    :param zfile: Nome do arquivo .zip a ser extraído
    :return: JSON no seguinte formato:
        {
            ext_dir: diretório onde os arquivos foram extraídos,
            json_file_path: arquivo JSON com dados extraídos
        }
    """
    log.debug("Extraindo arquivo ...")
    if not os.path.exists(config.EXTRACT_DIR):
        os.makedirs(config.EXTRACT_DIR)
    identifier = str(uuid.uuid4())
    zpath = config.EXTRACT_DIR + '/' + identifier + '.zip'
    zpath = os.path.abspath(zpath)

    try:
        # write bytes to disk
        with open(zpath, 'wb') as f:
            f.write(zfile.file.read())
    except Exception as e:
        raise Exception('Error while uploading file! %s' % e)

    ext_dir = os.path.abspath(config.EXTRACT_DIR + '/' + identifier)

    if not os.path.exists(ext_dir):
            os.makedirs(ext_dir)

    try:
        # extract zip file
        with zipfile.ZipFile(zpath, "r") as z:
            z.extractall(ext_dir)
    except Exception as e:
        raise Exception('Error while extracting zip file! %s' % e)

    # remove zip file
    os.remove(zpath)

    # Find JSON file
    json_file_path = None
    for (dirpath, dirnames, filenames) in os.walk(ext_dir):
        for file in filenames:
            full_path = os.path.join(dirpath, file)
            root, ext = os.path.splitext(full_path)
            if ext == '.json':
                json_file_path = full_path

    if json_file_path is None:
        raise Exception('Could not find any JSON file in zip file!!! Full path: %s', ext_dir)
    #json_file_path = ext_dir + '/' + config.JSON_FILENAME
    #json_file_path = os.path.abspath(json_file_path)
    log.debug("Caminho completo do arquivo JSON %s", json_file_path)

    if not os.path.exists(json_file_path):
        raise Exception('Could not find any json file in zip file: %s' %
            json_file_path)

    return ext_dir, json_file_path


def insert_relacional(document_json):
    host = config.HOST_DB
    database = config.DATABASE_DB
    user = config.USER_DB
    password = config.PASSWORD_DB
    conn = psycopg2.connect(host=host, database=database, user=user, password=password)
    cur = conn.cursor()
    verify_base = utils.RelacionalBase().verifyDatabase(conn)
    if verify_base:
        json_final, softwarelist = utils.RelacionalBase.removeGroupJson(document_json)
        if json_final.get('nome_orgao') is None:
            json_final["nome_orgao"] = orgao_name
        columns = json_final.keys()
        values = [json_final[column] for column in columns]
        insert_statement = 'INSERT INTO cacic_relacional.cacic_relacional (%s) values %s RETURNING id'
        cur.execute(insert_statement, (AsIs(','.join(columns)), tuple(values)))
        for item in cur:
            pc_id = item
            pc_id = pc_id[0]
        log.info("ID_PC = %s", pc_id)

        for software in softwarelist:
            # Um software em cada linha da tabela
            insert_statement = """
                INSERT INTO cacic_relacional.cacic_relacional_softwarelist (
                  pc_id,
                  hash_machine,
                  nome_orgao,
                  data_coleta,
                  siorg,
                  mac,
                  ip_computador,
                  ip_rede,
                  nome_rede,
                  data_ultimo_acesso,
                  nome_softwarelist
                  ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
              """

            cur.execute(
                insert_statement,
                (
                    pc_id,
                    json_final["hash_machine"],
                    json_final["nome_orgao"],
                    json_final["data_coleta"],
                    json_final.get("siorg"),
                    json_final["mac"],
                    json_final["ip_computador"],
                    json_final["ip_rede"],
                    json_final["nome_rede"],
                    json_final["data_ultimo_acesso"],
                    software
                )
            )
        conn.commit()
    else:
        log.error("Erro ao verificar ou criar a base.")
    conn.close()
    return True


def bulk_upload(ext_dir, file_path, url, default_value=None):
    """
    Faz upload de um conjunto de registros
    :param ext_dir: Diretório externo para extração do arquivo .zip com o conjunto de registros
    :param file_path: Caminho completo para arquivo JSON extraído
    :param url: URL do Lightbase para envio dos registros
    :param default_value: Um valor padrão para ser adicionado em todos os regisros da base
    """
    file_ = open(file_path, 'rb')
    data_coleta = datetime.datetime.now().strftime("%d/%m/%Y")
    print("default_value:", default_value)
    print("file:", file_path)
    print("data coleta", data_coleta)
    try:
        objects = ijson.items(file_, 'results.item')
        computers = (computer for computer in objects)
    except Exception as e:
        print('Error While Reading JSON file: %s' % e)

    for computer in computers:
        # Ajusta data da coleta
        computer['data_coleta'] = data_coleta
        if default_value is not None:
            log.debug("Valor padrão: \n%s", default_value)
            if default_value.get('attribute_name') is None or \
                default_value.get('attribute_value') is None:
                # None of the attributes can be null
                log.debug("Valores padrão não podem ter definições vazias vazios\n")
                pass
            else:
                try:
                    computer[default_value['attribute_name']] = default_value['attribute_value']
                except KeyError:
                    log.error("Não foi passível ajustar valor %s para o campo %s", default_value['attribute_name'], default_value['attribute_value'])

        document_old = computer
        document = json.dumps(computer, cls=utils.DecimalEncoder)

        response = requests.post(url, data={
            'value': document
        })
        # Create and insert in relational database
        insert_database = insert_relacional(document_old)

        if response.status_code == 200 and insert_database:
            log.debug("Registro inserido com sucesso!!!\n%s", document)
        else:
            log.error("Erro na inserção do registro!!! Código = %s\n%s", response.status_code, response.text)

    shutil.rmtree(ext_dir)
