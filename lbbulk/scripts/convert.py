#!../../../../../../bin/python
__author__ = 'eduardo'
import sys, getopt
from lbbulk.lib.csv import CSVFileHandler

class Convert(object):
    """
    Classe para o comando de conversão
    """
    def __init__(self, parameters):
        """
        Construtor
        """
        self.parameters = parameters

    def __doc__(self):
        """
        Documentação dos comandos
        """
        return "Comandos válidos são: " \
               "-i arquivo de entrada " \
               "-o arquivo de saída"

    def csv2json(self):
        """
        Converte o arquivo CSV para o JSON
        """
        csv_handler = CSVFileHandler(**self.parameters)
        csv_handler.csv2json()
        return

if __name__ == '__main__':
    parameters = dict()
    parameters['outfile'] = "/tmp/saida.xml"
    # Faz o parsing dos argumentos
    try:
        opts, args = getopt.getopt(sys.argv[1:], "hi:o:d:a:q:f:", ["ifile=", "ofile=", "help=", "delimiter=", "as_dict=", "quotechar=", "fieldnames="])
    except getopt.GetoptError:
        print('convert.py -i <inputfile> -o <outputfile>')
        sys.exit(2)
    for opt, arg in opts:
        if opt in ('-h', "--help"):
            convert = Convert(parameters=parameters)
            print(convert.__doc__())
            sys.exit()
        elif opt in ("-i", "--ifile"):
            parameters['filename'] = arg
        elif opt in ("-o", "--ofile"):
            parameters['outfile'] = arg
        elif opt in ("-d", "--delimiter"):
            parameters['delimiter'] = arg
        elif opt in ("-a", "--as_dict"):
            parameters['as_dict'] = arg
        elif opt in ("-q", "--quotechar"):
            parameters['quotechar'] = arg
        elif opt in ("-f", "--fieldnames"):
            parameters['fieldnames'] = arg

    # Executa o comando
    convert = Convert(parameters=parameters)
    convert.csv2json()