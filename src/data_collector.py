import os
import urllib.parse
import requests
from tqdm import tqdm
import config


class DataCollector:

    def __init__(self):
        self.__output_path = config.COLLECTED_DATA_FOLDER_PATH
        self.__keyword = "工人 工地 照片"
        self.__page_size = 15
        self.__curr_page = 1

    @staticmethod
    def __make_req(key_word: str, page_num: int, page_size: int) -> dict:
        url_encoded_str = urllib.parse.quote(key_word)
        return {
            "headers": {
                "Host": "image.baidu.com",
                "Referer": "https://image.baidu.com/search/index?tn=baiduimage&ipn=r&ct=201326592&cl=2&lm=-1&st=-1&fm=result&fr=&sf=1&fmq=1717829201342_R&pv=&ic=&nc=1&z=&hd=&latest=&copyright=&se=1&showtab=0&fb=0&width=&height=&face=0&istype=2&dyTabStr=MCwzLDEsMiw2LDQsNSw3LDgsOQ%3D%3D&ie=utf-8&sid=&word=%E5%B7%A5%E5%9C%B0+%E5%B7%A5%E4%BA%BA+%E7%85%A7%E7%89%87",
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36 Edg/125.0.0.0",
                "Cookie": """BAIDUID=9D823185D6C840F325112B29226B74AA:FG=1; BAIDUID_BFESS=9D823185D6C840F325112B29226B74AA:FG=1; __bid_n=1900c76af8e92968519ef6; RT="z=1&dm=baidu.com&si=6ac0a749-d009-459a-891d-8539bbc8d535&ss=lxbtjrrp&sl=5&tt=73b&bcn=https%3A%2F%2Ffclog.baidu.com%2Flog%2Fweirwood%3Ftype%3Dperf&ld=12ff&ul=143t&hd=1440"; BIDUPSID=9D823185D6C840F325112B29226B74AA; BDRCVFR[X_XKQks0S63]=mk3SLVN4HKm; BDRCVFR[dG2JNJb_ajR]=mk3SLVN4HKm; BDRCVFR[-pGxjrCMryR]=mk3SLVN4HKm; userFrom=images.baidu.com; ab_sr=1.0.1_ODA5ZTUxNWEwYzFhZmUzZjc3MjQzY2VjNzYzZGMyOGQ0NWYxNDAxNjVmZGUyNWFjNWY3NzAxMzFjMTg5M2I5YzU3ZTVhOWM5Mjk0ZDQ2YTEyMTc4NjdjMTA5ZTQ4YjU4YjdjZjQzNzdhZGQ1ZTYwMjIzODU2MTcyODk2ZTRhODNkMDNhZmJlZTZjNDViNmQ0Njc2NDY0YWEyYzAxMjQ2MQ==; rsv_i=2bf11We3sa5O/5KUrsbu+Gpaai2bB2V7Kvo0PE819lJjRN2HinLAHBbqdYuXMzXQuQ7xOCJ/U+ZcQOo3WAvptxs/IOVQq+4; BA_HECTOR=a58h2l212h20850h000581211v08oh1j6tqfj1u; BDORZ=AE84CDB3A529C0F8A2B9DCDD1D18B695; ZFY=vIP9YdgYSeIQV9R1yEM6:BzZ:BuM4BtrKfl7Ga665rrdo:C; SE_LAUNCH=5%3A28642414_16%3A28642414; delPer=0; PSINO=6; H_WISE_SIDS=110085_282466_607896_607747_607985_608327_608375_608443_608152_301667_608696_305467_607532_8000054_8000124_8000137_8000149_8000161_8000162_8000175_8000181_8000203; H_WISE_SIDS_BFESS=110085_282466_607896_607747_607985_608327_608375_608443_608152_301667_608696_305467_607532_8000054_8000124_8000137_8000149_8000161_8000162_8000175_8000181_8000203; IMG_WH=1280_609"""
            },
            "url": f"https://image.baidu.com/search/acjson?tn=resultjson_com&logid=10453765462755083880&ipn=rj&ct=201326592&is=&fp=result&fr=&word={url_encoded_str}&queryWord={url_encoded_str}&cl=2&lm=&ie=utf-8&oe=utf-8&adpicid=&st=-1&z=&ic=0&hd=&latest=&copyright=&s=&se=&tab=&width=&height=&face=0&istype=2&qc=&nc=1&expermode=&nojc=&isAsync=&pn={page_num * page_size}&rn={page_size}&gsm=1e&1717851020996="
        }

    def collect(self, task_name: str) -> dict:

        print(f"开启新一轮的数据收集任务（使用爬虫爬取若干张图片）")

        req = self.__make_req(self.__keyword, self.__curr_page, self.__page_size)
        resp = requests.get(**req).json()
        image_list = resp["data"][:-1]

        output_path = os.path.join(self.__output_path, task_name)
        os.makedirs(output_path, exist_ok=True)

        file_name_list = []
        idx = 1
        for data in tqdm(image_list):
            img_url = data["middleURL"]
            img_type = data["type"]

            file_name = f"{idx}.{img_type}"
            file_name_list.append(file_name)

            img_data = requests.get(url=img_url).content

            save_file_path = os.path.join(output_path, file_name)
            with open(save_file_path, mode="wb") as f:
                f.write(img_data)

            idx += 1

        self.__curr_page += 1

        print(f"数据收集结束，结果存于{output_path}")

        return {
            "images": file_name_list
        }


if __name__ == "__main__":
    collector = DataCollector()
    result = collector.collect("example")
    print(result)
