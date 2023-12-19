import torch
from PIL import Image
import torchvision.transforms as T

class ResSimCrop(torch.utils.data.Dataset):
    def __init__(self, df, unique_imgs, indices, phase): # df = rst
        self.df = df
        self.unique_imgs = unique_imgs
        self.indices = indices
        self.phase = phase

    def __len__(self):
        return len(self.indices)

    def __getitem__(self, idx):
      # index 접근 후 image name
        image_name = self.unique_imgs[self.indices[idx]]
        info = self.df[self.df.ImageID	== image_name]

      # 해당 이미지의 path, boxes 정보 가져오기
        boxes = info.iloc[:,-4:]

      # 이미지, 라벨 정보
        img = Image.open(f'{self.phase}/data/' + image_name).convert('RGB')
        labels = info.values[:, -5].astype('int64')
        labels = torch.tensor(labels, dtype = torch.int64)

      # 이미지 crop/resize
        cropped_resize_img_list = self.resize_image(img, boxes)
        # cropped_img_list = self.crop_image(img, boxes)
        preprocess = self.assign_transform()

      # process the result of list
        result = list()
        for image, label in zip(cropped_resize_img_list, labels):
          process_img = preprocess(image)
          label = label.unsqueeze(0)
          result.append((process_img, label))

        return result # 하나의 이미지에 여러개의 박스가 있는 경우, 각각 crop한 image의 tensor와 label이 매칭된 튜플의 리스트로 반환

    def assign_transform(self):
        # Augmentation : Flip/Color
        # preprocess = T.Compose([T.RandomHorizontalFlip(p = 0.5),
        #                         T.ColorJitter(brightness=0.5, contrast=0.5, saturation=0.5, hue=0.5),
        #                         T.ToTensor(),
        #                         T.Normalize(mean = [0.485, 0.456, 0.406], std = [0.229, 0.224, 0.225])])
        preprocess = T.Compose([T.ToTensor(),
                                T.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225])])

        return preprocess

    def crop_image(self, img, boxes):
      '''
      img : PIL.Image.open
      boxes : box coordinate pandas DataFrame
      '''
      bounding_boxes = list(v.values for k, v in boxes.iterrows()) #list of box coordinate np.array
      cropped_images = list()

      for bbox in bounding_boxes:
        box = bbox * 640  # 640 = result of image size labelled in roboflow : 만약 다른 사이즈의 img가 input 된다면, 그에 맞춰서 bbox rescaling 해주어야 한다.
        left, top, right, bottom = box.astype('int32')
        height = bottom - top
        width = right - left
        cropped_image = T.functional.crop(img, top, left, height, width)
        cropped_images.append(cropped_image)

      return cropped_images

    def resize_image(self, img, boxes):
      resized_width = 224
      resized_height = 224
      resize = T.Resize(size=(resized_width, resized_height))
      resized_images = list()
      cropped_images = self.crop_image(img, boxes)

      for cropped_image in cropped_images:
          resized_image = resize(cropped_image)
          resized_images.append(resized_image)

      return resized_images # return crop/resize PIL image list

def custom_collate(data):
    return data