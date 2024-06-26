import random
import os
import json
from flask import Flask, send_file
from flask_cors import cross_origin
from count_people_processor import CountPeopleProcessor
import config


app = Flask(__name__)


# 返回 Hello, World! 文本，随带一个随机数字
# 用于测试前后端的连接
@app.route("/")
@cross_origin()
def hello_world():
    return f"Hello, World! {random.randint(1, 100)}"


# 返回一个历史统计结果
@app.route("/history/<path:task_name>")
@cross_origin()
def history(task_name: str):
    with open(os.path.join(config.APP_DATA_FOLDER_PATH, "task", task_name + ".txt")) as f:
        return json.load(f)


# ---------

count_people_processor = CountPeopleProcessor()


# 执行一次统计操作
@app.route("/do")
@cross_origin()
def process():
    return count_people_processor.process()


# 返回一张收集到的图片
@app.route("/img/c/<path:task_name>/<path:img_file_name>")
@cross_origin()
def img_c(task_name: str, img_file_name: str):
    try:
        return send_file(os.path.join(config.COLLECTED_DATA_FOLDER_PATH, task_name, img_file_name))
    except FileNotFoundError:
        return "file not found", 404


# 返回一张模型预测后的图片
@app.route("/img/p/<path:task_name>/<path:img_name>")
@cross_origin()
def img_p(task_name: str, img_name: str):
    try:
        return send_file(os.path.join(config.PREDICTED_RESULT_FOLDER_PATH, task_name, "img", img_name))
    except FileNotFoundError as e:
        return "file not found", 404


# 返回模型预测后的结果
@app.route("/txt/p/<path:task_name>/<path:img_name>")
@cross_origin()
def txt_p(task_name: str, img_name: str):
    txt_name = img_name + ".txt"
    with open(os.path.join(config.PREDICTED_RESULT_FOLDER_PATH, task_name, "txt", txt_name)) as f:
        count_class_idx_list = [int(line.split(" ")[0]) for line in f.readlines()]
        result = {class_name: count_class_idx_list.count(idx) for idx, class_name in enumerate(config.CLASS_NAME)}
    return result


if __name__ == '__main__':
    app.run(debug=True)
