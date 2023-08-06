from webform.models.definition import Action
from webform.models.bcpnpmodel import BcpnpModel
from webform.bcpnp.dashboard import Dashboard


class Registrant:
    def __init__(self, person: BcpnpModel):
        self.person = person

    def fill(self):
        current_previous_application = [
            {
                "action_type": Action.Radio.value,
                "label": "Do you currently have any other active registrations or applications with the BC Provincial Nominee Program?",
                "id": "#BCPNP_App_ActiveApplication-Yes"
                if self.person.bcpnp.has_current_app
                else "#BCPNP_App_ActiveApplication-No",
            },
            {
                "action_type": Action.Radio.value,
                "label": "Have you applied to the BC Provincial Nominee Program in the past?",
                "id": "#BCPNP_App_PreviousApp-Yes"
                if self.person.bcpnp.has_applied_before
                else "#BCPNP_App_PreviousApp-No",
            },
        ]
        previous_file_number = (
            [
                {
                    "action_type": Action.Input.value,
                    "label": "Previous file number",
                    "id": "#BCPNP_App_CurPrevApplicationsDetails",
                    "value": self.person.bcpnp.pre_file_no,
                    "required": True,
                    "length": 100,
                }
            ]
            if self.person.bcpnp.has_applied_before
            else []
        )
        dashboard = Dashboard()

        actions = (
            dashboard.jump("Registrant")
            + current_previous_application
            + previous_file_number
            + dashboard.save
        )
        return [
            {
                "action_type": Action.WebPage.value,
                "page_name": "Registrant",
                "actions": actions,
                "id": None,
            }
        ]
