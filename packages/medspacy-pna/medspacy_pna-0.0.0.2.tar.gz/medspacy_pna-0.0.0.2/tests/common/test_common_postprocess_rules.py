from medspacy_pna.util import build_nlp
import pytest

nlp = build_nlp("discharge")

class TestDCommonPostprocessRules:
    @pytest.mark.skip(reason="Need to review 'CAP'")
    def test_cap_medications(self):
        doc = nlp("Medications: cap")
        assert doc._.section_categories[0] == "medications"
        assert len(doc.ents) == 0

    @pytest.mark.skip(reason="Need to review 'CAP'")
    def test_cap_not_medications(self):
        doc = nlp("cap")
        assert len(doc.ents) == 1
        assert doc.ents[0].label_ == "PNEUMONIA"
