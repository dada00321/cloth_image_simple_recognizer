from modules.cloth_category_filter import get_3_most_likely_info

def _trans_genre_2_zhTW(genre):
    if genre == "WOMEN":
        return "女裝"
    elif genre == "MEN":
        return "男裝"
    elif genre == "KIDS":
        return "童裝"
    elif genre == "BABY":
        return "嬰幼兒"
    else:   #elif genre == "SPORTS":
        return "運動類"
    
def get_recommended_msg(sales_cats, links, genres):
    '''
    描述性文字: 服飾銷售分類, 銷售客群
    功能性文字: 服飾銷售分類 的 網頁鏈結
    '''
    msg = "\n"
    msg += "本程式採 IBM Visual Recognition API "
    msg += "與文字餘弦相似度，計算與輸入圖片最相似的前幾個銷售分類"
    msg += "( P.S. 僅依\"文字\"分類，且無法判定性別、年紀(銷售客群分類) )" + "\n"
    msg += "已為您分析出與\"服飾類型\"前幾最相似的服飾！" + "\n"
    for i, v in enumerate(links):
        msg += "服飾種類： " + sales_cats[i] + "\n"
        msg += "銷售客群分類： " + _trans_genre_2_zhTW(genres[i]) + "\n"
        msg += "網頁鏈結： " + v + "\n"*2
    print(msg)
    
if __name__ == "__main__":
    img_path = "./local_images/lativ-test/3.jpg" # 本地圖片
    tmp1, tmp2, tmp3 = get_3_most_likely_info(img_path) # img_path: 可為 本地圖片 or LineBot上傳圖片
    most_likely_sales_cats, most_likely_sales_links, most_likely_genres = tmp1, tmp2, tmp3
    get_recommended_msg(most_likely_sales_cats, most_likely_sales_links, most_likely_genres)