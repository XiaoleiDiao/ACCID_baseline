#!/usr/bin/env python3
# -*- coding: utf-8 -*-

'''
通过解析xml文件，批量修改xml文件里的标签名称，比如把标签zero改成num
'''
import os.path
import pandas as pd
import glob
import collections
import os
import xml.etree.ElementTree as ET


path = r'F:/oracle/REZCR/Datasets/single/single/'    #存储标签的路径，修改为自己的Annotations标签路径
xls_path = r'F:/oracle/REZCR/excel_data/radical_606.xls'

xls_file = pd.read_excel(xls_path)
df = collections.OrderedDict(zip(xls_file.iloc[:,2],xls_file.iloc[:,0]))
# print("df", df)



origin_ann_dir = r'F:/oracle/REZCR/Datasets/OracleRC2022/Annotations/'  # 设置原始标签路径为 Annos
new_ann_dir = r'F:/oracle/REZCR/Datasets/OracleRC2022/Annotation_new/'  # 设置新标签路径 Annotations
for dirpaths, dirnames, filenames in os.walk(origin_ann_dir):  # os.walk游走遍历目录名
    for filename in filenames:
        print("process...")
        if os.path.isfile(r'%s%s' % (origin_ann_dir, filename)):  # 获取原始xml文件绝对路径，isfile()检测是否为文件 isdir检测是否为目录
            origin_ann_path = os.path.join(r'%s%s' % (origin_ann_dir, filename))  # 如果是，获取绝对路径（重复代码）
            new_ann_path = os.path.join(r'%s%s' % (new_ann_dir, filename))
            tree = ET.parse(origin_ann_path)  # ET是一个xml文件解析库，ET.parse（）打开xml文件。parse--"解析"
            root = tree.getroot()  # 获取根节点
            for object in root.findall('object'):  # 找到根节点下所有“object”节点
                name = str(object.find('name').text)  # 找到object节点下name子节点的值（字符串）
                # 如果name等于str，则删除该节点
                # if (name in ["car_head"]):
                #     root.remove(object)

                # 如果name等于str，则修改name
                if (name in df.keys()):
                    print("name", name)
                    object.find('name').text = str(df.get(name))
                    print("renew label",str(df.get(name)))
                else:
                    print("name", name)
            # 检查是否存在labelmap中没有的类别
            # for object in root.findall('object'):
            #     name = str(object.find('name').text)
            #     if not (name in ["chepai", "chedeng", "chebiao"]):
            #         print(filename + "------------->label is error--->" + name)
            tree.write(new_ann_path)  # tree为文件，write写入新的文件中。




# for xml_file in glob.glob(path + '/*.xml'):
# 	print("xml_file",xml_file)
#     ####### 返回解析树
# 	tree = ET.parse(xml_file)
# 	##########获取根节点
# 	root = tree.getroot()
# 	#######对所有目标进行解析
# 	for member in root.findall('object'):
# 		objectname = member.find('name').text
# 		print("member", member)
# 		print("objectname", objectname)
# 		if objectname == 'zero':      #原来的标签名字
# 			print(objectname)
# 			member.find('name').text = str('num')    #替换的标签名字
# 			tree.write(xml_file)
