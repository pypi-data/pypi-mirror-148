import json
from typing import Any, Dict

import ipywidgets
import traitlets.traitlets as t

from ._version import __version__


class GoslingWidget(ipywidgets.DOMWidget):
    _model_name = t.Unicode("GoslingModel").tag(sync=True)
    _model_module = t.Unicode("gosling-widget").tag(sync=True)
    _model_module_version = t.Unicode(__version__).tag(sync=True)

    _view_name = t.Unicode("GoslingView").tag(sync=True)
    _view_module = t.Unicode("gosling-widget").tag(sync=True)
    _view_module_version = t.Unicode(__version__).tag(sync=True)

    _viewconf = t.Unicode("null").tag(sync=True)

    # readonly properties
    location = t.List(t.Union([t.Float(), t.Tuple()]), read_only=True).tag(sync=True)

    def __init__(self, viewconf: Dict[str, Any], **kwargs):
        super().__init__(_viewconf=json.dumps(viewconf), **kwargs)

    def zoom_to(self, view_id: str, pos: str, padding: float = 0, duration: int = 1000):
        msg = json.dumps(["zoomTo", view_id, pos, padding, duration])
        self.send(msg)
