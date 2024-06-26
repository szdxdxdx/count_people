
# 介绍

本项目为学校大数据实训课程的作业

## 作业题目

工地作业环境的人数考勤统计

任务类型：实时数据处理、批量数据处理

开发平台：Hadoop、HBase，Mapreduce等

开发语言：Java，Python

现有的工地人数统计通常通过负责人手动数，为了加快智慧工地的进程，设计基于大数据分析的智慧工地人数统计算法。

要求：
1. 结合所学爬虫知识爬取工地人物图像或采用现有工地人物数据集。
2. 使用图像标注工具labelimg将图像标注为voc格式，并对图像标签进行本地存储。
3. 利用图像和图像标签，训练一个目标检测神经网络（根据链接配置电脑环境并下载相关代码https://github.com/ultralytics/yolov5），将人员目标检测的结果保存到本地，通过大数据分析相关技术进行考勤统计。

## 本项目介绍

本项目的开发语言只有 python

爬虫使用 requests 库

人员目标检测使用 yolo v8

检测结果统计使用 pyspark

后端使用 flask

前端仅使用单页面 html 作展示

![](./web/1.png)

# 如何运行

## 配置环境

1.  确保使用 3.8 版本的 python
2.  在项目根目录 /count_people 下，创建名为 venv 的 python 虚拟环境
3.  激活虚拟环境
4.  安装依赖，详见项目根目录下的 requirements.txt
5.  修改 /src/config.py 中的 `APP_ROOT`，指向项目的根目录
6.  修改 /src/config.py 中的 `JAVA_HOME`，指向一个能用的 java8 jdk 目录
7.  在根目录创建目录 /env，下载 hadoop-3.3.0 和 spark-3.1.2-bin-hadoop3.2 到 /env 中
    下载链接：
    [spark](https://archive.apache.org/dist/spark/spark-3.1.2/)、
    [hadoop](https://archive.apache.org/dist/hadoop/common/hadoop-3.3.0/)
8.  在系统环境变量中设置 HADOOP_HOME，指向刚刚下载的 /hadoop-3.3.0 目录 
9.  在系统环境变量中设置 SPARK_HOME，指向刚刚下载的 /spark-3.1.2-bin-hadoop3.2 目录
10. 在系统环境变量 Path 中添加 %HADOOP_HOME%\bin 和 %SPARK_HOME%\bin

## 初次运行

1.  使用 flask 运行 /src/app.py，访问`http://127.0.0.1:5000`，
    如果看到 hello world!和一个随机数字，说明 flask 可以正常运行。然后退出程序
2.  运行 /src/count_people_processor.py 中的 main，会执行一次人数统计操作
3.  使用 flask 运行 /src/app.py，然后用浏览器打开 /web/index.html 查看刚刚统计的结果

## 运行

1. 使用 flask 运行 /src/app.py
2. 用浏览器打开 /web/index.html
