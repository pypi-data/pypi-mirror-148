import datetime
import json
import os
from itertools import chain

import numpy as np
import pandas as pd
from progressbar import ProgressBar

from ..utils import filtering_category
from ._ner import sentence_to_nerlist
from ._textrank import sort_sentence_importance
from .countryset import morethan_two_countries


class NewspieacePreprocess:
    """크롤링한 원자료를 전처리 하기 위한 모듈입니다.

    이 모듈에서 데이터를 받아오는 방식은 크게 3개입니다.
    1. 첫번째 방식은 기존 pandas dataframe 객체를 받아오는 방식입니다.
        이 방식을 사용하기 위해서 NewspieacePreprocess(data = 객체명)을 사용해야 합니다.
    2. json_path를 입력해서 json file이 있는 파일을 받아오는 방식입니다.
        이 방식을 사용하기 위해서는 NewspieacePreprocess(json_path= 파일 폴더 경로, csv_path = 저장될 원자료 csv 경로, is_json = True)를 입력해줘야 합니다.
    3. csv_path를 입력하여 이미 저장되어 있는 csv를 불러오는 방식입니다.
        이 방식을 사용하기 위해서는 NewspieacePreprocess(csv_path= 저장되어 있는 원자료 csv 경로, is_csv = True)를 입력해줘야 합니다.

    본 프로젝트에서는 국제정치 뉴스만 고르기 위해서 신문기사를 필터링 합니다. 필터링 하는 키워드는 utils에 있으며, 필터링 기능을 사용하기 위해서 class의 use_filtering params를 사용합니다.


    Parameters
    ---------
    data: pands_dataframe
        판다스 dataframe으로 저장되어 있는 객체입니다.
    json_path: str
        json 파일들이 모여있는 폴더입니다.
    csv_path: str
        불러올, 저장될 csv파일이 있는 경로입니다. 불러올때는 csv 경로를, 저장할 때는 csv가 저장될 폴더를 정해줍니다.
    is_csv: Boolean
        불러올 파일이 csv로 이미 모여있을 경우에 입력합니다. 이 경우, json_path와 csv_path를 정확히 입력해야 합니다.
    is_json: Boolean
        불러올 파일들이 json일때 사용합니다.이 경우 csv_path를 정확히 입력해야 합니다.
    use_filtering: Boolean
        불러온 데이터를 필터링 할때 사용합니다.
    """

    def __init__(
        self,
        data=None,
        json_path=None,
        csv_path=None,
        is_csv=False,
        is_json=False,
        use_filtering=False,
    ):
        self.use_filtering = use_filtering

        if is_csv == True:
            self.csv_data = pd.read_csv(csv_path)
            if use_filtering == True:
                self.csv_data = filtering_category(self.csv_data)
        elif is_json == True:
            self.csv_data = self.get_jsondata(json_path, csv_path)
        else:
            self.csv_data = data

    def get_jsondata(self, json_path, csv_path):
        """
        # Description: 주어진 path에 위치한 json data를 반환합니다.

        -------------
        # argument
        - path: json data가 위치한 경로
        -------------
        # Return
        : 지정한 path에 위치한 train.csv data
        """
        json_files = [
            pos_json for pos_json in os.listdir(json_path) if pos_json.endswith(".json")
        ]

        json_data = pd.DataFrame(
            columns=["date", "title", "content", "source", "url", "category"]
        )

        # we need both the json and an index number so use enumerate()
        for index, js in enumerate(json_files):
            with open(os.path.join(json_path, js), encoding="UTF8") as json_file:
                json_text = json.load(json_file)

                # here you need to know the layout of your json and each json has to have
                # the same structure (obviously not the structure I have here)
                date = json_text["date"]
                title = json_text["title"]
                content = json_text["content"]
                source = json_text["source"]
                url = json_text["url"]
                category = json_text["category"].lower()

                # here I push a list of data into a pandas DataFrame at row given by 'index'
                json_data.loc[index] = [
                    date,
                    title,
                    content,
                    source,
                    url,
                    category,
                ]
        # 필요 없는 카테고리에 속하는 기사들을 제외한다. 이 카테고리에 대한 부분은 지속적으로 보완해야 한다.
        if self.use_filtering == True:
            json_data = filtering_category(json_data)

        json_data["title"] = json_data["title"].str.replace("\n", " ")
        json_data["content"] = json_data["content"].str.replace("\n", " ")
        json_data.to_csv(
            "{}/{}_raw_date.csv".format(
                csv_path, datetime.date.today().strftime("%Y-%m-%d")
            ),
            index=False,
        )

        return json_data

    def run_preprocessing(self, body_column):  # data = news.json or news.csv
        """주어진 data의 특정 컬럼의 이름을 전처리, 결측치 imputation, feature를 이용한 새로운 변수정의, labeling, 필요없는 컬럼삭제 등을
                       통해 전처리한 data를 반환합니다.
        Parameters
        -------------
        data: train에 사용할 raw data

        Return
        -------------
        ner_df: pandas dataframe
            전처리 후의 데이터
        """
        data = self.csv_data
        print(data["content"])
        ner_df = self.quasiNER_extractor3(data, body_column)
        ner_df["sententce_ner"] = ""
        for a in range(len(ner_df)):
            try:
                ner_df["sententce_ner"][a] = [
                    each
                    for each in model.predict(ner_df["input_text"][a])
                    if each["tag"] != self._tag_filter_value
                ]
            except:
                ner_df["sententce_ner"][a] = ""
        return ner_df

    def corpus_to_nerlist(input_corpus):
        return list(set(chain.from_iterable(map(sentence_to_nerlist, input_corpus))))

    def quasiNER_extractor3(self, body_column):
        """기존에 앞에서 작성한 함수를 연결하여 실행하는 코드이다.

        Parameters
        ---------
        dataframe: pandas dataframe
            국가간 관계가 들어가 있는 데이터 프레임을 넣는다.
        nameof_articlebody_column: str
            데이터 프레임의 칼럼 이름을 넣는다.
        ---------
        Return:
            전처리가 전부 완료된 데이터 프레임
        """
        dataframe = self.csv_data
        dataframe["lowercase_" + body_column] = dataframe[body_column]
        quasinerdf_output_list = []
        dataframe["doc_id"] = ""
        except_sentence = []
        for doc_id in ProgressBar(range(len(dataframe["lowercase_" + body_column]))):
            dataframe["doc_id"][doc_id] = doc_id
            input_text = dataframe["lowercase_" + body_column][doc_id]
            try:
                sentence = " ".join(
                    sort_sentence_importance(input_text, standard="mean", topn=3)
                )
            except:
                except_sentence.append(doc_id)
                sentence = ""

            vectorized_morethan_two_countries = np.vectorize(
                morethan_two_countries, otypes=[list]
            )
            output_list = vectorized_morethan_two_countries(sentence)
            output_df = pd.DataFrame.from_records(
                [output_list], columns=["isvalid", "list_of_countries"]
            )
            output_df["input_text"] = sentence

            output_df["doc_id"] = doc_id
            quasinerdf_output_list.append(output_df)

        quasinerdf_output_df = pd.concat(quasinerdf_output_list)
        quasinerdf_output_df = quasinerdf_output_df[
            quasinerdf_output_df["isvalid"] == True
        ].reset_index(drop=True)
        del quasinerdf_output_df["isvalid"]
        all_df = pd.merge(dataframe, quasinerdf_output_df)
        return all_df
