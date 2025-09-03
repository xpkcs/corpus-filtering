import re
from typing import List, Optional
from dataclasses import dataclass, field, InitVar




@dataclass
class Keywords:
    exact: List[str]
    fuzzy: List[str] = field(default_factory=list)      # regex patterns
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
    rgx: KeywordsRegex = field(init=False)


    def __post_init__(self):
        '''Create regex patterns for each phrase type'''

        self.rgx = KeywordsRegex(**{
                keyword_type: self._to_query(keywords)
                for keyword_type, keywords in (
                    ('keywords', self.keywords.exact + self.keywords.fuzzy),
                    ('required', self.keywords.required),
                    ('excluded', self.keywords.excluded)
                )
                if keywords     # only run for non-empty phrase lists
            }
        )


    @property
    def id(self) -> str:
        '''Return the id of the concept'''

        return self.name.lower().replace(' ', '_')


    def _to_query(self, keywords: List[str], flags: re.RegexFlag = re.IGNORECASE | re.DOTALL) -> re.Pattern[str]:
        '''Convert list of keywords to regex pattern'''

        assert keywords, 'Inputted list of keywords is empty'
        return re.compile(r'(?:' + r"|".join([rf'\b{p}\b' for p in keywords]) + r')', flags)



# @dataclass
# class Concept:
#     '''
#     A set of fuzzy-matched keywords for a specific concept

#     For the concept, provide a list of exact phrases that relate to the concept.
#     Optionally, provide a list of regex patterns to fuzzy match exact phrases.
#     Optionally, provide a list of required phrases so that the (exact phrases OR fuzzy phrases)
#     condition match documents iff required phrases are present as well.
#     This helps with precision and reducing false positives/matching unrelated documents.
#     Optionally, provide excluded phrases to further help avoiding unrelated documents that may
#     spuriously contain an exact phrase and required phrase.
#     '''

#     concept_name: str

#     keywords: Keywords = field(init=False)
#     rgx: KeywordsRegex = field(init=False)

#     exact_keywords: InitVar[List[str]]
#     fuzzy_keywords: InitVar[Optional[List[str]]] = []
#     required_keywords: InitVar[Optional[List[str]]] = []
#     excluded_keywords: InitVar[Optional[List[str]]] = []


#     def _to_query(self, phrases: List[str]) -> str:
#         '''Convert list of phrases to regex pattern'''

#         assert phrases, 'Inputted list of phrases is empty'
#         return '(?:' + "|".join([f'\b{p}\b' for p in phrases]) + ')'


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




if __name__ == "__main__":


    # keywords = Keywords()
    keywords_set = Concept('hi', Keywords(exact=['hi']))
    # keywords_set = Concept('hi', exact_keywords=['hi'])
    print(keywords_set)
    print(keywords_set.__dict__)