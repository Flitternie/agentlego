from agentlego.types import Annotated, ImageIO, Info
from agentlego.utils import load_or_build_object, require
from ..base import BaseTool


class TextToBbox(BaseTool):
    """A tool to detection the given object.

    Args:
        model (str): The model name used to detect texts.
            Which can be found in the ``MMDetection`` repository.
            Defaults to ``glip_atss_swin-t_a_fpn_dyhead_pretrain_obj365``.
        device (str): The device to load the model. Defaults to 'cpu'.
        toolmeta (None | dict | ToolMeta): The additional info of the tool.
            Defaults to None.
    """

    default_desc = ('The tool can detect the object location according to '
                    'description.')

    @require('mmdet>=3.1.0')
    def __init__(self,
                 model: str = 'glip_atss_swin-t_b_fpn_dyhead_pretrain_obj365',
                 device: str = 'cuda',
                 toolmeta=None):
        super().__init__(toolmeta=toolmeta)
        self.model = model
        self.device = device

    def setup(self):
        from mmdet.apis import DetInferencer
        self._inferencer = load_or_build_object(
            DetInferencer, model=self.model, device=self.device)
        self._visualizer = self._inferencer.visualizer

    def apply(
        self,
        image: ImageIO,
        text: Annotated[str, Info('The object description in English.')],
    ) -> Annotated[str,
                   Info('Detected objects, include bbox in '
                        '(x1, y1, x2, y2) format, and detection score.')]:
        from mmdet.structures import DetDataSample

        results = self._inferencer(
            image.to_array()[:, :, ::-1],
            texts=text,
            return_datasamples=True,
        )
        data_sample = results['predictions'][0]
        preds: DetDataSample = data_sample.pred_instances

        return preds

