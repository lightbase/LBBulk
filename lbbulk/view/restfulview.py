from pyramid_restler.view import RESTfulView
import json

class RegCustomView(RESTfulView):
    def get_member(self):
        id = self.request.matchdict['id']
        json_reg = self.requests.params['json_reg']
        json_reg = json.loads(json_reg)
        ins = registro.insert().values(chave_externa=json_reg['id_reg'])
        member = self.context.get_member(id)
        return self.render_to_response(member)