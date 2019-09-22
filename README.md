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
{'id': 1, 'languages': [{'id': 1, 'name': 'vhdl'}], 'name': 'ghdl', 'path': None}
```

## Suites
```
GET http://triel/port/suites/
```
```json
{'id': 1, 'simulators': [{'id': 1, 'name': 'ghdl', 'languages': [{'id': 1, 'name': 'vhdl'}]}], 'name': 'vunit'}
```

## Tests de Coco
```
GET http://triel/port/coco/
```
```json
{
    "id": 1,
    "working_dir": "/mnt/data/Programacion/teros/triel/triel_test/scripts/cocotb/simple",
    "modules": [{"path": "/mnt/data/Programacion/teros/triel/triel_test/scripts/cocotb/simple/test_adder.py"}],
    "sources": [{"path": "/mnt/data/Programacion/teros/triel/triel_test/hdl/adder.vhd"}],
    "top_level": "adder",
    "simulator": "ghdl",
    "simulator_args": [{"argument": "--vcd", "value": "func.vcd"}],
}
```
