# ---------------------------------------------#
#   运行前一定要修改classes
#   如果生成的2007_train.txt里面没有目标信息
#   那么就是因为classes没有设定正确
# ---------------------------------------------#
import xml.etree.ElementTree as ET
from os import getcwd
import shutil
from os.path import join
from os import listdir

sets = [('2023', 'train'), ('2023', 'val'), ('2023', 'test')]

classes = ['004', '008', '012', '026', '027', '030', '062', '063', '094',
           '104', '111', '123', '132', '134', '149', '154', '162', '164',
           '173', '183', '186', '189', '206', '209', '234', '247', '252',
           '255', '269', '274', '277', '287', '307', '311', '318', '323',
           '327', '334', '335', '338', '373', '376', '379', '387', '389',
           '393', '404', '407', '408', '419', '421', '446', '461', '468',
           '476', '483', '484', '489', '537']

class_s = ['1_Single', '2_UD', '3_LR', '4_Triangle', '5_S', '6_Multiple']

path_img = "F:\oracle\ACCID_baseline\Datasets\ACCID2023\Image_SR"
path_ann = "F:\oracle\ACCID_baseline\Datasets\ACCID2023\Annotation_SR"
dirs_img = listdir(path_img)
dirs_ann = listdir(path_ann)


def convert_annotation(image_id, list_file):
    in_file = open('Datasets\ACCID2023/Annotations/%s.xml' % (image_id), encoding='utf-8')
    tree = ET.parse(in_file)
    root = tree.getroot()
    # print("in_file", in_file)
    # print("tree", tree)
    # print("root", root)

    for obj in root.iter('object'):
        # print("obj", obj)
        difficult = 0
        if obj.find('difficult') != None:
            difficult = obj.find('difficult').text

        cls = obj.find('name').text
        # print("cls", cls)

        if cls not in classes or int(difficult) == 1:
            continue
        cls_id = classes.index(cls)
        xmlbox = obj.find('bndbox')
        b = (int(xmlbox.find('xmin').text), int(xmlbox.find('ymin').text), int(xmlbox.find('xmax').text),
             int(xmlbox.find('ymax').text))
        list_file.write(" " + ",".join([str(a) for a in b]) + ',' + str(cls_id))
        # print(" " + ",".join([str(a) for a in b]) + ',' + str(cls_id))


wd = getcwd()

list_file = open('radical_train.txt', 'w')
for folder in dirs_ann:
    folder_path = join(path_ann, folder)
    class_SR = folder
    SR_id = class_s.index(class_SR)
    print("folder_path", folder_path)
    print("class_SR", class_SR)
    for xml in listdir(folder_path):
        image_id = xml[:-4]
        # print("xml_path", image_id)

        list_file.write('%s/Datasets/ACCID2023/Image_SR/%s/%s.jpg' % (wd, class_SR, image_id))
        list_file.write(" " + str(SR_id))
        convert_annotation(image_id, list_file)
        list_file.write('\n')

        # print("finish one image", image_id)

list_file.close()

# for year, image_set in sets:
#     image_ids = open('VOCdevkit/VOC%s/ImageSets/Main/%s.txt'%(year, image_set)).read().strip().split()
# list_file = open('%s_%s.txt'%(year, image_set), 'w')
# for image_id in image_ids:
#     list_file.write('%s/VOCdevkit/VOC%s/JPEGImages/%s/%s.jpg'%(wd, year,class_SR ,image_id))
#     convert_annotation(year, image_id, list_file)
#     list_file.write('\n')
# list_file.close()