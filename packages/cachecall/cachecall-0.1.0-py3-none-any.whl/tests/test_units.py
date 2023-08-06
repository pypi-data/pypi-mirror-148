from cachecall import kb, mb, gb


class TestsUnits:
    def test_kb(self):
        assert kb(1) == 1024
        assert kb(15) == 15360
        assert kb(52.5) == 53760.0

    def test_mb(self):
        assert mb(1) == 1048576
        assert mb(18) == 18874368
        assert mb(45.7) == 47919923.2

    def test_gb(self):
        assert gb(1) == 1073741824
        assert gb(13.8) == 14817637171.2
        assert gb(22) == 23622320128
