from pyramid_restler.view import RESTfulView
import configparser
import json
import requests

class RegCustomView(RESTfulView):
    def _get_data(self):
        """ Read json data from the post sent by some source """
        print('\n\n\n\n\n\n\n\n\n\n\n\n')
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
        registro = self.is_error(data)
        id_source = registro['id_source']
        registro.pop('id_source', None)
        registro['json_reg'] = json.loads(registro['json_reg'])
        chave_externa = registro['json_reg']['id_reg']
        registro['json_reg'].pop('id_reg', None)
        url = self.get_url_lightbase()
        r = requests.post(url, data=registro)
        id_reg = r.json()
        data = {
                'id_source':id_source,
                'id_reg':id_reg,
                'chave_externa':chave_externa
               }
        return data

    def get_url_lightbase(self): #TODO
        """ Returns url from config """
        domain = 'http://localhost/lbgenerator'
        base_name = 'WMI'
        url = domain + '/' + base_name + '/reg'
        return url

    def is_error(self,data): #TODO
        return data