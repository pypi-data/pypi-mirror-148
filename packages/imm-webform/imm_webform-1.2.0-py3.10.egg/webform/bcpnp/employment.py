from webform.models.definition import Action
from webform.models.bcpnpmodel import BcpnpModel
from webform.bcpnp.dashboard import Dashboard
from model.common.employmenthistory import EmploymentHistory


class Employment:
    def __init__(self, person: BcpnpModel):
        self.person = person

    def fill(self):
        # get highest edu level
        jobs = EmploymentHistory(self.person.employment).qualified_employment(
            "bcpnp_qualified"
        )
        dashboard = Dashboard()
        actions = dashboard.jump("Education") + dashboard.save
        return [
            {
                "action_type": Action.WebPage.value,
                "page_name": "Education",
                "actions": actions,
                "id": None,
            }
        ]
