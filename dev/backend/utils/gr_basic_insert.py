""" basic data """
import traceback
from eve.methods.post import post_internal
from flask import current_app as app
from basic_data import DATA

# pylint: disable=broad-except
def insert_basic_data():
    """ Insert basic data """
    with app.test_request_context():
        for config in DATA:
            for item in config['data']:
                try:
                    relation = config.get('relation', None)
                    if relation:
                        relation_config = item[relation]
                        result = app.data.pymongo().db[relation_config['reference']].find_one({
                            relation_config['field_search']: relation_config['value']
                        })
                        if result:
                            item[relation] = result[relation_config['field_value']]
                    result_find = app.data.find_one_raw(config['resource'],
                                                        **{config['field']: item[config['field']]})
                    if not result_find:
                        post_internal(config['resource'], item)
                except Exception:
                    traceback.print_exc()
