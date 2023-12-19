import torchvision
import torch
from torch import nn

class MyResBck(torchvision.models.ResNet):
    def __init__(self, block, layers):
        super(MyResBck, self).__init__(block, layers)

    def forward(self, img, box):
      '''
      img : img tensor, (N, C, H, W)
      box : box coordinate, (x1, y1, x2, y2)
      '''
      x = self.conv1(img)
      x = self.bn1(x)
      x = self.relu(x)
      x = self.maxpool(x)

      x = self.layer1(x)
      x = self.layer2(x)
      x = self.layer3(x)

      max_img_size = max(img.size(2), img.size(3))
      layer4_max_size = max(x.size(2), x.size(3))
      spatial_scale = layer4_max_size/max_img_size

      x = torchvision.ops.roi_pool(x, box, 14, spatial_scale)
      x = self.layer4(x)
      x = self.avgpool(x)
      x = torch.flatten(x, 1)
      x = self.fc(x)

      return x

def _resnet(block, layers, weights, progress, num_classes, mode):
    '''
    block: BasicBlock or Bottleneck
    layers: block layer num order
    weights: pretrained model weights
    progress: False or True (displays a progress bar of the download to stderr)
    mode: whether last fc layer is new or not. True is new, False is not.
    '''

    model = MyResBck(block, layers)

    if weights is not None:
        model.load_state_dict(weights.get_state_dict(progress = progress, check_hash=True))

    if mode == True:

      model.fc = nn.Linear(512 * block.expansion, num_classes)

    else:
      model.fc.out_features = 8

    return model


def SimRes50(num_classes = 8, weights = None, progress = True, mode = False):

    weights = torchvision.models.ResNet50_Weights.DEFAULT
    Bottleneck = torchvision.models.resnet.Bottleneck

    return _resnet(Bottleneck, [3, 4, 6, 3], weights, progress, num_classes, mode)