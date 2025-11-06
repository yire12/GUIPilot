"""
Test entity classes
"""
import pytest
import numpy as np
from guipilot.entities import Bbox, Widget, WidgetType, Screen


def test_bbox_creation():
    """Test Bbox creation and properties"""
    bbox = Bbox(10, 20, 100, 200)
    assert bbox.xmin == 10
    assert bbox.ymin == 20
    assert bbox.xmax == 100
    assert bbox.ymax == 200


def test_widget_creation():
    """Test Widget creation"""
    bbox = Bbox(0, 0, 100, 100)
    widget = Widget(type=WidgetType.Button, bbox=bbox)
    assert widget.type == WidgetType.Button
    assert widget.bbox == bbox


def test_screen_creation():
    """Test Screen creation"""
    image = np.zeros((1080, 1920, 3), dtype=np.uint8)
    widgets = {
        0: Widget(type=WidgetType.Button, bbox=Bbox(0, 0, 100, 100))
    }
    screen = Screen(image, widgets)
    assert screen.image.shape == (1080, 1920, 3)
    assert len(screen.widgets) == 1
    assert 0 in screen.widgets


def test_screen_creation_without_widgets():
    """Test Screen creation without widgets"""
    image = np.zeros((1080, 1920, 3), dtype=np.uint8)
    screen = Screen(image)
    assert screen.image.shape == (1080, 1920, 3)
    assert isinstance(screen.widgets, dict)

