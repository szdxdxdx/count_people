import os
from pyspark import SparkConf, SparkContext
import config


class ResultAnalyzer:

    @staticmethod
    def check_env():
        tips = "（修改环境变量后，你可能需要重启 IDE）"
        assert "HADOOP_HOME" in os.environ, "请将 HADOOP_HOME 添加至系统环境变量" + tips
        assert "SPARK_HOME" in os.environ, "请将 SPARK_HOME 添加至系统环境变量" + tips
        paths = os.environ["Path"].split(";")
        assert os.path.join(os.environ["HADOOP_HOME"], "bin") in paths, \
            r"请将 %HADOOP_HOME%\bin 添加至系统 Path 环境变量" + tips
        assert os.path.join(os.environ["SPARK_HOME"], "bin") in paths, \
            r"请将 %SPARK_HOME%\bin 添加至系统 Path 环境变量" + tips

    def __init__(self):
        ResultAnalyzer.check_env()

        print(f"正在加载 spark")

        os.environ["JAVA_HOME"] = config.JAVA_HOME
        os.environ["PYSPARK_PYTHON"] = config.PYSPARK_PYTHON

        self.__conf = SparkConf().setAppName("people count")
        self.__sc = SparkContext(conf=self.__conf)
        self.__input_path = config.PREDICTED_RESULT_FOLDER_PATH

        print(f"加载 spark 完成")

    def map_reduce(self, task_name: str) -> dict:
        """
        对分析的结果进行统计
        """

        print(f"开始使用 spark 对分析的结果进行统计")

        input_path = os.path.join(self.__input_path, task_name, "txt")
        assert os.path.exists(input_path)

        lines = self.__sc.textFile(input_path)
        word_counts = lines.map(lambda line: line.split(" ")[0]) \
                           .map(lambda word: (word, 1)) \
                           .reduceByKey(lambda a, b: a + b) \
                           .collectAsMap()

        print(f"统计完成")

        return {
            "count": {class_name: word_counts.get(str(idx), 0) for idx, class_name in enumerate(config.CLASS_NAME)}
        }

    def stop(self):
        self.__sc.stop()


if __name__ == "__main__":
    analyzer = ResultAnalyzer()
    analyzed_result = analyzer.map_reduce("example")
    print(analyzed_result)
