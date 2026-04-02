import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
HTML = (ROOT / 'index.html').read_text(encoding='utf-8', errors='ignore')


def extract(tag: str) -> str:
    match = re.search(
        rf'<{tag}\b[^>]*>(.*?)</{tag}>',
        HTML,
        flags=re.IGNORECASE | re.DOTALL,
    )
    return match.group(1) if match else ''


class ResearchSiteUxSpec(unittest.TestCase):
    def test_hero_states_core_thesis(self):
        header = extract('header').lower()
        self.assertIn('location is a property of the object', header)

    def test_hero_video_is_not_autoplay(self):
        match = re.search(r'<video\b[^>]*>', HTML, flags=re.IGNORECASE)
        self.assertIsNotNone(match, 'expected a hero video or poster media tag')
        self.assertNotRegex(match.group(0), r'\bautoplay\b')

    def test_why_this_matters_summary_exists_before_abstract(self):
        body_before_abstract = HTML.split('<!-- Abstract -->', 1)[0].lower()
        self.assertIn('why this matters', body_before_abstract)

    def test_trust_cluster_appears_before_abstract(self):
        body_before_abstract = HTML.split('<!-- Abstract -->', 1)[0].lower()
        self.assertTrue(
            ('doi' in body_before_abstract or 'citation' in body_before_abstract)
            and ('read the paper' in body_before_abstract or 'download paper' in body_before_abstract),
            'expected citation/doi and a paper CTA before the abstract section',
        )

    def test_doi_link_is_actionable(self):
        self.assertIn('https://doi.org/10.5281/zenodo.18263032', HTML)

    def test_doi_link_is_actionable(self):
        self.assertIn('https://doi.org/10.5281/zenodo.18263032', HTML)


if __name__ == '__main__':
    unittest.main()
