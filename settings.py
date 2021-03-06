'''
Settings (default) management for viz redirection service.
'''
from argschema import ArgSchema, ArgSchemaParser
from argschema.fields import Boolean, Nested, Str, Int, Float, Dict
from argschema.schemas import DefaultSchema
from argschema.utils import args_to_dict, smart_merge
import marshmallow as mm

DEFAULT_SETTINGS = {}


class NeuroglancerDefaultOptions(DefaultSchema):
    blend = Str(default="default",
                validate=mm.validate.OneOf(['default', 'additive']),
                description="Default blend mode (default or additive)",
                required=False)
    layout = Str(validate=mm.validate.OneOf(['xy',
                                             'yz',
                                             'xy-3d',
                                             'yz-3d',
                                             'yz-3d',
                                             '4panel',
                                             '3d']),
                 description="default layout")


class NeuroglancerLayerOptions(DefaultSchema):
    opacity = Float(validate=mm.validate.Range(0, 1),
                    description="default opacity of layers")
    blend = Str(default="default",
                validate=mm.validate.OneOf(['default', 'additive']),
                description="Blend mode for this each layer created",
                required=False)
    shader = Str(description="shader to use")


class NeuroglancerSchema(DefaultSchema):
    base_url = Str(default="https://neuroglancer-demo.appspot.com/",
                   description="Neuroglancer URL", required=False)
    options = Nested(NeuroglancerDefaultOptions, default={})
    layer_options = Nested(NeuroglancerLayerOptions, default={})


class RenderSchema(DefaultSchema):
    protocol = Str(
        default="http",
        help="Protocol to connect to render with (http or https)",
        required=False)
    port = Int(default=80, required=False)
    encoding = Str(
        default="jpg",
        help="Encoding option for the neuroglancer render datasource (jpg or raw16)",
        required=False)
    all_channels = Boolean(default=False,
        help="Use Render API to query for and load all channels",
        required=False)
    alt_render = Str(
        default="",
        help="Alternate render host to use for vizrelay API calls [to work in Docker]",
        required=False)
    enable_one_channel = Boolean(default=False,
        help="Enable only one of the channels",
        required=False)
    channel_name_shader_sub = Dict(default={},
        help="Dictionary of CHANNEL_NAME : { SUB_NAME : SUB_VALUE }",
        required=False)



class VizRelaySchema(ArgSchema):
    neuroglancer = Nested(NeuroglancerSchema, required=False, default={})
    render = Nested(RenderSchema, required=False, default={})


def add_defaults(args):
    smart_merge(DEFAULT_SETTINGS, args)


def get_settings(query_args):
    d = {}
    smart_merge(d, DEFAULT_SETTINGS)
    smart_merge(d, args_to_dict(query_args, schema=VizRelaySchema()))

    return ArgSchemaParser(input_data=d, schema_type=VizRelaySchema, args=[])
