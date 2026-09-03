def test_auth_module_import():
    from backend.app.api.routes import auth
    assert auth.router is not None
