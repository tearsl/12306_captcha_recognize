import os
import numpy as np
from PIL import Image

pics_src_dir = './pics'
to_file_dir = pics_src_dir+'_cut'
#新建存储抠图的文件夹
os.makedirs(to_file_dir, exist_ok=True)
# 列出文件夹下所有的带切割图片
pics_list = os.listdir(pics_src_dir)
dist = [0, 73, 145, 216]
with open(to_file_dir + '_mapping.txt', 'w') as to_write_mapping:
    for ind, m_pic_name in enumerate(pics_list):
        cur_path = os.path.join(pics_src_dir, m_pic_name)
        m_pic_prefix_name = m_pic_name.split('.')[0]
        m_pic_suffix_name = '.'+m_pic_name.split('.')[1]
        pic_desc_name= m_pic_prefix_name + '_desc.'+m_pic_suffix_name
        if os.path.isfile(cur_path):
            im = Image.open(cur_path)
            #将图片灰度化
            gray = im.convert('L')
            np_gray = np.array(gray)
            #获得降色阶后的灰度图
            Image.fromarray(np.array(np_gray/16,dtype='uint8'))
            #获得文字图片
            Image.fromarray(np_gray[0:30, 120:120 + 80]).save(os.path.join(to_file_dir, pic_desc_name))

            # 分别抠图获得小图片
            for j in range(4):
                to_save_path_row1=os.path.join(to_file_dir,m_pic_prefix_name+str(j+1)+m_pic_suffix_name)
                to_save_path_row2=os.path.join(to_file_dir,m_pic_prefix_name+str(j+5)+m_pic_suffix_name)
                Image.fromarray(np_gray[42:42 + 66, 5 + dist[j]:5 + dist[j] + 66]).save(to_save_path_row1)
                Image.fromarray(np_gray[115:115 + 66, 5 + dist[j]:5 + dist[j] + 66]).save(to_save_path_row2)
                cur_path = os.getcwd()
                to_write_mapping.write('{path}/{pic_name}_desc.jpg,{path}/{pic_name}_{index}.jpg\n'.format_map(
                    {'path': cur_path,
                     'pic_name': m_pic_prefix_name,
                     'index': j + 1
                     }
                ))
                to_write_mapping.write('{path}/{pic_name}_desc.jpg,{path}/{pic_name}_{index}.jpg\n'.format_map(
                    {'path': cur_path,
                     'pic_name': m_pic_prefix_name,
                     'index': j + 5
                     }
                ))
            print('第%d张输出成功' % ind)
