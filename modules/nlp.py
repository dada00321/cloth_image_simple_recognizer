import jieba
import numpy as np

''' return 句子的餘弦相似度 '''
def get_word_vectors(s1, s2):
    # 分詞
    cut1 = jieba.cut(s1)
    cut2 = jieba.cut(s2)
    #stop_words = ["‧", "/"]
    list_word1 = (','.join(cut1)).split(',')
    list_word2 = (','.join(cut2)).split(',')

    # 列出所有的詞，取聯集
    key_word = list(set(list_word1 + list_word2))
    # 給定形狀和類型的用 0 填充的矩陣儲存向量
    word_vector1 = np.zeros(len(key_word))
    word_vector2 = np.zeros(len(key_word))

    # 計算詞頻
    # 依次確定向量的每個位置的值
    for i in range(len(key_word)):
        # 遍歷key_word中每個詞在句子中的出現次數
        for j in range(len(list_word1)):
            if key_word[i] == list_word1[j]:
                word_vector1[i] += 1
        for k in range(len(list_word2)):
            if key_word[i] == list_word2[k]:
                word_vector2[i] += 1

    # 輸出向量
    print(word_vector1)
    print(word_vector2)
    return word_vector1, word_vector2

''' return 兩個向量的餘弦相似度 '''
def cos_similarity(vec1, vec2):
    return float(np.dot(vec1,vec2)/(np.linalg.norm(vec1)*np.linalg.norm(vec2)))

def get_similarity(s1, s2):
    vec1, vec2 = get_word_vectors(s1, s2)
    cos_sim = cos_similarity(vec1, vec2)
    return cos_sim

if __name__ == "__main__":
    '''
    s1="這隻皮靴號碼大了。那隻號碼合適"
    s2="這隻皮靴號碼不小，那隻更合適" 
    '''
    s1, s2 = "休閒/連帽上衣/厚T系列", "休閒 連帽T"
    cos_sim = get_similarity(s1, s2)
    print(f"\'{s1}\' 和 \n\'{s2}\' 的相似度:\n", cos_sim)
    
    