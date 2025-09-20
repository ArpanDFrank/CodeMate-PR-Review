from pr_agent import connectors

def test_connect():
    assert connectors.connect("dummy_repo") is None
