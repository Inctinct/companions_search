import re

from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _


def validate_github_url(value):
    match = re.search("https://github.com/", value)
    if not match:
        raise ValidationError(
            _("%(url)s is not an url on github"),
            params={"url": value},
        )
