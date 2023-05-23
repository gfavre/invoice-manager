from django.core.exceptions import FieldDoesNotExist
from django.utils.dateparse import parse_datetime
from django.utils.timezone import now

from rest_framework_datatables.filters import DatatablesFilterBackend


def cleanup_value(model_class, accessor, values):
    if "__" in accessor:
        parent_field_name, child_field_name = accessor.split("__")[0], "__".join(
            accessor.split("__")[1:]
        )
        # noinspection PyProtectedMember
        query_filter, cleaned_values = cleanup_value(
            model_class._meta.get_field(parent_field_name).related_model,
            child_field_name,
            values,
        )
        return f"{parent_field_name}__{query_filter}", cleaned_values
    # noinspection PyProtectedMember
    model_field = model_class._meta.get_field(accessor)

    if hasattr(model_field, "choices") and model_field.choices:
        return f"{accessor}__in", values
    if model_field.get_internal_type() == "BooleanField":
        return f"{accessor}__in", [bool(int(value)) for value in values]
    if model_field.get_internal_type() == "DateTimeField":
        the_date = parse_datetime(values[0])
        if the_date > now():
            return f"{accessor}__isnull", True
        return f"{accessor}__gte", the_date
    if model_field.get_internal_type() == "ForeignKey":
        return f"{accessor}__in", values
    if model_field.get_internal_type() == "UUIDField":
        return f"{accessor}", values[0]
    return accessor, values


class DatatablesFilterAndPanesBackend(DatatablesFilterBackend):
    def filter_queryset(self, request, queryset, view):
        queryset = super().filter_queryset(request, queryset, view)
        if request.method == "POST":
            request_data = request.data
        else:
            request_data = request.query_params
        getter = request_data.get
        fields = self.get_fields(request)
        for field in fields:
            pane_name = field["data"]
            pane_data_accessor = field["name"][0]
            count = 0
            values = []
            while True:
                pane_value = getter(f"searchPanes[{pane_name}][{count}]")
                if not pane_value:
                    break
                values.append(pane_value)
                count += 1
            if values:
                try:
                    accessor, values = cleanup_value(queryset.model, pane_data_accessor, values)
                    queryset = queryset.filter(**{accessor: values})
                except FieldDoesNotExist:
                    # We are tring to filter on a calculated field
                    params = getattr(queryset.model, f"get_{pane_data_accessor}_query_params")(
                        values
                    )
                    queryset = queryset.filter(**params)

        filtered_count = queryset.count()
        view._datatables_filtered_count = filtered_count
        return queryset
