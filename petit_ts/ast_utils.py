import ast
import inspect
from typing import Any, Optional, Union, get_origin
import executing


class AstFailure(Exception):
    ...


class TooManyAssignments(Exception):
    ...


def get_parent_assign(node: ast.AST) -> ast.Assign:
    """Look for an ast.Assign node in the parents"""
    while hasattr(node, 'parent'):
        node = node.parent

        if isinstance(node, ast.Assign):
            return node
    raise AstFailure(
        'Failed to retrieve the variable name.'
    )


def get_variable_name(with_raise: bool = True) -> Optional[str]:
    # TODO: maybe should handle depth, number of f_back
    frame = inspect.currentframe().f_back.f_back
    node = executing.Source.executing(frame).node
    try:
        assignment = get_parent_assign(node)
    except AstFailure as e:
        if with_raise:
            raise e
        else:
            return None
    target = assignment.targets[0]
    if isinstance(target, ast.Name):
        return target.id
    if isinstance(target, ast.Tuple):
        raise TooManyAssignments(
            f"Can only work with one assignment"
        )
    if with_raise:
        raise AstFailure(
            f"Can only get name of a variable or attribute, not {ast.dump(assignment)}"
        )
    return None
