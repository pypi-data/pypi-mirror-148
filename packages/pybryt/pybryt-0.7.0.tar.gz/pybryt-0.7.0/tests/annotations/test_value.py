"""Tests for value annotations"""

import pytest

from itertools import chain
from unittest import mock

from pybryt import Annotation, Attribute, debug_mode, InitialCondition, ReturnValue, structural, \
    Value
from pybryt import invariants as inv
from pybryt.annotations.structural import _StructuralPattern
from pybryt.execution.memory_footprint import Event, MemoryFootprint, MemoryFootprintValue
from pybryt.utils import pickle_and_hash

from .structural_helpers import AttrContainer
from .utils import assert_object_attrs, generate_memory_footprint


def test_value_annotation():
    """
    """
    # TODO: create pytest fixtures that do these automatically
    footprint = generate_memory_footprint()
    Annotation.reset_tracked_annotations()

    seen = {}
    for mfp_val in footprint:
        v = Value(mfp_val.value)
        res = v.check(footprint)

        assert repr(res) == "AnnotationResult(satisfied=True, annotation=pybryt.Value)"

        h = pickle_and_hash(mfp_val.value)

        # check attributes of BeforeAnnotation and AnnotationResult
        assert_object_attrs(v, {"children__len": 0})
        assert_object_attrs(res, {
            "children": [],
            "satisfied": True,
            "_satisfied": True,
            "annotation": v,
            "timestamp": seen[h] if h in seen else mfp_val.timestamp,
            "value": mfp_val.value,
        })

        if h not in seen:
            seen[h] = mfp_val.timestamp

    v = Value(-1)  # does not occur in footprint
    res = v.check(footprint)

    assert v.to_dict() == {
        "name": "Annotation 11",
        "children": [],
        "success_message": None,
        "failure_message": None,
        "limit": None,
        "group": None,
        "invariants": [],
        "atol": None,
        "rtol": None,
        "type": "value",
    }
    assert repr(res) == "AnnotationResult(satisfied=False, annotation=pybryt.Value)"

    # check __repr__
    assert repr(v) == "pybryt.Value", "wrong __repr__"

    # check attributes of BeforeAnnotation and AnnotationResult
    assert_object_attrs(v, {"children__len": 0})
    assert_object_attrs(res, {
        "children": [],
        "satisfied": False,
        "_satisfied": False,
        "annotation": v,
        "timestamp": -1,
        "value": None,
    })

    # test pickling error
    with mock.patch("dill.dumps") as mocked_dumps:
        mocked_dumps.side_effect = Exception()
        with pytest.raises(ValueError):
            v = Value(-1)

    # test with invariants
    s = footprint.get_value(-1).value
    v = Value(s.upper(), invariants=[inv.string_capitalization])
    res = v.check(footprint)
    assert res.satisfied

    # test that check_against correctly calls check
    with mock.patch.object(v, "check") as mocked_check:
        mocked_check.return_value = mock.MagicMock()
        mocked_check.return_value.satisfied = True
        assert v.check_against(s.lower())
        mocked_check.assert_called_with(MemoryFootprint.from_values(MemoryFootprintValue(s.lower(), 0, None)))

    # check custom equivalence function
    mocked_eq = mock.MagicMock()
    v = Value(s, equivalence_fn=mocked_eq)
    mocked_eq.return_value = False
    assert not v.check_against("foo")
    mocked_eq.assert_called_with(s, "foo")
    mocked_eq.return_value = True
    assert v.check_against("")
    mocked_eq.assert_called_with(s, "")
    mocked_eq.side_effect = ValueError()
    assert not v.check_against("")

    # check for invalid return type error
    mocked_eq.return_value = 1
    mocked_eq.side_effect = None
    with pytest.raises(TypeError, match=f"Custom equivalence function returned value of invalid type: {type(1)}"):
        v.check_against(1)

    # check debug mode errors
    with debug_mode():
        with pytest.raises(ValueError, match="Absolute or relative tolerance specified with an equivalence function"):
            Value(1, atol=1e-5, equivalence_fn=lambda x, y: True)

        with pytest.raises(ValueError, match="Absolute or relative tolerance specified with an equivalence function"):
            Value(1, rtol=1e-5, equivalence_fn=lambda x, y: True)

        class FooError(Exception):
            pass

        with pytest.raises(FooError):
            def raise_foo(x, y):
                raise FooError()

            v = Value(1, equivalence_fn=raise_foo)
            v.check_against(1)


def test_attribute_annotation():
    """
    """
    footprint = generate_memory_footprint()
    Annotation.reset_tracked_annotations()
    val, ts = footprint.get_value(0).value, footprint.get_value(0).timestamp

    v = Attribute(val, "T")
    res = v.check(footprint)

    # check attributes of BeforeAnnotation and AnnotationResult
    assert_object_attrs(v, {"children__len": 1})
    assert_object_attrs(res, {
        "children__len": 1,
        "satisfied": True,
        "_satisfied": None,
        "annotation": v,
        "timestamp": -1,
        "satisfied_at": ts,
        "value": val,
    })

    assert v.to_dict() == {
        "name": "Annotation 2",
        "children": [
            {
                'name': 
                'Annotation 1', 
                'group': None, 
                'limit': None, 
                'success_message': None, 
                'failure_message': None, 
                'children': [], 
                'invariants': [], 
                'atol': None,
                'rtol': None,
                "type": None,
            }
        ],
        "success_message": None,
        "failure_message": None,
        "limit": None,
        "group": None,
        "invariants": [],
        "atol": None,
        "rtol": None,
        "type": "attribute",
        "attributes": ['T'],
        "enforce_type": False,
    }

    # test that check_against correctly calls check
    with mock.patch.object(v, "check") as mocked_check:
        mocked_check.return_value = mock.MagicMock()
        mocked_check.return_value.satisfied = False
        assert not v.check_against(val)
        mocked_check.assert_called_with(MemoryFootprint.from_values(MemoryFootprintValue(val, 0, None)))

    # check enforce type
    class Foo:
        T = val.T

    footprint2 = MemoryFootprint.from_values(MemoryFootprintValue(Foo(), 1, None))
    res = v.check(footprint2)
    assert res.satisfied

    v = Attribute(val, "T", enforce_type=True)
    res = v.check(footprint2)
    assert not res.satisfied

    footprint3 = MemoryFootprint.from_values(*chain(footprint, footprint2))
    res = v.check(footprint3)
    assert res.satisfied

    # check error raising
    with pytest.raises(TypeError):
        Attribute(val, ["T", 1])
    
    with pytest.raises(TypeError):
        Attribute(val, 1)

    with pytest.raises(AttributeError):
        Attribute(val, "foo")


def test_return_value():
    """
    Tests for the ``ReturnValue`` annotation.
    """
    rv = ReturnValue(1)
    footprint = MemoryFootprint.from_values(
        MemoryFootprintValue(1, 0, Event.RETURN),
        MemoryFootprintValue(2, 1, Event.LINE_AND_RETURN),
    )

    res = rv.check(footprint)
    assert_object_attrs(res, {
        "children": [],
        "satisfied": True,
        "_satisfied": True,
        "annotation": rv,
        "timestamp": 0,
        "value": 1,
    })

    footprint = MemoryFootprint.from_values(
        MemoryFootprintValue(1, 0, Event.LINE_AND_RETURN),
        MemoryFootprintValue(2, 1, Event.RETURN),
    )

    res = rv.check(footprint)
    assert_object_attrs(res, {
        "children": [],
        "satisfied": True,
        "_satisfied": True,
        "annotation": rv,
        "timestamp": 0,
        "value": 1,
    })

    footprint = MemoryFootprint.from_values(
        MemoryFootprintValue(1, 0, Event.LINE),
        MemoryFootprintValue(2, 1, Event.RETURN),
    )

    res = rv.check(footprint)
    assert_object_attrs(res, {
        "children": [],
        "satisfied": False,
        "_satisfied": False,
        "annotation": rv,
        "timestamp": -1,
        "value": None,
    })


def test_initial_conditions():
    """
    Tests for the use of initial conditions with value annotations.
    """
    name = "foo"
    ic = InitialCondition(name)

    val, offset = 2, 3
    v = Value(ic + offset)

    fp = MemoryFootprint.from_values(MemoryFootprintValue(val + offset, 0, None))
    fp.set_initial_conditions({name: val})

    res = v.check(fp)
    assert res.satisfied
    assert res.satisfied_at == 0
    assert res.value == val + offset

    ic2 = InitialCondition(name)
    v1, v2 = Value(ic, name="baz"), Value(ic2, name="baz")
    assert v1 == v2
    
    ic2 = InitialCondition("bar")
    v2 = Value(ic2, name="baz")
    assert v1 != v2

    # test errors
    with pytest.raises(ValueError, match="check_against cannot be used with initial conditions"):
        v.check_against(val + offset)

    with pytest.raises(TypeError, match="Initial conditions are not compatible with attribute annotations"):
        Attribute(ic, "foo")


def test_structural_patterns():
    """
    Tests for the using structural patterns with value annotations.
    """
    expected_attrs = dict(a=1, b=2, c=3)
    pat = structural.tests.annotations.structural_helpers.AttrContainer(**expected_attrs)
    v = Value(pat)
    with mock.patch.object(_StructuralPattern, "__eq__") as mocked_eq:
        obj = AttrContainer(**expected_attrs)
        v.check_against(obj)
        mocked_eq.assert_called_with(obj)
