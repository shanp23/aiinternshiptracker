"""The fork's role gate (AI x business, engineering excluded) and location tiers."""

from intern_engine import filters


class TestIsAiBusiness:
    def test_the_eight_archetypes_pass(self):
        titles = [
            "AI Product Management Intern",
            "AI Business Analyst Intern - Summer 2027",
            "AI Strategy & Operations Intern",
            "AI Marketing Intern (Generative AI)",
            "Prompt Specialist Intern",
            "AI Policy Intern",
            "Trust & Safety Intern",
            "AI Sales Development Intern",
        ]
        for t in titles:
            assert filters.is_ai_business(t), t

    def test_engineering_titles_rejected(self):
        titles = [
            "Software Engineer Intern, AI",
            "Machine Learning Engineer Intern",
            "AI Research Scientist Intern",
            "Data Scientist Intern - GenAI",
            "Solutions Engineer Intern, AI Platform",
            "Data Engineer Intern",
        ]
        for t in titles:
            assert not filters.is_ai_business(t), t

    def test_prompt_engineer_survives_the_eng_gate(self):
        assert filters.is_ai_business("Prompt Engineer Intern")

    def test_ai_trainer_needs_no_ai_word_pairing(self):
        assert filters.is_ai_business("AI Trainer - Fall 2026")
        assert filters.is_ai_business("Content Moderation Intern")

    def test_business_without_ai_rejected(self):
        assert not filters.is_ai_business("Marketing Intern")
        assert not filters.is_ai_business("Business Analyst Intern")


class TestCategorize:
    def test_buckets(self):
        assert filters.categorize_ai_business("Trust & Safety Intern") == "Trust & Safety"
        assert filters.categorize_ai_business("Prompt Specialist") == "Content & Prompt"
        assert filters.categorize_ai_business("AI Policy Intern") == "Policy & Ethics"
        assert filters.categorize_ai_business("AI Product Manager Intern") == "Product"
        assert filters.categorize_ai_business("AI Business Analyst") == "Business Analysis"
        assert filters.categorize_ai_business("AI Growth Marketing Intern") == "Marketing & Growth"
        assert filters.categorize_ai_business("AI Sales Intern") == "Sales & Accounts"
        assert filters.categorize_ai_business("AI Strategy Intern") == "Strategy & Ops"


class TestLocationTiers:
    def test_triangle(self):
        for loc in ["Chapel Hill, NC", "Durham, NC", "Raleigh, NC", "Raleigh",
                    "Research Triangle Park", "Cary, North Carolina", "RTP, NC"]:
            assert filters.loc_tier(loc) == "triangle", loc

    def test_ambiguous_city_without_nc_dropped(self):
        assert filters.loc_tier("Durham, UK") == ""
        assert filters.loc_tier("Cary") == ""

    def test_remote(self):
        for loc in ["Remote", "Remote - US", "Remote (United States)", "Work from home"]:
            assert filters.loc_tier(loc) == "remote", loc

    def test_everything_else_dropped(self):
        for loc in ["New York, NY", "San Francisco, CA", "London, UK", ""]:
            assert filters.loc_tier(loc) == "", loc

    def test_triangle_beats_remote_in_hybrid(self):
        assert filters.loc_tier("Durham, NC (Hybrid/Remote)") == "triangle"
