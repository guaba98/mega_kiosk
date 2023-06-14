import pandas as pd
import sqlite3

con = sqlite3.connect('./DATA/data.db')
cur = con.cursor()
price_df = pd.read_sql('select * from drinks_price', con) # 가격 테이블
menu_df = pd.read_sql('select * from drinks_menu', con) # 음료상세정보 전체 테이블
img_path_df = pd.read_sql('select * from drinks_img_path', con) # 음료 이미지 경로 테이블

# print(menu_df.columns)

drinks_id = menu_df.loc[(menu_df['category'] == '디카페인'), 'id'].to_string(index=False)
drinks_id_list = [id for id in drinks_id]
# for i in drinks_id_list:
#     print(img_path_df.loc[(img_path_df['id'] ==1), 'img_path'])

# new_dict = {}
new_list = [id for id in menu_df.loc[(menu_df['category'] == '디카페인'), 'id']]
# for i in new_list:
#     new_dict[i] = img_path_df.loc[(img_path_df['id'] ==i), 'img_path'].to_string(index=False)
# print(new_dict)

new_dict = {i:img_path_df.loc[(img_path_df['id'] ==i), 'img_path'].to_string(index=False) for i in new_list}
# print(new_dict)
# drinks_img_path = img_path_df.loc[(img_path_df['id'] ==1), 'img_path']
# print(drinks_img_path)


for i in range(1, 25):
    print(i)
    con2 = menu_df['category_num'] == i
    # print(menu_df.loc[con2, ['img_path']])
    print(menu_df.loc[con2, ['menu_name']].values)
    # print(menu_df.loc[con2, ['price']])
    # getattr(self, f'menu_img_{i}').setPixmap(QPixmap(menu_df.loc[i-1, 'img_path']).scaled(QSize(155, 84), aspectRatioMode=Qt.IgnoreAspectRatio))
    # getattr(self, f'menu_name_label_{i}').setText(str(menu_df.loc[con2, ['menu_name_x']]))
    # getattr(self, f'menu_price_label_{i}').setText(str(menu_df.loc[con2, ['price']]))
