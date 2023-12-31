#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import torch
import torchvision
from torchvision import transforms
import numpy as np
import faiss

class SimBck: # Similairty Backbone = Resnet50
    def __init__(self,
                    dir = False,
                    model = torchvision.models.resnet50(pretrained = True),
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
            self.model.load_state_dict(torch.load(dir))
        else:
            pass

    def assign_transform(self):
        try:
            preprocess = self.weights.transforms()

        except Exception:
            preprocess = transforms.Compose(
              [
                  transforms.ToTensor(),
                  transforms.Normalize(
                      mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225]
                  ),
              ]
            )

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

class YouRecoSIm(SimBck):
    def __init__(self, dir = False):
        super(YouRecoSIm, self).__init__(dir)
        self.initiate_model()
        self.index_DB = faiss.read_index('Youreco_vectorDB.index') # DB 저장소

    def feature_extractor(self,image_dir, query_img, box): # Resnet-50으로부터 feature extraction/extra classification
        query_img = Image.open(f'{image_dir}/{query_img}.jpg').convert('RGB')
        img_trans = self.transform(query_img)
        img_trans = img_trans.unsqueeze(0) # (1, 3, 224, 224)
        img_trans = img_trans.to(self.set_device())

        # Embedding vector = (1, 2048)
        embed_feature = []
        hook = self.model.avgpool.register_forward_hook(
          lambda self, input, output: embed_feature.append(output.flatten().unsqueeze(0)))
        res = self.model(img_trans, box)
        hook.remove()

        # Classification
        res = self.model(img_trans, box)
        _, cls = torch.max(res.data, 1)

        return embed_feature[0], cls

    def retrieval_similar(self, image_dir, query_img, box):
        query_img_embedding, category = self.feature_extractor(image_dir, query_img, box)
        
        n = 4
        while True:
            # query image may not be in similarity vector space.
            distance, indices = self.index_DB.search(query_img_embedding.reshape(1, -1), n)
            
            if len(set(indices.squeeze(0))) == 4:
                # 유사도 랭크 순으로 중복 제거한 itemid list
                indices = sorted(set(indices.squeeze(0)), key = lambda x : list(indices.squeeze(0)).index(x) )
                
                return indices, category  
                
            else:
                n += 1
                
        return

def similarity_result(model, key_result, image_dir):
    similar_itemid_list = list() # 유사 이미지 상품 itemid
    category_list = list() # 각 object의 classification 결과의 category
    for obj in key_result:
        indices, category = model.retrieval_similar(image_dir, obj[0], obj[3])
        similar_itemid_list.append(indices)
        category_list.append(category)
    
    return similar_itemid_list, category_list 

