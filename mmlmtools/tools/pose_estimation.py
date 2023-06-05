# Copyright (c) OpenMMLab. All rights reserved.
from mmengine import Registry
from mmpose.apis import MMPoseInferencer

from mmlmtools.toolmeta import ToolMeta
from ..utils.utils import get_new_image_name
from .base_tool import BaseTool


class HumanBodyPoseTool(BaseTool):
    DEFAULT_TOOLMETA = dict(
        tool_name='HumanBodyPoseTool',
        model='human',
        description='This is a useful tool '
        'when you want to draw or show the skeleton of human, '
        'or estimate the pose or keypoints of human in a photo.')

    def __init__(self,
                 toolmeta: ToolMeta = None,
                 input_style: str = 'image_path',
                 output_style: str = 'image_path',
                 remote: bool = False,
                 device: str = 'cuda'):
        super().__init__(toolmeta, input_style, output_style, remote, device)

        self.inferencer = None

    def setup(self):
        if self.inferencer is None:
            self.inferencer = MMPoseInferencer(
                self.toolmeta.model, device=self.device)

    def convert_inputs(self, inputs):
        if self.input_style == 'image_path':  # visual chatgpt style
            return inputs
        elif self.input_style == 'pil image':  # transformer agent style
            temp_image_path = get_new_image_name(
                'image/temp.jpg', func_name='temp')
            inputs.save(temp_image_path)
            return temp_image_path
        else:
            raise NotImplementedError

    def apply(self, inputs, **kwargs):
        if self.remote:
            raise NotImplementedError
        else:
            image_path = get_new_image_name(
                inputs, func_name='pose-estimation')
            with Registry('scope').switch_scope_and_registry('mmpose'):
                next(self.inferencer(inputs, vis_out_dir=image_path, **kwargs))
        return image_path

    def convert_outputs(self, outputs):
        if self.output_style == 'image_path':  # visual chatgpt style
            return outputs
        elif self.output_style == 'pil image':  # transformer agent style
            from PIL import Image
            outputs = Image.open(outputs)
            return outputs
        else:
            raise NotImplementedError
