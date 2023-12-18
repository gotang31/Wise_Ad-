import torch
import torchvision
from torchvision import transforms
from torch import nn

class SimBck: # Similairty Backbone = Resnet50
    def __init__(self,
                dir = False,
                model = torchvision.models.resnet50(weights = torchvision.models.ResNet50_Weights.DEFAULT),
                model_weights = torchvision.models.ResNet50_Weights.DEFAULT):
        '''
        dir : file directory of fine-tuned model state_dict. Default is pre-trained model
        model : pretrained model, resnet50(ImageNet_V2)
        model_weights : weights of pretrained model
        '''
        self.model = model
        self.weights = model_weights
        self.transform = self.assign_transform()
        self.device = self.set_device()

        if dir:
            self.model.load_state_dict(torch.load(dir, map_location='cpu'))
        else:
            pass

    def assign_transform(self):
        preprocess = transforms.Compose([transforms.ToTensor(),
                                        transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225])])

        return preprocess

    def set_device(self):
        if torch.cuda.is_available():
            device = "cuda:0"
        else:
            device = "cpu"
        return device

    def initiate_model(self): # model initiate 후 eval 모드로 바꿈
        self.model.to(self.device)

        return self.model.eval()

class MyResBck(torchvision.models.ResNet):
    def __init__(self, block, layers):
        super(MyResBck, self).__init__(block, layers)
        self.roi_pool = torchvision.ops.RoIPool(7, 1.0)

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