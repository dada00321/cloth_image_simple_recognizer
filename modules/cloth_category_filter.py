import os
from translate import Translator

from modules.img2word import Image2Word
from modules.local_data_reader import read_sales_cats_and_links
from modules.nlp import get_similarity

''' 主函式 '''
""" 傳回前 K 項 與輸入圖片最相似的銷售分類等資訊 (預設 K=5) """
def get_3_most_likely_info(img_path, K=5):
    #img_path = "./local_images/lativ-test/4.jpg" # 本地圖片
    recog_words = inputImg_2_recognizedWords(img_path)
    recog_words = get_prettified_msg(recog_words, 1) # 英文描述文字
    #print(recog_words)
    recog_words = translate_en_2_zhTW(recog_words)
    recog_words = get_prettified_msg(recog_words, 2) # 中文描述文字
    #print(recog_words)
    
    most_likely_sales_cats, most_likely_sales_links, most_likely_genres = get_similar_salesCat_and_link(recog_words, K)
    #print("most_likely_sales_cats:\n", most_likely_sales_cats, "\nmost_likely_sales_links:\n", most_likely_sales_links, "\nmost_likely_genres:\n", most_likely_genres)
    return most_likely_sales_cats, most_likely_sales_links, most_likely_genres

''' 輸入圖片(本機圖片|LineBot) => ibm-API 辨識出文字(英文) '''
def inputImg_2_recognizedWords(img_path):
    # 辨識單一圖片的解釋文字
    if os.path.exists(img_path):
        recog_words = Image2Word().img2word_singleImg(img_path)
        #print(recog_words)
        return recog_words # type: 'dict'
    else:
        print(f"圖片路徑: {img_path} 不存在")

def get_prettified_msg(recog_words, state): # type: 'dict'
    '''
    [1] 最終需 mapping 到銷售分類，只需知道 材質特徵 即可，此處過濾掉 顏色特徵
    [2] 結果字串 不保留前綴 "texture: "
    [3] 結果字串 以 "," 分隔資料
    '''
    if state == 1:
        # e.g. texture: raglan garment, sleeve, fabric@color: gray color
        textures = recog_words.get("texture") # type: 'list'
        #colors = recog_words.get("color") # type: 'list'
        #prettified_msg = "texture: " + ", ".join(textures) # + "@"
        prettified_msg = ",".join(textures) # + "@"
        #prettified_msg += "color: " + ", ".join(colors)
        return prettified_msg
    elif state == 2:
        # e.g. 質地：插肩式服裝,袖子,面料@顏色：灰色
        prettified_msg = recog_words.replace("質地", "材質").replace("袖子", "長袖").replace("面料", "棉質")
        return prettified_msg
    else:
        return None

''' ibm-API 辨識文字(英文) => 文字轉為中文 '''
def translate_en_2_zhTW(input_en_words):
    # e.g. 質地：插肩式服裝,袖子,面料@顏色：灰色
    translator= Translator(to_lang="zh-TW")
    translation = translator.translate(input_en_words)
    translation = translation.replace("“","\"").replace("”","\"").replace("，",",")
    return translation

''' 辨識文字(中文) => 與本地資料類別做比較篩選 '''
def get_similar_salesCat_and_link(recog_words, K):
    # load: "服飾銷售分類"、"銷售分類連結"
    sales_cats, sales_links, genres = read_sales_cats_and_links("lativ")
    
    # 對所有本地服飾銷售分類，兩兩計算 "銷售分類" 與 "圖片辨識文字" 的文字餘弦相似度
    # e.g. sales_cat: 上衣類 | recog_words: 插肩式服裝,袖子,面料
    cos_sim_list = list()
    print("正在為所有可能的銷售分類計算餘弦相似度 ...")
    for sales_cat in sales_cats:
        cos_sim = get_similarity(sales_cat, recog_words)
        cos_sim_list.append(cos_sim)
    
    # 依文字相似度排序
    sorted_sales_cats = _sort_list1_by_list2(sales_cats, cos_sim_list)
    sorted_sales_links = _sort_list1_by_list2(sales_links, cos_sim_list)
    sorted_genres = _sort_list1_by_list2(genres, cos_sim_list)
    
    # 傳回前五項(5/190)
    return sorted_sales_cats[:K], sorted_sales_links[:K], sorted_genres[:K]
    
def _sort_list1_by_list2(list1, list2):
    #list1 = ["a", "b", "c"]
    #list2 = [2, 3, 1]
    zipped_lists = zip(list2, list1)
    sorted_zipped_lists = sorted(zipped_lists, reverse=True) # 遞減
    sorted_list1 = [element for _, element in sorted_zipped_lists]
    #print(sorted_list1)
    return sorted_list1
    
if __name__ == "__main__":
    pass