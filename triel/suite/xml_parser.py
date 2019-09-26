import os.path
import xml.etree.ElementTree as et


class XmlParser:
    def __init__(self):
        self.data = {}

    def parse(self, xml_file):
        tree = et.parse(xml_file)
        base = tree.getroot()
        return base

    def coco_xml(self, xml_file, wave_file):
        base = self.parse(xml_file)
        self.data["summary"] = []
        self.data["test"] = []
        num_test = 0
        num_fail = 0
        for cases in base.iter("testcase"):
            num_test = num_test + 1
            for std in cases:
                num_fail = num_fail + 1
            self.data["test"].append({"classname": cases.attrib["classname"], "name": cases.attrib["name"],
                                      "time": cases.attrib["time"][0:6],
                                      "test": "Failed" if cases.findall('failure') else " OK",
                                      "stdout": std.attrib["stdout"] if cases.findall('failure') else " Test passed",
                                      "waveform": wave_file})
        self.data["summary"] = {"test": num_test, "failures": num_fail, "errors": "--", "skipped": "--"}

        return self.data

    def edalize_xml(self, stdout_value, wave_file):
        self.data["summary"] = {"test": 1, "failures": "", "errors": "", "skipped": ""}
        self.data["test"] = []
        self.data["test"].append(
            {"classname": "", "name": "", "time": "", "test": "", "stdout": stdout_value, "waveform": wave_file})
        return self.data

    def vunit_xml(self, xml_file, simulator, vunit_out_path):
        base = self.parse(xml_file)
        map_file_path = os.path.join(vunit_out_path, "vunit_out", "test_output", "test_name_to_path_mapping.txt")
        map_file = open(map_file_path, "r")
        test_map = {}
        for lines in map_file.readlines():
            test_map[lines.split()[1]] = os.path.join(vunit_out_path, "vunit_out", "test_output", lines.split()[0],
                                                      simulator, "wave.vcd")
        self.data["summary"] = []
        self.data["test"] = []
        self.data["summary"] = {"test": base.attrib["tests"], "failures": base.attrib["failures"],
                                "errors": base.attrib["errors"], "skipped": base.attrib["skipped"]}
        for cases in base.iter("testcase"):
            for std in cases.iter("system-out"):
                self.data["test"].append(
                    {"classname": cases.attrib["classname"], "name": cases.attrib["name"], "time": cases.attrib["time"],
                     "test": "Failed" if cases.findall('failure') else " OK", "stdout": std.text,
                     "waveform": test_map[cases.attrib["classname"] + "." + cases.attrib["name"]]})

        return self.data
