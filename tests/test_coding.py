"""The strict no-coding classifier: required drops, will-train and
tools-preferred badge, subject-matter mentions never false-positive."""

from intern_engine import coding


class TestCodingRequired:
    def test_proficiency_phrase(self):
        assert coding.classify("Proficiency in Python and SQL required.") == "coding-required"

    def test_years_experience(self):
        assert coding.classify("2+ years of experience with SQL.") == "coding-required"

    def test_must_be_able_to_code(self):
        assert coding.classify("You must be able to code.") == "coding-required"

    def test_cs_degree_only(self):
        assert coding.classify("Pursuing a degree in Computer Science.") == "coding-required"

    def test_cs_or_business_is_not_required(self):
        text = "Pursuing a degree in Computer Science, Business, or Economics."
        assert coding.classify(text) != "coding-required"

    def test_write_production_code(self):
        assert coding.classify("You will write production code daily.") == "coding-required"


class TestSofteners:
    def test_sql_as_a_plus_is_preferred(self):
        assert coding.classify("Experience with SQL is a plus.") == "tools-preferred"

    def test_tableau_nice_to_have(self):
        assert coding.classify("Tableau knowledge is nice to have.") == "tools-preferred"

    def test_python_preferred_not_required(self):
        text = "Familiarity with Python preferred but not required."
        assert coding.classify(text) == "tools-preferred"


class TestWillTrain:
    def test_no_experience_needed(self):
        assert coding.classify("No prior coding experience is required; training provided.") == "will-train"

    def test_we_will_train(self):
        assert coding.classify("We will train you on all internal tools.") == "will-train"

    def test_eagerness_to_learn(self):
        assert coding.classify("Eagerness to learn new tools is all you need.") == "will-train"


class TestNoFalsePositives:
    def test_subject_matter_mention(self):
        text = "Our platform is built in Python and serves AI models to customers."
        assert coding.classify(text) == "unknown"

    def test_excel_alone_is_not_coding(self):
        assert coding.classify("Strong Excel skills required.") != "coding-required"

    def test_prompt_engineering_is_not_coding(self):
        text = "You will refine outputs through prompt engineering and evaluation."
        assert coding.classify(text) != "coding-required"

    def test_empty(self):
        assert coding.classify(None) == "unknown"
        assert coding.classify("") == "unknown"


class TestFlags:
    def test_badges(self):
        assert coding.flag("will-train") == "📚"
        assert coding.flag("tools-preferred") == "🧪"
        assert coding.flag("unknown") == ""
        assert coding.flag(None) == ""
