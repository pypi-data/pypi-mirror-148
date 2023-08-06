# AUTO GENERATED FILE - DO NOT EDIT

from dash.development.base_component import Component, _explicitize_args


class DashReactFlow(Component):
    """A DashReactFlow component.


Keyword arguments:

- id (string; optional):
    The ID used to identify this component in Dash callbacks.

- NodeClicked (dict; optional):
    called when user clicks a node.

- attributionPosition (string; optional)

- className (string; optional)

- defaultPosition (list of numbers; optional)

- defaultZoom (number; optional)

- draggable (boolean; default False):
    are the node and its edges draggable.

- edges (list of dicts; optional):
    array of edges (for an controlled flow).

- maxZoom (number; optional)

- minZoom (number; optional)

- nodes (list of dicts; optional):
    array of nodes (for an controlled flow).

- onlyRenderVisibleElements (boolean; optional)

- preventScrolling (boolean; optional)

- snapGrid (list of numbers; optional)

- snapToGrid (boolean; optional)

- style (dict; default {height:500,width:500}):
    style."""
    @_explicitize_args
    def __init__(self, id=Component.UNDEFINED, nodes=Component.UNDEFINED, edges=Component.UNDEFINED, NodeClicked=Component.UNDEFINED, draggable=Component.UNDEFINED, style=Component.UNDEFINED, className=Component.UNDEFINED, minZoom=Component.UNDEFINED, maxZoom=Component.UNDEFINED, defaultZoom=Component.UNDEFINED, defaultPosition=Component.UNDEFINED, snapGrid=Component.UNDEFINED, snapToGrid=Component.UNDEFINED, onlyRenderVisibleElements=Component.UNDEFINED, preventScrolling=Component.UNDEFINED, attributionPosition=Component.UNDEFINED, **kwargs):
        self._prop_names = ['id', 'NodeClicked', 'attributionPosition', 'className', 'defaultPosition', 'defaultZoom', 'draggable', 'edges', 'maxZoom', 'minZoom', 'nodes', 'onlyRenderVisibleElements', 'preventScrolling', 'snapGrid', 'snapToGrid', 'style']
        self._type = 'DashReactFlow'
        self._namespace = 'dash_react_flow'
        self._valid_wildcard_attributes =            []
        self.available_properties = ['id', 'NodeClicked', 'attributionPosition', 'className', 'defaultPosition', 'defaultZoom', 'draggable', 'edges', 'maxZoom', 'minZoom', 'nodes', 'onlyRenderVisibleElements', 'preventScrolling', 'snapGrid', 'snapToGrid', 'style']
        self.available_wildcard_properties =            []
        _explicit_args = kwargs.pop('_explicit_args')
        _locals = locals()
        _locals.update(kwargs)  # For wildcard attrs
        args = {k: _locals[k] for k in _explicit_args if k != 'children'}
        for k in []:
            if k not in args:
                raise TypeError(
                    'Required argument `' + k + '` was not specified.')
        super(DashReactFlow, self).__init__(**args)
