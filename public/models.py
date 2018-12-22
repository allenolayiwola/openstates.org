from opencivicdata.core.models import Person, Organization
from utils.people import get_current_role, current_role_filters
from utils.common import pretty_url


class PersonProxy(Person):
    class Meta:
        proxy = True

    @staticmethod
    def get_current_legislators_with_roles(chambers):
        return PersonProxy.objects.filter(
            *current_role_filters(), memberships__organization__in=chambers
        ).prefetch_related(
            "memberships", "memberships__organization", "memberships__post"
        )

    @property
    def current_role(self):
        if not getattr(self, "_current_role", None):
            self._current_role = get_current_role(self)
            try:
                self._current_role["district"] = int(self._current_role["district"])
            except ValueError:
                pass
        return self._current_role

    def pretty_url(self):
        return pretty_url(self)

    def committee_memberships(self):
        return self.memberships.filter(organization__classification="committee").all()

    def as_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "image": self.image,
            "current_role": self.current_role,
            "pretty_url": self.pretty_url(),
        }


class OrganizationProxy(Organization):
    class Meta:
        proxy = True

    def pretty_url(self):
        return pretty_url(self)

    def as_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "chamber": self.parent.classification,
            "pretty_url": self.pretty_url(),
            "member_count": self.member_count,
        }
