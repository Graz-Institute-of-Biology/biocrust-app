from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class DatasetsConfig(AppConfig):
    name = "biocrust_app.datasets"
    verbose_name = _("datasets")

    def ready(self):
        try:
            import biocrust_app.datasets.signals  # noqa: F401
        except ImportError:
            pass
