import os
import sys

from PIL import Image
from tqdm import tqdm


def cutout():
    pics_src_dir = sys.argv[1]
    pics_target_dir = pics_src_dir + '_cut'
    # 新建存储抠图的文件夹
    os.makedirs(pics_target_dir, exist_ok=True)
    # 列出文件夹下所有的带切割图片
    pics_list = os.listdir(pics_src_dir)
    dist = [0, 73, 145, 216]
    with open(pics_target_dir + '_mapping.txt', 'w') as to_write_mapping:
        for m_ind, m_pic_name in tqdm(enumerate(pics_list), desc='切图进度', total=len(pics_list)):
            cur_path = os.path.join(pics_src_dir, m_pic_name)
            m_pic_prefix_name = m_pic_name.split('.')[0]
            m_pic_suffix_name = '.' + m_pic_name.split('.')[1]
            pic_desc_name = m_pic_prefix_name + '_desc' + m_pic_suffix_name
            if os.path.isfile(cur_path):
                im = Image.open(cur_path)

                # 取消灰度化
                # # 将图片灰度化
                # gray = im.convert('L')
                # np_gray = np.array(gray)

                # 获得降色阶后的灰度图
                # 暂时不需要进行降色阶
                # Image.fromarray(np.array(np_gray / 16, dtype='uint8'))

                # 获得文字图片
                to_save_path_word = os.path.join(pics_target_dir, pic_desc_name)
                Image.fromarray(im[0:30, 120:120 + 80, :]).save(to_save_path_word)

                # 分别抠图获得小图片
                for j in range(4):
                    to_save_path_row1 = os.path.join(pics_target_dir,
                                                     m_pic_prefix_name + '_' + str(j + 1) + m_pic_suffix_name)
                    to_save_path_row2 = os.path.join(pics_target_dir,
                                                     m_pic_prefix_name + '_' + str(j + 5) + m_pic_suffix_name)
                    Image.fromarray(im[42:42 + 66, 5 + dist[j]:5 + dist[j] + 66, :]).save(to_save_path_row1)
                    Image.fromarray(im[115:115 + 66, 5 + dist[j]:5 + dist[j] + 66, :]).save(to_save_path_row2)
                    to_write_mapping.write('%s,%s\n%s,%s\n' % (
                        to_save_path_word,
                        to_save_path_row1,
                        to_save_path_word,
                        to_save_path_row2,
                    ))

            if m_ind > 0 and m_ind % 100 == 0:
                to_write_mapping.flush()


if __name__ == '__main__':
    cutout()
