'''
Settings (default) management for viz redirection service.
'''
from argschema import ArgSchema, ArgSchemaParser
from argschema.fields import Nested, Str, Int
from argschema.schemas import DefaultSchema
from argschema.utils import args_to_dict, smart_merge

DEFAULT_SETTINGS = {}

class NeuroglancerSchema(DefaultSchema):
    base_url = Str(default="https://neuroglancer-demo.appspot.com/", help="Neuroglancer URL", required=False)
    blend = Str(default="default", help="Default blend mode (default or additive)", required=False)

class RenderSchema(DefaultSchema):
    protocol = Str(default="http", help="Protocol to connect to render with (http or https)", required=False)
    port = Int(default=80, required=False)

class VizRelaySchema(ArgSchema):
    neuroglancer = Nested(NeuroglancerSchema, required=False)
    render = Nested(RenderSchema, required=False)

def add_defaults(args):
    smart_merge(DEFAULT_SETTINGS, args)

def get_settings(query_args):
    d = {}
    smart_merge(d, DEFAULT_SETTINGS)
    smart_merge(d, args_to_dict(query_args, schema=VizRelaySchema()))
    
    return ArgSchemaParser(input_data=d, schema_type=VizRelaySchema, args=[])
