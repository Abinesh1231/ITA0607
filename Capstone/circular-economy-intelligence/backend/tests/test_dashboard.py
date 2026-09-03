def test_dashboard_module_import():
    from backend.app.database.crud import dashboard_stats
    assert callable(dashboard_stats)
