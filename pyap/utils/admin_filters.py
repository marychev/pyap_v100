"""
Расширение:
from daterange_filter.filter import DateRangeFilter
`````````````````````````````````````````````````````
Расширение стандартного Модуля ДЖАНГИ!
Форма и Фильтр только для Времи: ```model:TimeField```
"""

import datetime
from django.utils.translation import ugettext as _
from daterange_filter.filter import admin, models, forms, static
from django.contrib.admin.widgets import AdminTimeWidget


FILTER_PREFIX = 'trf__'


def clean_input_prefix(input_):
    return dict((key.split(FILTER_PREFIX)[1] if key.startswith(FILTER_PREFIX) else key, val)
                for (key, val) in input_.items())


class TimeRangeFilterBaseForm(forms.Form):
    def __init__(self, request, *args, **kwargs):
        super(TimeRangeFilterBaseForm, self).__init__(*args, **kwargs)
        self.request = request

    @property
    def media(self):
        try:
            if getattr(self.request, 'daterange_filter_media_included'):
                return forms.Media()
        except AttributeError:
            setattr(self.request, 'daterange_filter_media_included', True)

            js = ["calendar.js", "admin/DateTimeShortcuts.js"]
            css = ['widgets.css']

            return forms.Media(
                js=[static("admin/js/%s" % path) for path in js],
                css={'all': [static("admin/css/%s" % path) for path in css]}
            )


class TimeRangeForm(TimeRangeFilterBaseForm):

    def __init__(self, *args, **kwargs):
        field_name = kwargs.pop('field_name')
        super(TimeRangeForm, self).__init__(*args, **kwargs)

        self.fields['%s%s__gte' % (FILTER_PREFIX, field_name)] = forms.TimeField(
            label='',
            widget=AdminTimeWidget(
                attrs={'placeholder': _('From time')}
            ),
            localize=True,
            required=False
        )

        self.fields['%s%s__lte' % (FILTER_PREFIX, field_name)] = forms.TimeField(
            label='',
            widget=AdminTimeWidget(
                attrs={'placeholder': _('To time')}
            ),
            localize=True,
            required=False,
        )


class TimeRangeFilter(admin.filters.FieldListFilter):
    template = 'daterange_filter/filter.html'

    def __init__(self, field, request, params, model, model_admin, field_path):
        self.lookup_kwarg_since = '%s%s__gte' % (FILTER_PREFIX, field_path)
        self.lookup_kwarg_upto = '%s%s__lte' % (FILTER_PREFIX, field_path)
        super(TimeRangeFilter, self).__init__(
            field, request, params, model, model_admin, field_path)
        self.form = self.get_form(request)

    def choices(self, cl):
        """
        Pop the original parameters, and return the date filter & other filter
        parameters.
        """

        cl.params.pop(self.lookup_kwarg_since, None)
        cl.params.pop(self.lookup_kwarg_upto, None)
        return ({
                    'get_query': cl.params,
                },)

    def expected_parameters(self):
        return [self.lookup_kwarg_since, self.lookup_kwarg_upto]

    def get_form(self, request):
        return TimeRangeForm(request, data=self.used_parameters,
                             field_name=self.field_path)

    def queryset(self, request, queryset):
        if self.form.is_valid():
            # get no null params
            filter_params = clean_input_prefix(dict(filter(lambda x: bool(x[1]), self.form.cleaned_data.items())))

            # filter by upto included
            lookup_upto = self.lookup_kwarg_upto.lstrip(FILTER_PREFIX)
            if filter_params.get(lookup_upto) is not None:
                lookup_kwarg_upto_value = filter_params.pop(lookup_upto)
                filter_params['%s__lt' % self.field_path] = lookup_kwarg_upto_value + datetime.timedelta(hours=1)

            return queryset.filter(**filter_params)
        else:
            return queryset


# register the filters
admin.filters.FieldListFilter.register(
    lambda f: isinstance(f, models.TimeField), TimeRangeFilter)

