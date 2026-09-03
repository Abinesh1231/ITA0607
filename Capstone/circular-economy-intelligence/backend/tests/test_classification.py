def test_classification_module_import():
    from backend.app.services.classification_service import classify_image
    assert callable(classify_image)
