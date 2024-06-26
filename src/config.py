
import os

# 你需要给出本项目在磁盘中的绝对路径
APP_ROOT = r""

# ---------

# 该文件夹下存放着本应用会产生的所有数据
APP_DATA_FOLDER_PATH = os.path.join(APP_ROOT, "data")

# 该文件夹下存放着收集到的数据
COLLECTED_DATA_FOLDER_PATH = os.path.join(APP_DATA_FOLDER_PATH, "collected")

# 该文件夹下存放着模型预测的结果
PREDICTED_RESULT_FOLDER_PATH = os.path.join(APP_DATA_FOLDER_PATH, "predicted")

# 该文件夹下存放着每次人数统计的结果
COUNT_TASK_RESULT_FOLDER_PATH = os.path.join(APP_DATA_FOLDER_PATH, "task")

# 模型 1
# MODEL_PATH = os.path.join(APP_ROOT, r"src\object_prediction_models\lu_6m.pt")
# CLASS_NAME = ["safety_helmet", "no_safety_helmet", "person"]
# 模型 2
MODEL_PATH = os.path.join(APP_ROOT, r"src\object_prediction_models\css_6m.pt")
CLASS_NAME = ["safety_helmet", "mask", "no_safety_helmet",
              "no_mask", "no_safety_vest", "person", "safety_cone",
              "safety_vest", "machinery", "vehicle"]

# pyspark 环境
# 注意：你还需要在环境变量中指定 HADOOP_HOME 和 SPARK_HOME
JAVA_HOME = r""  # 必须 java 8
PYSPARK_PYTHON = os.path.join(APP_ROOT, r"venv\Scripts\python.exe")

TIME_FORMAT = "%Y-%m-%d %H:%M:%S"

assert APP_ROOT is not "", "你还没配置完环境"
assert JAVA_HOME is not "", "你还没配置完环境"
