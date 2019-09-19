# Triel

A web-server for HDL simulation with VUnit, Cocotb and Edalize.

# API

## Languages
```
GET http://triel:port/languages/
```
```json
[{"id":1,"name":"vhdl"},{"id":2,"name":"verilog"}]
```

## Simulators
```
GET http://triel/port/simulators/
```
```json
[{"id":1,"languages":[{"id":1,"name":"vhdl"}],"name":"ghdl","path":null},{"id":2,"languages":[{"id":2,"name":"verilog"}],"name":"icarus","path":null}]
```

## Suites
```
GET http://triel/port/suites/
```
```json
[{"id":1,"simulators":[{"id":1,"name":"ghdl"}],"name":"vunit"},{"id":2,"simulators":[{"id":1,"name":"ghdl"},{"id":2,"name":"icarus"}],"name":"cocotb"},{"id":3,"simulators":[{"id":1,"name":"ghdl"}],"name":"edalize"}]
```

## Tests de Coco
```
GET http://triel/port/coco/
```
```json
[{"id":1,"name":"test_adder_vlog","language":2,"top_level":"adder","simulator":2,"module":"/mnt/data/Programacion/teros/triel/triel_test/scripts/cocotb/simple/test_adder.py","tests":[],"options":[],"files":[{"path":"/mnt/data/Programacion/teros/triel/triel_test/hdl/adder.v"}],"result":"<testsuites name=\"results\">\n  <testsuite name=\"all\" package=\"all\" tests=\"0\">\n    <property name=\"random_seed\" value=\"1568834801\" />\n    <testcase classname=\"test_adder\" name=\"adder_basic2_test\" ratio_time=\"88271014170252.97\" sim_time_ns=\"401000000000.0\" time=\"0.004542827606201172\" />\n    <testcase classname=\"test_adder\" name=\"adder_basic_test\" ratio_time=\"123788614410833.89\" sim_time_ns=\"401000000000.0\" time=\"0.0032393932342529297\" />\n    <testcase classname=\"test_adder\" name=\"adder_random_test\" ratio_time=\"122040916715139.34\" sim_time_ns=\"2201000000000.0\" time=\"0.018034934997558594\" />\n  </testsuite>\n</testsuites>\n"},{"id":2,"name":"test_adder_vhdl","language":1,"top_level":"adder","simulator":1,"module":"/mnt/data/Programacion/teros/triel/triel_test/scripts/cocotb/simple/test_adder.py","tests":[],"options":[],"files":[{"path":"/mnt/data/Programacion/teros/triel/triel_test/hdl/adder.vhd"}],"result":"<testsuites name=\"results\">\n  <testsuite name=\"all\" package=\"all\" tests=\"0\">\n    <property name=\"random_seed\" value=\"1568834806\" />\n    <testcase classname=\"test_adder\" name=\"adder_basic2_test\" ratio_time=\"0.07139771210255974\" sim_time_ns=\"0.000401\" time=\"0.005616426467895508\" />\n    <testcase classname=\"test_adder\" name=\"adder_basic_test\" ratio_time=\"0.08427276801282693\" sim_time_ns=\"0.000401\" time=\"0.004758358001708984\" />\n    <testcase classname=\"test_adder\" name=\"adder_random_test\" ratio_time=\"0.08884116467780429\" sim_time_ns=\"0.002201\" time=\"0.024774551391601562\" />\n  </testsuite>\n</testsuites>\n"}]
```
