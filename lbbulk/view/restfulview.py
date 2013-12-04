from pyramid_restler.view import RESTfulView
from pyramid.response import Response
from lbbulk.model.BulkUpload import BulkUpload
import configparser
import json
import requests

class RegCustomView(RESTfulView):

    def create_member(self):
        member = self.context.create_member(self._get_data())
        id = self.context.get_member_id_as_string(member)
        headers = {'Location': '/'.join((self.request.path, id))}
        return Response(status=201, headers=headers)

    def _get_data(self):
        """ Read json data from the post sent by some source """
        content_type = self.request.content_type
        if content_type == 'application/json':
            data = json.loads(self.request.body)
        elif content_type == 'application/x-www-form-urlencoded':
            data = dict(self.request.POST)
        else:
            data = self.request.params
        data = self.send_to_lightbase(data)
        # Must come with the external key as a value of
        # 'data.json_reg.id_reg'
        return data

    def send_to_lightbase(self, data):
        """ Sends the register to a lightbase table and returns a dict
        with the external key and lighbase's id_reg """
        data['json_reg'] = json.loads(data['json_reg'])
        # converte os filhos pra dicts
        existente = BulkUpload.verifica_registro(data)
        # print(existente.id_reg)
        print('\n\n\n\n\n\n\n\n\n\n')
        registro = self.is_error(data)
        id_source = registro['id_source']
        registro.pop('id_source', None)
        chave_externa = registro['json_reg']['id_reg']
        registro['json_reg'].pop('id_reg', None)
        registro['json_reg'] = json.dumps(registro['json_reg'])
        url = self.get_url_lightbase()
        if existente is None:
            r = requests.post(url, data=registro)
            id_reg = self.is_error_resp(r.json())
            data = {
                    'id_source':id_source,
                    'id_reg':id_reg,
                    'chave_externa':chave_externa
                   }
        else:
            r = requests.put(url, data=registro)
            id_reg = existente
            data = None
        return data

    def get_url_lightbase(self): #TODO
        """ Returns url from config """
        domain = 'http://api.brlight.org'
        base_name = 'wmi'
        url = domain + '/' + base_name + '/reg'
        return url

    def is_error(self,data): #TODO
        return data

    def is_error_resp(self,r):
        if type(r) is dict:
            raise TypeError('Lightbase error ' + str(r['_status']) + ': ' + r['_error_message'])
        return r