def test_import():
    try:
        import alto2txt  # noqa F401

        assert True
    except ImportError:
        assert False
