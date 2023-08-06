from typing import Optional

import pytest

from sym.sdk.resource import (
    SRN,
    InvalidSlugError,
    InvalidSRNError,
    MultipleErrors,
    SymResource,
    TrailingSeparatorError,
)


class MockSymResource(SymResource):
    """This is a test class for SymResource behavior."""


class TestResource:
    def test_sym_resource_fails_on_malformed_srn(self):
        self._test_bad("foo", InvalidSRNError)
        self._test_bad("foo:bar", InvalidSRNError)
        self._test_bad("foo:bar:baz", InvalidSRNError)
        self._test_bad("foo:bar:baz:boz", InvalidSRNError)
        self._test_bad("foo:bar:baz:lates:", TrailingSeparatorError, match="trailing separator.")
        self._test_bad("foo:bar:baz:1.0:", InvalidSRNError)
        self._test_bad("foo:bar:baz:1.0.0::", InvalidSRNError)
        self._test_bad("foo:bar:baz:latest:1.0.0:", TrailingSeparatorError)
        self._test_bad("foo:bar:baz:1.3000.0:something", InvalidSRNError)
        self._test_bad("foo:bar:baz::something", InvalidSRNError)
        self._test_bad("foo:bar:baz:latestsomething", InvalidSRNError)
        self._test_bad("foo:bar:baz:latest:", TrailingSeparatorError)
        self._test_bad("foo!foobar:bar::baz:latest:foo", InvalidSlugError, match="org")
        self._test_bad("sym:flow:something::", InvalidSRNError)
        self._test_bad("foo!foobar:bar:baz:1000.0.2000:foo", MultipleErrors, match="version")

    def _test_bad(self, srn, exc, match: str = None):
        if match:
            with pytest.raises(exc, match=match):
                SRN.parse(srn)
        else:
            with pytest.raises(exc):
                SRN.parse(srn)

    def test_sym_srn_succeeds_on_valid_srn(self):
        self._test_good(
            "sym:foo-bar::12345-11233:0.1.0:stuff",
            "sym",
            "foo-bar",
            None,
            "12345-11233",
            "0.1.0",
            "stuff",
        )
        self._test_good(
            "foo:bar::baz:1.300.0:something", "foo", "bar", None, "baz", "1.300.0", "something"
        )
        self._test_good("foo:bar::baz:latest", "foo", "bar", None, "baz", "latest", None)
        self._test_good("foo_foo:bar::baz:latest", "foo_foo", "bar", None, "baz", "latest", None)
        self._test_good(
            "sym:template::approval:1.0.0", "sym", "template", None, "approval", "1.0.0", None
        )
        self._test_good(
            "sym:template::approval:1.0.0:e97af6b3-0249-4855-971f-4e1dd188773a",
            "sym",
            "template",
            None,
            "approval",
            "1.0.0",
            "e97af6b3-0249-4855-971f-4e1dd188773a",
        )
        self._test_good(
            "sym:integration:slack:my-integration:latest",
            "sym",
            "integration",
            "slack",
            "my-integration",
            "latest",
            None,
        )

    def _test_good(
        self,
        raw,
        org: str,
        model: str,
        model_type: Optional[str],
        slug: str,
        version: str,
        identifier: Optional[str],
    ):
        srn = SRN.parse(raw)
        assert srn.organization == org
        assert srn.model == model
        assert srn.type == model_type
        assert srn.slug == slug
        assert srn.version == version
        assert srn.identifier == identifier

    def test_srn_copy_should_succeed_without_identifier(self):
        srn_string = "foo:bar::baz:1.0.0"

        srn = SRN.parse(srn_string)

        assert str(srn.copy(version="latest")) == "foo:bar::baz:latest"
        assert str(srn.copy(organization="myorg")) == "myorg:bar::baz:1.0.0"

    def test_srn_str_should_produce_an_identical_srn(self):
        text = "sym:template::approval:1.0.0"
        srn = SRN.parse(text)

        srn_str = str(srn)
        srn2 = SRN.parse(srn_str)

        assert srn == srn2
        assert str(srn) == str(srn2)
        assert text == srn_str

    def test_sym_resource_srn_getattr_fallback(self):
        srn = SRN.parse("test:mock::slug:latest:12345")
        resource = MockSymResource(srn=srn)

        assert resource.srn == srn
        assert resource.name == srn.slug
        assert resource.organization == srn.organization
        assert resource.identifier == srn.identifier

    def test_sym_resource_srn_getattr_errors(self):
        srn = SRN.parse("test:mock::slug:latest:12345")
        resource = MockSymResource(srn=srn)

        # Ensure a normal missing attribute errors properly.
        with pytest.raises(AttributeError, match="no attribute 'nope'"):
            resource.nope

        # Delete the attributes so the __getattr__ override should fall back,
        # but we want to ensure it doesn't infinitely recurse.
        delattr(resource, "_srn")
        with pytest.raises(AttributeError, match="no attribute 'srn"):
            resource.srn
