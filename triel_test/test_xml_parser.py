from triel.suite.xml_parser import XmlParser
from triel_test.resources_test import resource_test_path

if __name__ == '__main__':
    xmlParser = XmlParser()
    print("\n ====  Vunit ok  ====  sim-> ghdl\n")
    print(xmlParser.vunit_xml(resource_test_path("xml/out.xml"), "ghdl", resource_test_path("")))
    print("\n ==== Vunit fail ====  sim-> ghdl\n")
    print(xmlParser.vunit_xml(resource_test_path("xml/out_fail.xml"), "ghdl", resource_test_path("")))
    print("\n ====  Vunit ok  ====  sim-> modelsim\n")
    print(xmlParser.vunit_xml(resource_test_path("xml/out.xml"), "modelsim", resource_test_path("")))
    print("\n ==== Vunit fail ====  sim-> modelsim\n")
    print(xmlParser.vunit_xml(resource_test_path("xml/out_fail.xml"), "modelsim", resource_test_path("")))
    print("\n ====  coco ok   ====\n")
    print(xmlParser.coco_xml(resource_test_path("xml/results.xml"), resource_test_path("xml/func.vcd")))
    print("\n ==== coco fail  ====\n")
    print(xmlParser.coco_xml(resource_test_path("xml/results_fail.xml"), resource_test_path("xml/func.vcd")))
