import json
import os

BASE_DIR = os.path.dirname(os.path.dirname(__file__))

V2_DIR = os.path.join(BASE_DIR, "v2")


class KnowledgeBase:

    def __init__(self):

        self.components = []
        self.faults = []
        self.symptoms = []
        self.repairs = []
        self.costs = []
        self.aliases = []

    def load_json(self, filename):

        path = os.path.join(V2_DIR, filename)

        if not os.path.exists(path):
            return []

        with open(path, encoding="utf-8") as f:
            return json.load(f)

    def load(self):

        self.components = self.load_json("components.json")
        self.faults = self.load_json("faults.json")
        self.symptoms = self.load_json("symptoms.json")
        self.repairs = self.load_json("repairs.json")
        self.costs = self.load_json("costs.json")
        self.aliases = self.load_json("aliases.json")

    def get_component(self, code):

        for item in self.components:
            if item["code"] == code:
                return item

        return None

    def get_fault(self, code):

        for item in self.faults:
            if item["code"] == code:
                return item

        return None

    def get_repair(self, fault):

        for item in self.repairs:
            if item["fault"] == fault:
                return item

        return None

    def get_cost(self, fault):

        for item in self.costs:
            if item["fault"] == fault:
                return item

        return None

    def search_alias(self, keyword):

        keyword = keyword.lower()

        for item in self.aliases:

            if item["keyword"].lower() == keyword:
                return item

        return None


knowledge = KnowledgeBase()
knowledge.load()
