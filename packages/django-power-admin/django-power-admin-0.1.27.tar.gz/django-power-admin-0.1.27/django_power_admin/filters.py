

from django.contrib.admin import FieldListFilter
from django.utils.translation import gettext_lazy as _

class TextInputFieldFilter(FieldListFilter):
    template = 'django_power_admin/filters/TextInputFieldFilter.html'

    def __init__(self, field, request, params, model, model_admin, field_path):
        super().__init__(field, request, params, model, model_admin, field_path)
        self.input_name = f"{self.field_path}__icontains"
        self.input_value = self.used_parameters.get(self.input_name, "")

    def expected_parameters(self):
        return [f"{self.field_path}__icontains"]
    
    def choices(self, request):
        return []

    class Media:
        css = {
            "all": [
                "django_power_admin/filters/TextInputFieldFilter/css/TextInputFieldFilter.css",
            ]
        }
        js = [
            "django_power_admin/assets/js/parseParam.js",
            "admin/js/vendor/jquery/jquery.js",
            "django_power_admin/filters/TextInputFieldFilter/js/TextInputFieldFilter.js",
            "admin/js/jquery.init.js",
        ]


class DateRangeFilter(FieldListFilter):
    template = 'django_power_admin/filters/DateRangeFilter.html'

    def __init__(self, field, request, params, model, model_admin, field_path,
            input_start_placeholder=_("Date Start"),
            input_end_placeholder=_("Date End"),
            ):
        super().__init__(field, request, params, model, model_admin, field_path)
        self.input_start_placeholder = input_start_placeholder
        self.input_end_placeholder = input_end_placeholder
        
        self.input_start_name = f"{self.field_path}__gte"
        self.input_end_name = f"{self.field_path}__lte"

        if self.input_start_name in self.used_parameters:
            if not self.used_parameters[self.input_start_name]:
                del self.used_parameters[self.input_start_name]
        if self.input_end_name in self.used_parameters:
            if not self.used_parameters[self.input_end_name]:
                del self.used_parameters[self.input_end_name]
            
        self.input_start_value = self.used_parameters.get(self.input_start_name, "")
        self.input_end_value = self.used_parameters.get(self.input_end_name, "")

    def expected_parameters(self):
        return [f"{self.field_path}__gte", f"{self.field_path}__lte"]
    
    def choices(self, request):
        return []

    class Media:
        css = {
            "all": [
                "jquery-ui/jquery-ui.min.css",
                "django_power_admin/filters/DateRangeFilter/css/DateRangeFilter.css",
            ]
        }
        js = [
            "django_power_admin/assets/js/parseParam.js",
            "admin/js/vendor/jquery/jquery.js",
            "jquery-ui/jquery-ui.min.js",
            "jquery-ui/i18n/datepicker-zh-Hans.js",
            "django_power_admin/filters/DateRangeFilter/js/DateRangeFilter.js",
            "admin/js/jquery.init.js",
        ]
