import torch
from PIL import Image
import numpy as np
import torchvision.transforms as T

class ResSimRoi(torch.utils.data.Dataset):
    def __init__(self, df, unique_imgs, indices, phase): # df = rst
        self.df = df
        self.unique_imgs = unique_imgs
        self.indices = indices
        self.phase = phase
        self.process = self.assign_transform()

    def __len__(self):
        return len(self.indices)

    def __getitem__(self, idx):
      # index 접근 후 image name
        image_name = self.unique_imgs[self.indices[idx]]
        info = self.df[self.df.ImageID	== image_name]

      # 이미지, 라벨, 박스 정보
        img = Image.open(f'{self.phase}/data/' + image_name).convert('RGB')
        boxes = info.iloc[:,-4:]
        boxes = np.concatenate([list([0] for i in range(len(boxes))), boxes.values], axis = 1) # roi_pooling input format
        labels = info.iloc[:, -5]

      # 이미지, 박스, 라벨  to tensor
        img = self.process(img)
        boxes = torch.tensor(boxes, dtype = torch.float32) # 예시 : tensor([[0.000, 0.0516, 0.3203, 0.3133, 0.6508], [0.000, 0.3937, 0.3609, 0.6445, 0.6828], [0.000, 0.6922, 0.2984, 0.9789, 0.6281]], dtype=torch.float64)
        labels = torch.tensor(labels.values.reshape(-1, 1)) # 예시: tensor([[9],[9],[9]])

      # process the result of list
        result = list()
        box_num = len(boxes)
        for res in zip([img] * box_num, boxes, labels):
          result.append((res[0], res[1].unsqueeze(0), res[2]))

        return result # 하나의 이미지에 여러개의 박스가 있는 경우, 각각 crop한 image의 tensor와 label이 매칭된 튜플의 리스트로 반환

    def assign_transform(self): # augmentation 적용, process img 자체가 이미 (224,224) 크기이므로, resize는 X
        # Augmentation : Flip/Color
        # preprocess = T.Compose([T.RandomHorizontalFlip(p = 0.5),
        #                         T.ColorJitter(brightness=0.5, contrast=0.5, saturation=0.5, hue=0.5),
        #                         T.ToTensor(),
        #                         T.Normalize(mean = [0.485, 0.456, 0.406], std = [0.229, 0.224, 0.225])])
        preprocess = T.Compose([T.ToTensor(),
                                T.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225])])

        return preprocess

def custom_collate(data):
    return data