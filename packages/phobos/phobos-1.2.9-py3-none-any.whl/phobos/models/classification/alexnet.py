from typing import Any
import logging

import torch
import torch.nn as nn

try:
    from torch.hub import load_state_dict_from_url
except ImportError:
    from torch.utils.model_zoo import load_url as load_state_dict_from_url


__all__ = ["alexnet"]


model_urls = {
    "alexnet-imagenet1k": "https://download.pytorch.org/models/alexnet-owt-7be5be79.pth"
}


class AlexNet(nn.Module):
    def __init__(
        self, 
        input: dict,
        output: dict,
        responses: dict,
        dropout: float = 0.5) -> None:
        assert len(input.keys()) == 1, logging.error("This AlexNet implementation only supports single input head")
        assert len(input[list(input.keys())[0]].dates) == 1, logging.error("This AlexNet implementation only supports single date input")
        assert len(output.keys()) == 1, logging.error("This AlexNet implementation only supports single output head")
        super().__init__()
        self.input = input
        self.output = output
        self.num_bands = len(self.input[list(self.input.keys())[0]].bands)
        self.num_classes = len(responses[output[list(output.keys())[0]].question].response_options)

        self.features = nn.Sequential(
            nn.Conv2d(self.num_bands, 64, kernel_size=11, stride=4, padding=2),
            nn.ReLU(inplace=True),
            nn.MaxPool2d(kernel_size=3, stride=2),
            nn.Conv2d(64, 192, kernel_size=5, padding=2),
            nn.ReLU(inplace=True),
            nn.MaxPool2d(kernel_size=3, stride=2),
            nn.Conv2d(192, 384, kernel_size=3, padding=1),
            nn.ReLU(inplace=True),
            nn.Conv2d(384, 256, kernel_size=3, padding=1),
            nn.ReLU(inplace=True),
            nn.Conv2d(256, 256, kernel_size=3, padding=1),
            nn.ReLU(inplace=True),
            nn.MaxPool2d(kernel_size=3, stride=2),
        )
        self.avgpool = nn.AdaptiveAvgPool2d((6, 6))
        self.classifier = nn.Sequential(
            nn.Dropout(p=dropout),
            nn.Linear(256 * 6 * 6, 4096),
            nn.ReLU(inplace=True),
            nn.Dropout(p=dropout),
            nn.Linear(4096, 4096),
            nn.ReLU(inplace=True),
            nn.Linear(4096, self.num_classes),
        )

    def forward(self, x: dict) -> dict:
        assert len(x.keys()) == len(self.input.keys()), logging.error("Input data does not have same number of head(s) as passed input dict during class intialization")
        assert x[list(x.keys())[0]].shape[1] == len(self.input[list(self.input.keys())[0]].dates), logging.error("Input data does not have same number of dates as passed in input dict during class initialization")
        assert x[list(x.keys())[0]].shape[2] == self.num_bands, logging.error("Input data does not have same number of bands as passed in input dict during class initialization")
        
        x = x[list(self.input.keys())[0]][:, 0, :, :, :]
        x = self.features(x)
        x = self.avgpool(x)
        x = torch.flatten(x, 1)
        x = self.classifier(x)
        x = {list(self.output.keys())[0]: x}
        
        return x

def alexnet(pretrained_weights: str = None, progress: bool = True, **kwargs: Any) -> AlexNet:
    r"""AlexNet model architecture from the
    `"One weird trick..." <https://arxiv.org/abs/1404.5997>`_ paper.
    The required minimum input size of the model is 63x63.
    Args:
        pretrained (bool): If True, returns a model pre-trained on ImageNet
        progress (bool): If True, displays a progress bar of the download to stderr
    """
    model = AlexNet(**kwargs)
    if pretrained_weights:
        state_dict = load_state_dict_from_url(model_urls[pretrained_weights], progress=progress)
        assert state_dict['features.0.weight'].shape[1] == model.num_bands, logging.error("This pretrained weights has different number of bands then specified in metadata.yaml")
        if state_dict['classifier.6.weight'].shape[0] != model.num_classes:
            del state_dict['classifier.6.weight']
            del state_dict['classifier.6.bias']

        model.load_state_dict(state_dict, strict=False)
    return model