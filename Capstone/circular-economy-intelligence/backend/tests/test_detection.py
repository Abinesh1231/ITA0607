def test_detection_module_import():
    from backend.app.services.detection_service import detect_objects
    assert callable(detect_objects)
