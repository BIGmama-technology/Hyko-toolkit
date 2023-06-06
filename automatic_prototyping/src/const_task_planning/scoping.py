import json
from pathlib import Path
from typing import Dict, List, Tuple


class ScopeBook:
    r"""
    ScopeBook Class DOCstring
    """

    SCOPEBOOK_CACHE_DIR = Path("./scopebooks")
    RAW_JSON: Dict = dict()
    scopebook_title: str = None
    scopebook_background: str = None
    scopebook_context: str = None
    scopebook_operational_pbs: List[str] = None
    json_file = None
    scopebook_body: List[Tuple[str, List[str]]] = list()

    def __init__(self, json_file: str = None, json_: Dict = None):
        if json_file and json_:
            raise ValueError(
                "json_file and json_ arguments can be fed at the same time to the constructor"
            )
        if json_file:
            self.json_file = self.SCOPEBOOK_CACHE_DIR / json_file
        elif json_:
            self.RAW_JSON = json_

        self.structure_scopebook()

    def load_json(self, json_file: str = None) -> Dict:
        with open(self.json_file, "r") as file_:
            self.RAW_JSON = json.load(file_)

    def parse_json(self, raw_json: Dict) -> Dict:
        r"""
        parse JSON file and get scopeBook Question-List[Answers]
        """
        self.scopebook_title = raw_json["data"]["blocks"]["data"][0]["children"][0][
            "text"
        ]
        data = raw_json["data"]["blocks"]["data"][1:]

        for i, data_ in enumerate(data):
            if data_["type"] == "question":
                if data_["children"][0]["text"] == "Background:":
                    self.scopebook_background = data[i + 1]["children"][0]["text"]
                elif data_["children"][0]["text"] == "'Name of the project:":
                    self.scopebook_title = data[i + 1]["children"][0]["text"]
                else:
                    question = data_["children"][0]["text"]
                    answers = []
                    for prob_answer in data[i + 1 :]:
                        if prob_answer["type"] == "paragraph":
                            answers.append(prob_answer["children"][0]["text"])
                        elif (
                            prob_answer["type"] != "paragraph"
                            or prob_answer["type"] == "question"
                        ):
                            break

                    self.scopebook_body.append([question, answers])

    def fix_context(self):
        r"""
        Get context of the ScopeBook obj, returns the answers value for the first elemenet (index=0)
        in self.scopebook.body_
        """
        self.scopebook_context = self.scopebook_body[0][1][0]
        self.scopebook_body = self.scopebook_body[1:]

    def fix_operational_problems(self):
        self.scopebook_operational_pbs = self.scopebook_body[0]

    def structure_scopebook(self) -> Dict:
        if self.json_file:
            self.load_json(json_file="scopebook1.json")

        self.parse_json(self.RAW_JSON)

        # ignore first item in self.scopebook.body_ (name of the project -> scopebook_title)
        self.scopebook_body = self.scopebook_body[1:]
        self.fix_context()
        self.fix_operational_problems()

    def __repr__(self):
        return f"""
                
                """


if __name__ == "__main__":
    scopeb = ScopeBook(json_file="scopebook1.json")
    # scopeb.structure_scopebook()

    print(scopeb.scopebook_context)
    print(scopeb.scopebook_operational_pbs)
