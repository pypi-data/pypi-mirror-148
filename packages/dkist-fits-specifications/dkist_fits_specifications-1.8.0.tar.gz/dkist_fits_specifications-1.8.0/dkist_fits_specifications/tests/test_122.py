from dkist_fits_specifications.spec122 import load_raw_spec122, load_spec122
from dkist_fits_specifications.utils.frozendict import frozendict


def test_load_122():
    spec = load_spec122()
    assert isinstance(spec, frozendict)
    assert isinstance(spec["fits"], frozendict)
    assert isinstance(spec["fits"]["NAXIS"], frozendict)


def test_load_raw_122():
    spec = load_raw_spec122()
    assert isinstance(spec, frozendict)
    assert isinstance(spec["fits"], tuple)
    header, spec = spec["fits"]
    assert isinstance(header, frozendict)
    assert isinstance(spec["NAXIS"], frozendict)
