from model import SimBck
from PIL import Image
import faiss

class YouRecoVecDB(SimBck):
    def __init__(self, dir = False):
        super(YouRecoVecDB, self).__init__(dir)
        self.initiate_model()
        
    def load_img(self, category, imgfile):

        img = Image.open(f'../Product_DB/data/{category}/{imgfile}.jpg').convert('RGB')
        
        return img

    def feature_extractor(self, category, imagefile): # Resnet-50으로부터 feature extraction/extra classification
        img = self.load_img(category, imagefile)
        img_trans = self.transform(img)
        img_trans = img_trans.unsqueeze(0) # (1, 3, 224, 224)
        img_trans = img_trans.to(self.set_device())

        # Embedding vector
        embed_feature = []
        hook = self.model.avgpool.register_forward_hook(
          lambda self, input, output: embed_feature.append(output.flatten().unsqueeze(0)))
        res = self.model(img_trans)
        hook.remove()

        return embed_feature[0] # (1, 2048)
    
    def vector_to_faiss(self, dataframe):
        index= faiss.IndexFlatL2(2048)
        index = faiss.IndexIDMap2(index)
        for col in dataframe.values:
            itemid = col[0]
            category = col[1]
            imagefile = col[2]
            try: # 없는 이미지의 경우 에러 무시
                img_embedding= self.feature_extractor(category, imagefile)
                img_embedding = img_embedding.detach().numpy()
                index.add_with_ids(img_embedding, itemid) # index의 vetor space에 vector projection with itemid
                print("good!")
            except:
                print("bad.")
                pass

        faiss.write_index(index, 'Youreco_vectorDB.index')

        return