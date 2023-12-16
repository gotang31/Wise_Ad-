import pandas as pd
from PIL import ImageFile
from pdb_to_vdb import YouRecoVecDB
from model import SimRes50
import torch


if __name__ == '__main__':

    pdb_df = pd.read_csv('../Product_DB/item_table.csv')

    ImageFile.LOAD_TRUNCATED_IMAGES = True                                      # 깨진 파일 에러 무시

    model_dir = '../fine_tuned_Res_Sim_RoI.pt'                                     # your resnet model

    model = YouRecoVecDB()
    # model.model = SimRes50()                                                  # 만약 RoI로 이용한다면 주석 처리 삭제하면 됨.
    model.model.load_state_dict(torch.load(model_dir, map_location='cpu'))      # GPU 사용 시에 map_location = 'cpu' 삭제

    model.vector_to_faiss(pdb_df)                                               # 현재 디렉토리에 vector database 파일 저장