from django.db import migrations


def load_data(apps, schema_editor):
    vhdl_lang = create(apps, 'Language', name="vhdl")
    verilog_lang = create(apps, 'Language', name="verilog")

    ghdl_sim = create(apps, 'Simulator', name='ghdl')
    ghdl_sim.languagues.add(vhdl_lang)
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


def create(apps, model_str, **kwargs):
    AbsModel = apps.get_model('manager', model_str)
    result_list = AbsModel.objects.filter(**kwargs)
    if not result_list:
        result = AbsModel(**kwargs)
        result.save()
    else:
        result = result_list[0]
    return result


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        ('manager', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(load_data),
    ]
