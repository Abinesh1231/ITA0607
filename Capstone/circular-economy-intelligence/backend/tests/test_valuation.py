def test_valuation():
    from backend.app.services.valuation_service import estimate_value
    result = estimate_value("plastic", 1.0, 1.0)
    assert result["estimated_value"] >= 0
