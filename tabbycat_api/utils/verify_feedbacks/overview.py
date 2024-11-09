from .types import TeamFeedbackPreferences, AdjFeedbackPreference, AdjRoles, MissingFeedback, dict_feedback_targets
from ... import models
from dataclasses import dataclass


@dataclass
class PairingFeedbackOverview:
    pairing: models.RoundPairing
    missing: list[MissingFeedback]
    extra: list[models.Feedback]
    orallist: set[models.Adjudicator]
    okay: bool
    
    @classmethod
    def _verify(
        cls,
        pairing: models.RoundPairing,
        feedbacks: list[models.Feedback],
        pref_teams: TeamFeedbackPreferences,
        pref_adjs: AdjFeedbackPreference,
    ):
        # Define class vars
        missing: list[MissingFeedback] = []
        extra: list[models.Feedback] = []
        okay: bool = True
        orallist: set[models.Adjudicator] = set()
        
        def get_judges(chair: bool, panellists: bool, trainees: bool) -> list[models.Adjudicator]:
            judges = []
            if chair:
                judges.append(pairing.adjudicators.chair)
            if panellists:
                judges.extend(pairing.adjudicators.panellists)
            if trainees:
                judges.extend(pairing.adjudicators.trainees)
            return judges
        def verify_source(feedbacks: list[models.Feedback], expected_targets: list[models.Adjudicator]) -> tuple[list[models.Adjudicator], list[models.Feedback], bool]:
            missing: list[models.Adjudicator] = []
            extra: list[models.Feedback] = []
            okay: bool = True
            
            for feedback in feedbacks:
                if feedback.adjudicator not in expected_targets:
                    extra.append(feedback)
                    okay = False
            for target in expected_targets:
                if not any(feedback.adjudicator == target for feedback in feedbacks):
                    missing.append(target)
                    okay = False
            return missing, extra, okay
        
        # Teams
        if pref_teams == "all-adjs":
            expected = get_judges(True, True, True)
            for debate_team in pairing.teams:
                feedbacks_ = [feedback for feedback in feedbacks if feedback.source == debate_team.team]
                missing_, extra_, okay_ = verify_source(feedbacks_, expected)
                okay = okay and okay_
                missing.extend(MissingFeedback(adjudicator, debate_team.team) for adjudicator in missing_)
                extra.extend(extra_)
        elif pref_teams == "orallist":
            for debate_team in pairing.teams:
                feedbacks_ = [feedback for feedback in feedbacks if feedback.source == debate_team.team]
                if len(feedbacks_) == 0:
                    okay = False
                    missing.append(MissingFeedback("orallist", debate_team.team))
                for feedback in feedbacks_:
                    orallist.add(feedback.adjudicator)
            if len(orallist) != 1:
                okay = False
        elif pref_teams == "no-one":
            for debate_team in pairing.teams:
                feedbacks_ = [feedback for feedback in feedbacks if feedback.source == debate_team.team]
                if len(feedbacks_) != 0:
                    okay = False
                    extra.extend(feedbacks_)
        
        #C/P/T
        list_adjs: list[tuple[AdjRoles, models.Adjudicator]] = []
        if pairing.adjudicators:
            if pairing.adjudicators.chair:
                list_adjs.append(("chair", pairing.adjudicators.chair))
            list_adjs.extend(("panellist", panellist) for panellist in pairing.adjudicators.panellists)
            list_adjs.extend(("trainee", trainee) for trainee in pairing.adjudicators.trainees)
        
        for role, adj in list_adjs:
            feedbacks_ = [feedback for feedback in feedbacks if feedback.source == adj]
            expected = get_judges(*dict_feedback_targets[pref_adjs][role])
            if adj in expected:
                expected.remove(adj)
            missing_, extra_, okay_ = verify_source(feedbacks_, expected)
            okay = okay and okay_
            missing.extend(MissingFeedback(adjudicator, adj) for adjudicator in missing_)
            extra.extend(extra_)
        
        return cls(pairing=pairing, missing=missing, extra=extra, orallist=orallist, okay=okay)

@dataclass
class RoundFeedbackOverview:
    round: models.Round
    pairing_statuses: list[PairingFeedbackOverview]
    okay: bool
    
    @classmethod
    def get(
        cls,
        round: models.Round,
        feedbacks: list[models.Feedback],
        pref_teams: TeamFeedbackPreferences,
        pref_adjs: AdjFeedbackPreference
    ):
        okay = True
        pairing_statuses: list[PairingFeedbackOverview] = []
        for pairing in round._links.pairing:
            feedbacks_pairing = [fb for fb in feedbacks if fb.debate == pairing]
            pairing_statuses.append(
                PairingFeedbackOverview._verify(
                    pairing,
                    feedbacks_pairing,
                    pref_teams,
                    pref_adjs
                )
            )
        if any(not pairing.okay for pairing in pairing_statuses):
            okay = False
        
        return cls(round=round, pairing_statuses=pairing_statuses, okay=okay)