import os
import torchvision
from torch.utils.data import DataLoader
from libs.load_huggingface import image_processor


# Dataset settings
dataset_location = input("데이터셋 경로를 입력하세요: ex)D:/Data/dataset ")
ANNOTATION_FILE_NAME = "labels.json"
TRAIN_DIRECTORY = os.path.join(dataset_location, "train")
VAL_DIRECTORY = os.path.join(dataset_location, "val")
TEST_DIRECTORY = os.path.join(dataset_location, "test")

class CocoDetection(torchvision.datasets.CocoDetection):
    def __init__(self, dataset_directory_path, image_directory_path, image_processor, train=True):
        annotation_file_path = os.path.join(dataset_directory_path, ANNOTATION_FILE_NAME)
        super().__init__(image_directory_path, annotation_file_path)
        self.image_processor = image_processor

    def __getitem__(self, idx):
        images, annotations = super().__getitem__(idx)
        image_id = self.ids[idx]
        annotations = {'image_id': image_id, 'annotations': annotations}
        encoding = self.image_processor(images=images, annotations=annotations, return_tensors="pt")
        pixel_values = encoding["pixel_values"].squeeze()
        target = encoding["labels"][0]
        return pixel_values, target

# Assuming 'image_processor' is defined elsewhere in your project
TRAIN_DATASET = CocoDetection(TRAIN_DIRECTORY, TRAIN_DIRECTORY + "/data", image_processor, train=True)
VAL_DATASET = CocoDetection(VAL_DIRECTORY, VAL_DIRECTORY + "/data", image_processor, train=False)
TEST_DATASET = CocoDetection(TEST_DIRECTORY, TEST_DIRECTORY + "/data", image_processor, train=False)

print("Number of training examples:", len(TRAIN_DATASET))
print("Number of validation examples:", len(VAL_DATASET))
print("Number of test examples:", len(TEST_DATASET))

def collate_fn(batch):
    pixel_values = [item[0] for item in batch]
    encoding = image_processor.pad(pixel_values, return_tensors="pt")
    labels = [item[1] for item in batch]
    return {'pixel_values': encoding['pixel_values'], 'pixel_mask': encoding['pixel_mask'], 'labels': labels}

TRAIN_DATALOADER = DataLoader(TRAIN_DATASET, collate_fn=collate_fn, batch_size=8, num_workers=12, shuffle=True, pin_memory=True, persistent_workers=True)
VAL_DATALOADER = DataLoader(VAL_DATASET, collate_fn=collate_fn, batch_size=8, num_workers=12, pin_memory=True, persistent_workers=True)
TEST_DATALOADER = DataLoader(TEST_DATASET, collate_fn=collate_fn, batch_size=8, num_workers=24, pin_memory=True, persistent_workers=True)

# id2label definition
categories = TRAIN_DATASET.coco.cats
id2label = {k: v['name'] for k, v in categories.items()}
