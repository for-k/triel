from django.db import migrations

from triel.server.manager.migrations.utils.db import create


def load_data(apps, schema_editor):
    vhdl_lang = create(apps, 'Language', name="vhdl")
    verilog_lang = create(apps, 'Language', name="verilog")

    ghdl_sim = create(apps, 'Simulator', name='ghdl')
    ghdl_sim.languages.add(vhdl_lang)
    ghdl_sim.save()

    vunit_suite = create(apps, 'Suite', name="vunit")
    vunit_suite.simulators.add(ghdl_sim)
    vunit_suite.save()

    cocotb = create(apps, 'Suite', name="cocotb")
    cocotb.simulators.add(ghdl_sim)
    cocotb.save()

    edalize = create(apps, 'Suite', name="edalize")
    edalize.simulators.add(ghdl_sim)
    edalize.save()


class Migration(migrations.Migration):
    initial = False

    dependencies = [
        ('manager', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(load_data),
    ]
