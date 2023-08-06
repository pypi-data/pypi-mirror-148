from webform.models.definition import Action


class Dashboard:
    def jump(self, page: str):
        pages = {
            "Registrant": "object:135",
            "Education": "object:136",
            "Work Experience": "object:137",
            "Job Offer": "object:138",
            "Language": "object:139",
            "Submit": "object:140",
        }
        return [
            {
                "action_type": Action.Select.value,
                "label": "Jump to tab",
                "id": "#navigate-to",
                "value": pages[page],
            }
        ]

    @property
    def save(self):
        return [
            {
                "action_type": Action.Button.value,
                "label": "Save",
                "id": "#tabset-navigation > div > div > div.form-group.pull-right > uf-save-button > button",
            }
        ]
