from pyramid_restler.view import RESTfulView
import json

class RegCustomView(RESTfulView):
    def _get_data(self):
        content_type = self.request.content_type
        if content_type == 'application/json':
            data = json.loads(self.request.body)
        elif content_type == 'application/x-www-form-urlencoded':
            data = dict(self.request.POST)
        else:
            data = self.request.params
        data = data['json_reg']
        return data