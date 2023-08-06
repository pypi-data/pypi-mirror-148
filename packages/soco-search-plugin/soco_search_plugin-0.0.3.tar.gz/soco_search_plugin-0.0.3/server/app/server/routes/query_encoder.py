from fastapi import APIRouter, Body
from fastapi.encoders import jsonable_encoder
from server.app.server.models.data_manager import (
    PluginIn,
    PluginOut
)
from plugins.clip_plugin import CLIP
from plugin_class import PluginClass

router = APIRouter()
pc = PluginClass()


@router.post("/plugin_call", name="plugin_call")
def clip_text(x: PluginIn = Body(...)) :
    x = jsonable_encoder(x)
    return PluginOut(resp=pc(x["data"]))
