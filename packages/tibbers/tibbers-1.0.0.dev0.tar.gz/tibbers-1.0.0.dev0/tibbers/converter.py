from typing import Type, List, Dict, Any, Tuple, Iterable
import copy
import ast
import re

import torch
import torch.fx as fx
import torch.nn as nn
import torch.nn.functional as F

from .ops import convert_op

VALID_AST_TYPES = [int, float, bool, tuple, list, dict]

OPS_CLASS_LIST = [
    nn.Conv1d,
    nn.Conv2d,
    nn.ConvTranspose2d,
    nn.Linear,
    nn.MaxPool2d,
    nn.AdaptiveAvgPool2d,
    nn.Dropout2d,
    nn.BatchNorm1d,
    nn.BatchNorm2d,
    nn.LayerNorm,
    nn.Embedding,
    nn.Flatten,
]

OPS_FUNC_LIST = [
    F.conv1d,
    F.conv2d,
    torch.flatten,
]


def _parent_name(target: str) -> Tuple[str, str]:
    """
    Splits a qualname into parent path and last atom.
    For example, `foo.bar.baz` -> (`foo.bar`, `baz`)
    """
    *parent, name = target.rsplit(".", 1)
    return parent[0] if parent else "", name


def matches_module_pattern(pattern: Iterable[Type], node: fx.Node, modules: Dict[str, Any]):
    if len(node.args) == 0:
        return False
    if node.op != "call_module":
        return False
    if not isinstance(node.target, str):
        return False
    if node.target not in modules:
        return False
    for ops in pattern:
        if type(modules[node.target]) is ops:
            return True
    return False


def matches_function_pattern(pattern: Iterable[Any], node: fx.Node):
    if len(node.args) == 0:
        return False
    if node.op != "call_function":
        return False
    for ops in pattern:
        if node.target is ops:
            return True
    return False


# Parse string to kwargs
def parse_param_dict(extra_lines: List, kwargs: Dict):
    for i in range(0, len(extra_lines), 2):
        value = ast.literal_eval(extra_lines[i + 1])
        if type(value) in VALID_AST_TYPES:
            kwargs.update({extra_lines[i]: value})
        else:
            raise NotImplementedError
    return kwargs


def parse_params_repr(repr: str):
    args, kwargs = [], {}

    repr = repr.replace(" ", "")
    extra_lines = re.split(r",|=", repr)

    for i in range(len(extra_lines) - 1):
        if "(" in extra_lines[i] and ")" in extra_lines[i + 1]:
            ori_tuple_str = ",".join([extra_lines[i], extra_lines[i + 1]])
            extra_lines[i] = ori_tuple_str
            extra_lines[i + 1] = ""

    extra_lines = [i for i in extra_lines if i != ""]

    # Parse string to args
    for i, _ in enumerate(extra_lines):
        try:
            arg = ast.literal_eval(extra_lines[i])
            if type(arg) in VALID_AST_TYPES:
                args.append(arg)
            else:
                raise NotImplementedError
        except ValueError:
            kwargs = parse_param_dict(extra_lines[i:], kwargs)
            break

    return args, kwargs


def replace_node_module(node: fx.Node, modules: Dict[str, Any], new_module: torch.nn.Module):
    assert isinstance(node.target, str)
    parent_name, name = _parent_name(node.target)
    modules[node.target] = new_module
    setattr(modules[parent_name], name, new_module)


def flatten_replacement(x, dim_start):
    x = torch.flatten(x, dim_start + 1)
    return x.transpose(0, 1)


def check_flatten_rewrite(node: fx.Node, graph: fx.Graph):
    if str(node) == "flatten":
        with graph.inserting_after(node):
            new_node = graph.call_function(flatten_replacement, node.args, node.kwargs)
            node.replace_all_uses_with(new_node)
        graph.erase_node((node))


def model_fuse(model: torch.nn.Module, B: int = 1, inplace=False) -> torch.nn.Module:
    """
    Fuses convolution/BN layers for inference purposes. Will deepcopy your
    model by default, but can modify the model inplace as well.
    """
    if not inplace:
        model = copy.deepcopy(model)
    fx_model = fx.symbolic_trace(model)
    modules = dict(fx_model.named_modules())
    new_graph = copy.deepcopy(fx_model.graph)

    for node in new_graph.nodes:
        if matches_module_pattern(OPS_CLASS_LIST, node, modules):
            repr = modules[node.target].extra_repr()
            args, kwargs = parse_params_repr(repr)
            group_op = convert_op(type(modules[node.target]), B)(*args, **kwargs)
            # with new_graph.inserting_after(node):
            #     node.replace_all_uses_with(group_op)
            # new_graph.erase_node((node))
            replace_node_module(node, modules, group_op)
            fx_model.delete_all_unused_submodules()

        if matches_function_pattern(OPS_FUNC_LIST, node):
            check_flatten_rewrite(node, new_graph)
    new_graph.lint()
    fx_model.recompile()
    return fx.GraphModule(fx_model, new_graph)


# model = models.resnet18()
# model.eval()

# fx_model: fx.GraphModule = fx.symbolic_trace(model)
# modules = dict(fx_model.named_modules())
# # print(fx_model.named_modules())
# fmodel = model_fuse(model, B=2)
# print(fmodel.graph)
# print(fx_model.graph)


# print(node.args, node.kwargs)

# torch.testing.assert_allclose(new_output, torch.nn.LeakyReLU()(orig_output))


# ShapeProp? vmap example?

# from torch.fx import replace_pattern?  replace_pattern(traced, pattern, replacement)

