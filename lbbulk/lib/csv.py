__author__ = 'eduardo'
import csv
import json


class CSVFileHandler:
    """
    Classe para trabalhar com arquivos CSV
    """
    def __init__(self, filename, outfile, delimiter=';', quotechar='"', as_dict=True, fieldnames=None):
        """
        O Construtor abre o arquivo para leitura e inicia os parâmetros obrigatórios
        """
        self.outfile = outfile
        self.delimiter = delimiter
        self.quotechar = quotechar
        self.as_dict = as_dict
        self.fieldnames = fieldnames
        self.filename = filename
        self.open(filename)

    def __del__(self):
        """
        Fechar o arquivo é suficiente?
        """
        self.close()

    def open(self, filename):
        """
        Abrir o arquivo
        """
        self.file = open(filename, 'r')
        if self.as_dict:
            self.reader = csv.DictReader(self.file,
                                         fieldnames=self.fieldnames,
                                         delimiter=self.delimiter,
                                         quotechar=self.quotechar)
        else:
            self.reader = csv.reader(self.file,
                                     delimiter=self.delimiter,
                                     quotechar=self.quotechar)

    def close(self):
        self.file.close()

    def process(self, function, args):
        """
        Processa o arquivo carregado
        """
        #for row in self.reader:
        #    function(row, args)
        function(args)

    def csv2json(self):
        """
        Converte o arquivo CSV de entrada em um JSON

        Fonte: http://stackoverflow.com/questions/1884395/csv-to-json-script
        """
        # Normaliza o nome dos campos primeiro
        self.normalize()
        out = [obj for obj in self.reader]

        if out:
            with open(self.outfile, 'w+') as json_file:
                json_file.write(json.dumps(out))
        else:
            # Adiciona alguma mensagem de erro
            print("ERRO - Erro ao processar o arquivo CSV")

    def normalize(self):
        fieldnames = list()
        for linha in self.reader:
            # Lê somente a primeira linha
            campos = linha
            break
        i = 0
        for chave in campos:
            # O tamanho maximo do nome do campo é 10
            nome = self.cap(chave, 10).strip()
            # Adiciona ao nome o número do campo
            nome += "_"+str(i)
            fieldnames.append(nome)
            i += 1
        # Novo nome do campo
        self.fieldnames = fieldnames

        # Abre e fecha o arquivo de novo
        self.close()
        self.open(self.filename)

    def cap(self, s, l):
        return s if len(s)<=l else s[0:l]