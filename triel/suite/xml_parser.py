# -*- coding: utf-8 -*-
import xml.etree.ElementTree as et
import json

class xml_parser:
    def __init__ (self,xml_file,simulator):
        self.xml_file = xml_file
        self.json_out = ""
        self.data = {}
        self.simulator = simulator

    def parse(self):
        tree = et.parse(self.xml_file)
        base = tree.getroot()
        return base

    def coco_xml(self):
        base = self.parse()
        self.data["summary"]=[]
        self.data["test"]  =[]
        num_test=0
        num_fail=0
        for cases in base.iter("testcase"):
            num_test=num_test+1
            for std in cases:
                num_fail=num_fail+1
            self.data["test"].append({"classname":cases.attrib["classname"],"name":cases.attrib["name"],"time":cases.attrib["time"][0:6],"test":cases.attrib["classname"],"stdout":std.attrib["stdout"] if cases.findall('failure') else " Test passed","waveform":cases.attrib["classname"]})
        self.data["summary"] = {"test":num_test,"failures":num_fail}

        self.json_out = json.dumps(self.data)
        return self.json_out

    def vunit_xml(self):
        base = self.parse()
        self.data["summary"]=[]
        self.data["test"]  =[]
        self.data["summary"] = {"test":base.attrib["tests"],"failures":base.attrib["failures"]}
        for cases in base.iter("testcase"):
            for std in cases:
                self.data["test"].append({"classname":cases.attrib["classname"],"name":cases.attrib["name"],"time":cases.attrib["time"],"test":"FAIL!!","stdout":std.text,"waveform":cases.attrib["classname"]})

        self.json_out = json.dumps(self.data)
        return self.json_out
