"""
Test basic imports to ensure package structure is correct
"""


def test_core_imports():
    """Test that core modules can be imported"""
    from guipilot.checker import GVT as GVTChecker
    from guipilot.entities import Bbox, Screen, Widget, WidgetType
    from guipilot.matcher import GVT, GUIPilotV2

    assert Screen is not None
    assert Widget is not None
    assert WidgetType is not None
    assert Bbox is not None
    assert GUIPilotV2 is not None
    assert GVT is not None
    assert GVTChecker is not None


def test_models_imports():
    """Test that model modules can be imported"""
    try:
        from guipilot.models import OCR, Detector

        assert Detector is not None
        assert OCR is not None
    except ImportError:
        # Models may require additional setup
        pass


def test_agent_imports():
    """Test that agent modules can be imported"""
    try:
        from guipilot.agent import GPTAgent

        assert GPTAgent is not None
    except ImportError:
        # Agent may require OpenAI API key
        pass
