import json
import os

import pandas as pd
import requests
from IPython.core.magic import Magics, line_cell_magic, magics_class, needs_local_scope
from requests.exceptions import ConnectionError

from .parse import convert_local_ns, is_url

DEFAULT_API_URL = "http://localhost:8000/api/v1/query"


@magics_class
class ThanosMagic(Magics):
    @needs_local_scope
    @line_cell_magic
    def thanosql(self, line=None, cell=None, local_ns={}):
        if not os.getenv("API_URL"):
            os.environ["API_URL"] = DEFAULT_API_URL

        if line:
            # api url change for debugging
            if is_url(line):
                os.environ["API_URL"] = line
                print(f"API URL is changed to {line}")
                return

            # 'line' will treat as same as 'cell'
            else:
                cell = line

        if not cell:
            return

        query_string = convert_local_ns(cell, local_ns)

        data = {"query_string": query_string}
        try:
            res = requests.post(os.getenv("API_URL"), data=json.dumps(data))
        except ConnectionError as e:
            print(e)
            print("\nThanoSQL Engine is not ready for connection.")
            return

        if res.status_code == 200:
            data = res.json()
            query_result = data.get("final_result")
            if query_result:
                df = pd.read_json(query_result, orient="columns")
                return df
        else:
            return res


# In order to actually use these magics, you must register them with a
# running IPython.
def load_ipython_extension(ipython):
    """Load the extension in IPython."""
    ipython.register_magics(ThanosMagic)
