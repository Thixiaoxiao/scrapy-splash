# -*- coding: utf-8 -*-
from __future__ import absolute_import
import json

from hypothesis import given, assume
from hypothesis import strategies as st
from scrapy.http import Headers
from scrapy_splash.utils import headers_to_scrapy, fast_hash


def test_headers_to_scrapy():
    assert headers_to_scrapy(None) == Headers()
    assert headers_to_scrapy({}) == Headers()
    assert headers_to_scrapy([]) == Headers()

    html_headers = Headers({'Content-Type': 'text/html'})

    assert headers_to_scrapy({'Content-Type': 'text/html'}) == html_headers
    assert headers_to_scrapy([('Content-Type', 'text/html')]) == html_headers
    assert headers_to_scrapy([{'name': 'Content-Type', 'value': 'text/html'}]) == html_headers


_primitive = st.floats() | st.booleans() | st.text() | st.none() | st.integers()
_data = st.recursive(_primitive,
    lambda children: (
        children |
        st.lists(children) |
        st.tuples(children) |
        st.dictionaries(st.text(), children) |
        st.tuples(st.just('h'), children)
    ),
    max_leaves=5,
)


@given(_data, _data)
def test_fast_hash_different(val1, val2):
    def _dump(v):
        return json.dumps(v, sort_keys=True)
    assume(_dump(val1) != _dump(val2))
    assert fast_hash(val1) == fast_hash(val1)
    assert fast_hash(val1) != fast_hash(val2)

