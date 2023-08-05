from django.core.management import (
    BaseCommand,
)
from m3_gar_client.constants import (
    GAR_LEVELS_PLACE,
)
from m3_gar.models import (
    AddrObj,
    AddrObjParams,
    ParamTypes,
)
from m3_gar.models.hierarchy import (
    MunHierarchy,
    AdmHierarchy
)


def chunks(lst, n):
    """Разбивает лист на несколько листов размером n"""
    for i in range(0, len(lst), n):
        yield lst[i:i + n]


class Command(BaseCommand):
    """
    Команда для обновления поля name_with_parents в моделях иерархий

    Доступные аргументы:
    --adm - поля обновляются для административной иерархии
    --guids - можно через запятую указать guid-ы объектов, для которых нужно обновить поле
    --levels - можно через запятую указать уровни объектов, для которых нужно обновить поле
    """
    help = 'Утилита для заполнения дополнительного поля name_with_parents в модели Hierarchy'

    def add_arguments(self, parser):
        super().add_arguments(parser)

        parser.add_argument(
            '--adm',
            action='store_true',
            default=None,
            help='Add objects guid for filter columns for adding data',
        )

        parser.add_argument(
            '--guids',
            default=None,
            help='Add objects guid for filter columns for adding data',
        )

        parser.add_argument(
            '--levels',
            default=None,
            help='Add objects level for filter columns for adding data',
        )

    def get_name_with_parents(self, obj):

        CODE_PARAM_TYPES_OFFICIAL = 'Official'
        result_parts = []

        for item in obj.get_ancestors(include_self=True):
            try:
                addr_obj = AddrObj.objects.get(
                    objectid=item.objectid_id,
                    isactual=True,
                )
                official_type = ParamTypes.objects.filter(code=CODE_PARAM_TYPES_OFFICIAL, isactive=True)
                official_param = None
                if official_type:
                    official_param = AddrObjParams.objects.filter(
                        objectid=item.objectid_id,
                        typeid=official_type.get(),
                    )
            except Exception as err:
                self.stdout.write(f'В ходе выполнения команды возникла ошибка: {err}')
            else:
                if addr_obj:
                    type_name = addr_obj.type_full_name
                    # Если Респ, то Республика, а если г., то город
                    if addr_obj.typename and addr_obj.typename[0].islower():
                        type_name = type_name.lower()

                    # Делаем так, чтобы не "область Кировская", а "Кировская область"
                    # Впрочем, если есть официальное название, то используем его.
                    # Перестановки остаются на уровне районов, городов и т.д.
                    if official_param:
                        for actual_param in official_param:
                            # Может быть два официальных названия: Пермский край и Пермская область. Используем то,
                            # которое используется на данный момент. При этом заранее присваиваем наименование,
                            # чтобы не возникла ошибка, когда в рамках цикла по какой-либо причине условие не выполнится.
                            official_name = actual_param.value
                            if type_name.lower() in actual_param.value.lower():
                                official_name = actual_param.value
                                break

                        addr_obj_name = f'{official_name}'
                    elif addr_obj.is_prefix_type:
                        addr_obj_name = f'{type_name} {addr_obj.name}'
                    else:
                        addr_obj_name = f'{addr_obj.name} {type_name}'

                    result_parts.append(addr_obj_name)

        result = ', '.join(result_parts)

        return result

    def handle(self, *args, adm, guids, levels, **options):

        # Муниципальная модель иерархии по умолчанию
        hierarchy_model = MunHierarchy
        if adm:
            hierarchy_model = AdmHierarchy

        if guids:
            guids_list = guids.split(',')
            object_ids = AddrObj.objects.filter(
                objectguid__in=guids_list, level__in=GAR_LEVELS_PLACE
            ).values_list('objectid', flat=True)
            data = hierarchy_model.objects.filter(objectid__in=object_ids)

        elif levels:
            levels_list = levels.split(',')
            object_ids = AddrObj.objects.filter(level__in=levels_list).values_list('objectid', flat=True)
            data = hierarchy_model.objects.filter(objectid__in=object_ids)

        else:
            data = hierarchy_model.objects.filter(level__in=GAR_LEVELS_PLACE)

        self.stdout.write(f'Запущено обновление полей name_with_parents для модели {hierarchy_model.__name__}')

        lines_for_update = []
        for lines_list in chunks(data, 500):
            for line in lines_list:
                name_with_parents_value = self.get_name_with_parents(line)
                if line.name_with_parents != name_with_parents_value:
                    line.name_with_parents = name_with_parents_value
                    lines_for_update.append(line)
            self.stdout.write(f'На необходимость обновления проверено {len(lines_list)} записей')

        self.stdout.write(f'Будет обработано {len(lines_for_update)} записей')

        for update_list in chunks(lines_for_update, 500):
            hierarchy_model.objects.bulk_update(
                objs=update_list,
                fields=(
                    'name_with_parents',
                ),
            )
            self.stdout.write(f'{len(update_list)} полей записаны успешно')
