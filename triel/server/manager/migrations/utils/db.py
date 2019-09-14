def create(apps, model_str, **kwargs):
    AbsModel = apps.get_model('manager', model_str)
    result_list = AbsModel.objects.filter(**kwargs)
    if not result_list:
        result = AbsModel(**kwargs)
        result.save()
    else:
        result = result_list[0]
    return result
