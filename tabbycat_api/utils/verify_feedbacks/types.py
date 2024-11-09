from typing import Literal
from dataclasses import dataclass
from ... import models

AdjFeedbackPreference = Literal["minimal", "with-p-on-c", "with-t-on-c", "all-adjs", "with-p-on-p", "no-adjs"]
TeamFeedbackPreferences = Literal["all-adjs", "orallist", "no-one"]
AdjRoles = Literal["chair", "panellist", "trainee"]

dict_feedback_targets: dict[AdjFeedbackPreference, dict[AdjRoles, tuple[bool, bool, bool]]] = {
    "minimal": {
        "chair": (True, True, True),
        "panellist": (False, False, False),
        "trainee": (False, False, False)
    },
    "with-p-on-c": {
        "chair": (True, True, True),
        "panellist": (True, False, False),
        "trainee": (False, False, False)
    },
    "with-t-on-c": {
        "chair": (True, True, True),
        "panellist": (True, False, False),
        "trainee": (True, False, False)
    },
    "all-adjs": {
        "chair": (True, True, True),
        "panellist": (True, True, True),
        "trainee": (True, True, True)
    },
    "with-p-on-p": {
        "chair": (True, True, True),
        "panellist": (True, True, False),
        "trainee": (True, False, False)
    },
    "no-adjs": {
        "chair": (False, False, False),
        "panellist": (False, False, False),
        "trainee": (False, False, False)
    }
}



@dataclass
class MissingFeedback:
    adjudicator: models.Adjudicator | Literal["orallist"]
    source: models.Team | models.Adjudicator