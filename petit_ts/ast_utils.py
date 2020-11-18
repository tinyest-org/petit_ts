import ast
import inspect
from typing import Optional, Any

import executing

NAME_TOKEN = '__petit_name__'


class AstFailure(Exception):
    ...


# TODO: make a custom type that reflects the added functionnalities
ExtendedBasicTypeHint = Any

def get_extended_name(item: ExtendedBasicTypeHint) -> Optional[str]:
    if hasattr(item, NAME_TOKEN):
        return item.__dict__[NAME_TOKEN]
    else:
        return None


def set_extended_name(item: ExtendedBasicTypeHint, name: Optional[str]) -> None:
    if name is not None:
        item.__dict__[NAME_TOKEN] = name


def get_parent_assign(node: ast.AST) -> ast.Assign:
    """Look for an ast.Assign node in the parents"""
    while hasattr(node, 'parent'):
        node = node.parent

        if isinstance(node, ast.Assign):
            return node
    raise Exception(
        'Failed to retrieve the variable name.'
    )


def get_variable_name(with_raise: bool = True) -> Optional[str]:
    # TODO: maybe should handle depth, number of f_back
    frame = inspect.currentframe().f_back.f_back
    node = executing.Source.executing(frame).node
    try:
        assignment = get_parent_assign(node)
    except:
        return None
    if len(assignment.targets) > 1:
        if with_raise:
            raise AstFailure(
                f"Too many assignments is not supported {ast.dump(assignment)}")
        return None
    target = assignment.targets[0]
    if isinstance(target, ast.Name):
        return target.id
    if isinstance(target, ast.Attribute):
        return target.attr
    if with_raise:
        raise AstFailure(
            f"Can only get name of a variable or attribute, not {ast.dump(assignment)}"
        )
    return None
