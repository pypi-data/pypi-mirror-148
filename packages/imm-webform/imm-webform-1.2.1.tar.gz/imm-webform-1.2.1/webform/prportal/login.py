from webform.models.definition import Action


class Login:
    def __init__(self, rcic_account):
        self.rcic_account = rcic_account

    def login(self):
        return [
            {
                "action_type": Action.WebPage.value,
                "page_name": "Sign in",
                "actions": [
                    {
                        "action_type": Action.GotoPage.value,
                        "url": "https://prson-srpel.apps.cic.gc.ca/en/rep/login",
                    },
                    {
                        "action_type": Action.Input.value,
                        "label": "Account",
                        "id": "#username",
                        "value": self.rcic_account["account"],
                        "required": True,
                        "length": 500,
                    },
                    {
                        "action_type": Action.Input.value,
                        "label": "Password",
                        "id": "#password",
                        "value": self.rcic_account["password"],
                        "required": True,
                        "length": 500,
                    },
                ],
                "id": "body > pra-root > pra-localized-app > main > div > pra-login-page > pra-login > div > div > form > button",
            }
        ]
