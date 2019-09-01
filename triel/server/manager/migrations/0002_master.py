from django.db import migrations

LANG_VHDL = "vhdl"
LANG_VERILOG = "verilog"


def load_data(apps, schema_editor):
    vhdl_lang = create(apps, 'Language', name=LANG_VHDL)
    create(apps, 'Language', name=LANG_VERILOG)
    ghdl_sim = create(apps, 'Simulator', name='ghdl')
    create(apps, 'SimulatorLanguage', simulator=ghdl_sim, language=vhdl_lang)

    vunit_suite = create(apps, 'Suite', name="vunit")
    cocotb = create(apps, 'Suite', name="cocotb")
    edalize = create(apps, 'Suite', name="edalize")

    create(apps, 'SuiteSimulator', suite=vunit_suite, simulator=ghdl_sim)
    create(apps, 'SuiteSimulator', suite=cocotb, simulator=ghdl_sim)
    create(apps, 'SuiteSimulator', suite=edalize, simulator=ghdl_sim)


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
