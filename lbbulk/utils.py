# -*- coding: utf-8 -*-
__author__ = 'eduardo'

import json
from decimal import *


class DecimalEncoder(json.JSONEncoder):
    """
    Adiciona conversão de decimais no JSON
    """
    def default(self, obj):
        """Convert ``obj`` to something JSON encoder can handle."""

        if isinstance(obj, Decimal):
            obj = int(obj)
        else:
            # method to generate JSON
            obj = obj._encoded()

        return obj