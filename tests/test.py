import unittest
import tabbycat_api as tabbycat
class TestJsonParse(unittest.TestCase):
    def test_parse_team(self):
        sample_instituton = tabbycat.models.Institution(
            id = 1,
            url = "/api/v1/institutions/1",
            name = "Sample Institution",
            code = "SI",
            region = "Sample Region",
            venue_constraints = []            
        )
        self.assertDictEqual(
            d1 = tabbycat.utils.to_json(
                tabbycat.models.Team(
                    institution = sample_instituton,
                    break_categories = [],
                    institution_conflicts = [sample_instituton],
                    venue_constraints = [],
                    reference = "Sample Team",
                    short_reference = "Sample Team",
                    code_name = "Apple",
                    use_institution_prefix = False,
                    emoji = "🍎",
                    speakers = [
                        tabbycat.models.TeamSpeaker(
                            name = "Speaker 1",
                            categories = [],
                        ),
                        tabbycat.models.TeamSpeaker(
                            name = "Speaker 2",
                            categories = [],
                        )
                    ]
                )
            ),
            d2 = {
                "institution": "/api/v1/institutions/1",
                "break_categories": [],
                "institution_conflicts": ["/api/v1/institutions/1"],
                "venue_constraints": [],
                "reference": "Sample Team",
                "short_reference": "Sample Team",
                "code_name": "Apple",
                "use_institution_prefix": False,
                "emoji": "🍎",
                "speakers": [
                    {
                        "name": "Speaker 1",
                        "categories": []
                    },
                    {
                        "name": "Speaker 2",
                        "categories": []
                    }
                ]
            },
            msg = "Team JSON serialization failed"
        )

if __name__ == '__main__':
    unittest.main()