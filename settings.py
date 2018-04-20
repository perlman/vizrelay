'''
Settings (default) management for viz redirection service.
'''

from argschema import ArgSchema, ArgSchemaParser
from argschema.fields import List, NumpyArray, Bool, Int, Nested, Str
from argschema.schemas import DefaultSchema
from argschema.utils import args_to_dict, smart_merge

DEFAULT_SETTINGS = {
    'neuroglancer' : {
        'base_url' : 'http://ibs-forrestc-ux1.corp.alleninstitute.org:8002',
        'blend' : 'additive'
    }
}

class NeuroglancerSchema(DefaultSchema):
    base_url = Str(default="https://neuroglancer-demo.appspot.com/", help="Neuroglancer URL", required=False)
    blend = Str(default="default", help="Default blend mode (default or additive)", required=False)


class VizRelaySchema(ArgSchema):
    neuroglancer = Nested(NeuroglancerSchema, required=True)

def get_settings(query_args):  # {'a.b.c.' : 'd'} {'--a.b.c}

    d = {}
    smart_merge(d, DEFAULT_SETTINGS)
    smart_merge(d, args_to_dict(query_args, schema=VizRelaySchema()))
    
    return ArgSchemaParser(input_data=d, schema_type=VizRelaySchema, args=[])
