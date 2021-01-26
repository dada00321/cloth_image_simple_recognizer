import os
import pandas as pd

def read_sales_cats_and_links(clothes_provider):
    if clothes_provider == "lativ":
        # 以 '/modules' 為起始節點
        #csv_path = "../local_data/Lativ_Crawler/res/tier_1.csv"
        # 以 主程式 為起始節點
        csv_path = "./local_data/Lativ_Crawler/res/tier_1.csv"
        
        if os.path.exists(csv_path):
            data = pd.read_csv(csv_path)
        needed_col_names = ["sales-category","link","genre"]
        
        #print(data[needed_col_names[0]].head()) # 印出 '銷售分類'(中文) 的前幾列
        #print(data[needed_col_names[1]].head()) # 印出 '銷售分類 URL' 的前幾列
        #print(len(sales_cats), len(sales_links))
        sales_cats = data[needed_col_names[0]]
        sales_links = data[needed_col_names[1]]
        genres = data[needed_col_names[2]]
        return sales_cats, sales_links, genres
"""
if __name__ == "__main__":
    sales_cats, sales_links = read_sales_cats_and_links("lativ")
    print(sales_links.head())
    print()
    print(sales_cats.tail())
"""