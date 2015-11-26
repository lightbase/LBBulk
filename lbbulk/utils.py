# -*- coding: utf-8 -*-
__author__ = 'eduardo'

import json
from decimal import *
import psycopg2
from psycopg2.extensions import AsIs

class DecimalEncoder(json.JSONEncoder):
    """
    Adiciona conversão de decimais no JSON
    """
    def default(self, obj):
        """Convert ``obj`` to something JSON encoder can handle."""

        if isinstance(obj, Decimal):
            obj = int(obj)
        elif isinstance(obj, str):
            if obj.isdigit():
                obj = int(obj)
        else:
            # method to generate JSON
            obj = obj._encoded()

        return obj

class RelacionalBase():
        def __ini__(self):
            pass

        def verifyDatabase(self, conn):
            try:
                cur = conn.cursor()
                cur.execute("SELECT EXISTS (SELECT schema_name FROM information_schema.schemata WHERE schema_name = 'cacic_relacional');")
                for item in cur:
                    check_exists = item
                check_exists = check_exists[0]
                if not check_exists:
                    cur.execute ("CREATE SCHEMA cacic_relacional;")
                    # cur.execute ("CREATE TABLE cacic_relacional.cacic_relacional("
                    #              "id BIGSERIAL PRIMARY KEY,"
                    #              "hash_machine character varying(250),"
                    #              "win32_diskdrive_size bigint,"
                    #              "name_orgao character(250),"
                    #              "data_coleta character varying(250),"
                    #              "data_ultimo_acesso character varying(250),"
                    #              "win32_processor_manufacturer character varying(250),"
                    #              "win32_processor_numberoflogicalprocessors bigint,"
                    #              "operatingsystem_version character varying(250),"
                    #              "win32_diskdrive_model character varying(250),"
                    #              "operatingsystem_caption character varying(250),"
                    #              "win32_processor_caption character varying(250),"
                    #              "win32_physicalmemory_capacity bigint,"
                    #              "win32_processor_family bigint,"
                    #              "win32_bios_manufacturer character varying(250),"
                    #              "win32_physicalmemory_memorytype bigint,"
                    #              "win32_diskdrive_caption character varying(250),"
                    #              "operatingsystem_installdate character varying(250),"
                    #              "win32_processor_maxclockspeed character varying(250));")
                    cur.execute ("CREATE TABLE cacic_relacional.cacic_relacional("
                                 "id BIGSERIAL PRIMARY KEY,"
                                 "hash_machine varchar(250),"
                                 "win32_diskdrive_size varchar(250),"
                                 "nome_orgao varchar(250),"
                                 "data_coleta varchar(250),"
                                 "siorg varchar,"
                                 "mac varchar,"
                                 "ip_computador varchar,"
                                 "ip_rede varchar,"
                                 "nome_rede varchar,"
                                 "data_ultimo_acesso varchar(250),"
                                 "win32_processor_manufacturer varchar(250),"
                                 "win32_processor_numberoflogicalprocessors varchar(250),"
                                 "operatingsystem_version varchar(250),"
                                 "win32_diskdrive_model varchar(250),"
                                 "operatingsystem_caption varchar(250),"
                                 "win32_processor_caption varchar(250),"
                                 "win32_physicalmemory_capacity varchar(250),"
                                 "win32_processor_family varchar(250),"
                                 "win32_bios_manufacturer varchar(250),"
                                 "win32_physicalmemory_memorytype varchar(250),"
                                 "win32_diskdrive_caption varchar(250),"
                                 "operatingsystem_installdate varchar(250),"
                                 "win32_processor_maxclockspeed varchar(250));")
                    #Criando tabela de softwarelist
                    cur.execute ("CREATE TABLE cacic_relacional.cacic_relacional_softwarelist("
                                 "id BIGSERIAL PRIMARY KEY,"
                                 "nome_softwarelist varchar(250)[],"
                                 "pc_id integer);")
                    conn.commit()
                return True
            except Exception as e:
                return False

        def removeGroupJson(json_data):
            new_json = {}
            softwarelist = list()
            for item in json_data.keys():
                if isinstance(json_data[item], str):
                    new_json[item] = json_data[item]
                elif isinstance(json_data[item], list):
                    # TODO: ALTERAR PARA CRIAR A TABELA DE SOFTWARELIST
                    for software in json_data[item]:
                        softwarelist.append(software)
                    pass
                else:
                    for item_group in json_data[item].keys():
                        new_json[item_group] = json_data[item][item_group]
            return new_json,softwarelist
