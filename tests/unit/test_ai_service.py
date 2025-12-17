
def test_parse_transaction():
    service = AIService()
    result = service._parse_transaction("Trinta dólares para jantar")
    assert result["valor"] == 30
