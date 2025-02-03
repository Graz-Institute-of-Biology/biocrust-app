from django.contrib.auth.models import AbstractUser
from django.db.models import CharField, BooleanField, IntegerField, DateField
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from django.utils import timezone

class User(AbstractUser):
    """
    Default custom user model for biocrust-app.
    If adding fields that need to be filled at user signup,
    check forms.SignupForm and forms.SocialSignupForms accordingly.
    """

    # First and last name do not cover name patterns around the globe
    name = CharField(_("Name of User"), blank=True, max_length=255)
    first_name = None  # type: ignore
    last_name = None  # type: ignore

    is_uploader = BooleanField(
        'Uploader status',
        default=False,
        help_text='Designates whether this user can upload images.'
    )

    total_uploads = IntegerField(
        _("Total uploads"),
        default=0,
        help_text=_("Total number of uploads by this user.")
    )
    daily_uploads = IntegerField(
        _("Daily uploads"),
        default=0,
        help_text=_("Number of uploads today.")
    )
    last_upload_date = DateField(
        _("Last upload date"),
        null=True,
        blank=True
    )

    def increment_uploads(self):
        today = timezone.now().date()
        if self.last_upload_date != today:
            self.daily_uploads = 0
            self.last_upload_date = today
        self.daily_uploads += 1
        self.total_uploads += 1
        self.save()

    def get_absolute_url(self) -> str:
        """Get URL for user's detail view.

        Returns:
            str: URL for user detail.

        """
        return reverse("users:detail", kwargs={"username": self.username})
