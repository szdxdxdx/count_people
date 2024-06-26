import os
from ultralytics import YOLO
import config


class ObjectPredictor:
    def __init__(self):
        self.__model = YOLO(config.MODEL_PATH)
        self.__input_path = config.COLLECTED_DATA_FOLDER_PATH
        self.__output_path = config.PREDICTED_RESULT_FOLDER_PATH

    def predict(self, task_name: str):

        print(f"开始对收集到的图片进行预测分析")

        input_path = os.path.join(self.__input_path, task_name)
        assert os.path.exists(input_path)

        output_path = os.path.join(self.__output_path, task_name)
        img_save_path = os.path.join(output_path, "img")
        txt_save_path = os.path.join(output_path, "txt")
        os.makedirs(img_save_path, exist_ok=True)
        os.makedirs(txt_save_path, exist_ok=True)

        results = self.__model.predict(source=input_path)
        for result in results:
            file_name = os.path.basename(result.path)
            result.save(os.path.join(img_save_path, file_name))
            result.save_txt(os.path.join(txt_save_path, file_name + ".txt"))

        print(f"预测分析结束，结果存于{output_path}")

        return {
            "output_path": {
                "img": img_save_path,
                "txt": txt_save_path,
            }
        }


if __name__ == '__main__':
    predictor = ObjectPredictor()
    predicted_result = predictor.predict("example")
    print(predicted_result)
