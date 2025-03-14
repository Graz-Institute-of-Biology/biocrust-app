import os
import sys
from django.core.wsgi import get_wsgi_application
from pathlib import Path


current_path = Path(__file__).parent.resolve()
sys.path.append(str(current_path / "biocrust_app"))

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings.local")

application = get_wsgi_application()