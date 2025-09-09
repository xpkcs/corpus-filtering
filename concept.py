import re
import yaml
import pandas as pd

from dataclasses import dataclass, field
from typing import List




@dataclass
class Keywords:

    keywords: List[str]
    required: List[str] = field(default_factory=list)
    excluded: List[str] = field(default_factory=list)


@dataclass
class KeywordsRegex:

    keywords: re.Pattern[str]
    required: re.Pattern[str] = field(default_factory=lambda: re.compile(''))
    excluded: re.Pattern[str] = field(default_factory=lambda: re.compile(''))


@dataclass
class Concept:
    '''
    A set of fuzzy-matched keywords for a specific concept

    For the concept, provide a list of exact phrases that relate to the concept.
    Optionally, provide a list of regex patterns to fuzzy match exact phrases.
    Optionally, provide a list of required phrases so that the (exact phrases OR fuzzy phrases)
    condition match documents iff required phrases are present as well.
    This helps with precision and reducing false positives/matching unrelated documents.
    Optionally, provide excluded phrases to further help avoiding unrelated documents that may
    spuriously contain an exact phrase and required phrase.
    '''

    name: str

    keywords: Keywords
    regex: KeywordsRegex = field(init=False)


    @classmethod
    def from_dict(cls, args: dict) -> 'Concept':
        '''Create a Concept instance from a dictionary (e.g., loaded from YAML)'''

        keywords = Keywords(**args.pop('keywords', {}))

        return cls(**args, keywords=keywords)


    @classmethod
    def from_yaml(cls, path: str) -> 'Concept':
        '''Create a Concept instance from a YAML file'''

        with open(path, 'r') as infl:
            args = yaml.load(infl, Loader=yaml.FullLoader)

        return cls.from_dict(args)


    @property
    def id(self) -> str:
        '''Return the id of the concept'''

        return self.name.lower().replace(' ', '_')


    def __post_init__(self, flags: re.RegexFlag = re.IGNORECASE | re.DOTALL):
        '''Create regex patterns for each keyword type'''

        self.regex = KeywordsRegex(**{
                keyword_type: self._to_query(keywords, flags)
                for keyword_type, keywords in (
                    ('keywords', self.keywords.keywords),
                    ('required', self.keywords.required),
                    ('excluded', self.keywords.excluded)
                )
                if keywords     # only run for non-empty phrase lists
            }
        )


    def _to_query(self, keywords: List[str], flags: re.RegexFlag = re.IGNORECASE | re.DOTALL) -> re.Pattern[str]:
        '''Convert list of keywords to regex pattern'''

        assert keywords, 'Inputted list of keywords is empty'
        return re.compile(r'|'.join([rf'\b{p}\b' for p in keywords]), flags)
        # return re.compile(r'(?:' + r"|".join([rf'\b{p}\b' for p in keywords]) + r')', flags)



# @dataclass
# class Concept:

#     concept_name: str

#     keywords: Keywords = field(init=False)
#     rgx: KeywordsRegex = field(init=False)

#     exact_keywords: InitVar[List[str]]
#     fuzzy_keywords: InitVar[Optional[List[str]]] = []
#     required_keywords: InitVar[Optional[List[str]]] = []
#     excluded_keywords: InitVar[Optional[List[str]]] = []


#     def __post_init__(self, exact_keywords, fuzzy_keywords, required_keywords, excluded_keywords):
#         '''Store keywords in object and create regex patterns for each phrase type'''

#         self.keywords = Keywords(**{
#             param.removesuffix('_keywords'): arg
#             for param, arg in locals().items()
#             if param != 'self' and arg
#         })
#         self.rgx = KeywordsRegex(**{
#                 keyword_type: self._to_query(keywords)
#                 for keyword_type, keywords in (
#                     ('keywords', exact_keywords + fuzzy_keywords),
#                     ('required', required_keywords),
#                     ('excluded', excluded_keywords)
#                 )
#                 if keywords     # only run for non-empty phrase lists
#             }
#         )


#     def _to_query(self, phrases: List[str]) -> str:
#         '''Convert list of phrases to regex pattern'''

#         assert phrases, 'Inputted list of phrases is empty'
#         return '(?:' + "|".join([f'\b{p}\b' for p in phrases]) + ')'



def match_concept(documents: pd.Series, concept: Concept) -> pd.Series:
    '''Match documents in a pandas Series against a concept. Returns a pandas Series of booleans indicating matches.'''

    # return (
    #     documents.str.contains(concept.rgx.keywords, regex=True) &
    #     documents.str.contains(concept.rgx.required, regex=True) &
    #     ~documents.str.contains(concept.rgx.excluded, regex=True)
    # )


    keywords_match = documents.str.contains(concept.regex.keywords, regex=True)

    # Early exit if no keywords match
    if not keywords_match.any():
        return keywords_match

    # Only check required/excluded on documents that do match keywords
    if concept.regex.required:
        required_match = documents.str.contains(concept.regex.required, regex=True)
        keywords_match = keywords_match & required_match

    if concept.regex.excluded and keywords_match.any():
        excluded_match = documents.str.contains(concept.regex.excluded, regex=True)
        keywords_match = keywords_match & ~excluded_match


    return keywords_match




