from datetime import datetime
import os
import json
from data_collector import DataCollector
from object_predictor import ObjectPredictor
from result_analyzer import ResultAnalyzer
import config


class CountPeopleProcessor:
    def __init__(self):
        self.__data_collector = None
        self.__object_predictor = None
        self.__result_analyzer = None
        self.__inited = False
        self.__output_path = config.COUNT_TASK_RESULT_FOLDER_PATH

    def init(self):
        self.__data_collector = DataCollector()
        self.__object_predictor = ObjectPredictor()
        self.__result_analyzer = ResultAnalyzer()
        self.__inited = True

    def process(self, task_name_: str = None) -> dict:
        """
        执行一轮人数统计（收集数据 -> 对象检测 -> 统计分析）
        """

        if not self.__inited:
            self.init()

        process_start_time = datetime.now()
        task_name = process_start_time.strftime("%Y%m%d%H%M%S")

        if task_name_ is not None:
            task_name = task_name_

        collected_result = self.__data_collector.collect(task_name)
        predicted_result = self.__object_predictor.predict(task_name)
        analyzed_result = self.__result_analyzer.map_reduce(task_name)

        process_end_time = datetime.now()

        result_json = {
            "process_detail": [
                {"whole_process": {
                    "task_name": task_name,
                    "start_time": process_start_time.strftime(config.TIME_FORMAT),
                    "end_time": process_end_time.strftime(config.TIME_FORMAT)
                }},
                {"data_collection": {
                    "images": collected_result["images"]
                }},
                {"object_detection": {

                }},
                {"result_analysis": {
                    "count": analyzed_result["count"]
                }},
            ],
        }

        os.makedirs(self.__output_path, exist_ok=True)
        with open(os.path.join(self.__output_path, f"{task_name}.txt"), 'w') as f:
            json.dump(result_json, f)

        return result_json


if __name__ == "__main__":
    processor = CountPeopleProcessor()
    result = processor.process("example")
    print(result)
