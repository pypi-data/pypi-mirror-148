"""
Hoodat components
"""
import os

try:
    from kfp.v2.components import load_component_from_file
except ImportError:
    from kfp.components import load_component_from_file

__all__ = ["AddPyOp", "MakeCascadeFileOp", "VideoToFramesOp"]

AddPyOp = load_component_from_file(
    os.path.join(os.path.dirname(__file__), "add_py/component.yaml")
)

MakeCascadeFileOp = load_component_from_file(
    os.path.join(os.path.dirname(__file__), "make_cascade_file/component.yaml")
)

VideoToFramesOp = load_component_from_file(
    os.path.join(os.path.dirname(__file__), "video_to_frames/component.yaml")
)
