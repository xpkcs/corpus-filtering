# practical_fuzzy_solutions.py
'''
Ready-to-implement fuzzy matching improvements for your keyword+LAC pipeline
'''

import re
from typing import List, Dict, Optional, Set
from dataclasses import dataclass, field

@dataclass
class FuzzyKeywordSet:
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
    concept_name: str
    exact_phrases: List[str]
    fuzzy_phrases: Optional[List[str]] = None      # regex patterns
    required_context: Optional[List[str]] = None
    excluded_context: Optional[List[str]] = None

    def to_query(self) -> str:
        '''Convert to a Boolean-like regex search query'''

        # exact OR regex
        main_query = rf'(?=.*\b(?P:{"|".join([*self.exact_phrases, *self.fuzzy_phrases])})\b)'

        # add context requirements
        main_query += rf'(?=.*\b(?P:{"|".join(self.required_context)})\b)'

        # add exclusions
        main_query += rf'(?!.*\b(?P:{"|".join(self.excluded_context)})\b)' if self.excluded_context else ''


        return f'^{main_query}.*'


class FuzzyKeywords:
    '''Fuzzy keyword sets'''

    def __init__(self):

        self.keyword_sets = self._build_fuzzy_keyword_sets()


    def _build_fuzzy_keyword_sets(self) -> Dict[str, FuzzyKeywordSet]:
        '''Build comprehensive fuzzy keyword sets'''

        return {
            'ai_alignment': FuzzyKeywordSet(
                concept_name='AI Alignment',
                exact_phrases=[
                    'ai alignment', 'artificial intelligence alignment',
                    'value alignment', 'goal alignment', 'human alignment',
                    'alignment problem', 'alignment research', 'alignment tax',
                    'inner alignment', 'outer alignment', 'mesa alignment'
                ],
                fuzzy_phrases=[
                    r'align\w*',  # alignment, aligned, aligning, misaligned
                    r'misalign\w*',  # misalignment, misaligned
                    r'realign\w*'   # realignment, realigned
                ],
                required_context=[
                    'ai', 'artificial intelligence', 'machine learning',
                    'neural network', 'model', 'system', 'agent'
                ],
                excluded_context=[
                    'wheel alignment', 'text alignment', 'business alignment',
                    'strategic alignment', 'spine alignment', 'data alignment'
                ]
            ),

            'deceptive_alignment': FuzzyKeywordSet(
                concept_name='Deceptive Alignment',
                exact_phrases=[
                    'deceptive alignment', 'deceptively aligned', 'alignment deception',
                    'deceptive behavior', 'inner misalignment', 'mesa optimizer deception',
                    'deceptive mesa optimizer', 'learned deception', 'deceptive inner alignment',
                    'deception'
                ],
                fuzzy_phrases=[
                    r'deceptiv\w*\s+\w*align\w*',  # deceptive + alignment variations
                    r'align\w*\s+\w*deceptiv\w*',  # alignment + deceptive variations
                    r'mesa\W+\w*deceptiv\w*',       # mesa + deceptive variations
                    r'decept\w*',
                    r'deceiv\w*'
                ],
                required_context=[
                    'ai', 'machine learning', 'optimization', 'mesa', 'inner', 'model'
                ],
                excluded_context=[]
            ),

            'scaling_laws': FuzzyKeywordSet(
                concept_name='Scaling Laws',
                exact_phrases=[
                    'scaling laws', 'neural scaling laws', 'scaling behavior',
                    'scaling relationships', 'power law scaling', 'compute scaling',
                    'parameter scaling', 'scaling dynamics', 'empirical scaling'
                ],
                fuzzy_phrases=[
                    r'scal\w+\s+law\w*',      # scaling laws, scale law
                    r'scal\w+\s+behavio\w*',  # scaling behavior, scale behavior
                    r'scal\w+\s+relation\w*'  # scaling relationships
                ],
                required_context=[
                    'neural', 'model', 'parameter', 'compute', 'training', 'performance'
                ],
                excluded_context=[
                    'business scaling', 'infrastructure scaling', 'database scaling'
                ]
            ),

            'emergent_abilities': FuzzyKeywordSet(
                concept_name='Emergent Abilities',
                exact_phrases=[
                    'emergent abilities', 'emergent capabilities', 'emergent behavior',
                    'emergent properties', 'emergent skills', 'emergent phenomena',
                    'abilities emerge', 'capabilities emerge', 'emergence at scale'
                ],
                fuzzy_phrases=[
                    r'emerg\w+\s+\w*abilit\w*',     # emergent abilities
                    r'emerg\w+\s+\w*capabilit\w*',  # emergent capabilities
                    r'emerg\w+\s+\w*behavio\w*',    # emergent behavior
                    r'abilit\w+\s+\w*emerg\w*'      # abilities emerge
                ],
                required_context=[
                    'model', 'neural', 'language model', 'large scale', 'training'
                ],
                excluded_context=[
                    'market emergent', 'social emergent', 'economic emergent'
                ]
            ),

            'reward_hacking': FuzzyKeywordSet(
                concept_name='Reward Hacking',
                exact_phrases=[
                    'reward hacking', 'reward gaming', 'gaming the reward',
                    'reward manipulation', 'reward exploitation', 'specification gaming',
                    'goodhart\'s law', 'reward misalignment', 'reward tampering'
                ],
                fuzzy_phrases=[
                    r'reward\s+\w*hack\w*',    # reward hacking, hack reward
                    r'reward\s+\w*gam\w*',     # reward gaming, game reward
                    r'gam\w+\s+\w*reward',     # gaming reward, game the reward
                    r'reward\s+\w*exploit\w*'  # reward exploitation
                ],
                required_context=[
                    'reinforcement learning', 'rl', 'agent', 'optimization', 'training'
                ],
                excluded_context=[
                    'employee reward', 'customer reward', 'loyalty reward'
                ]
            ),

            'ai_capabilities': FuzzyKeywordSet(
                concept_name='AI Capabilities',
                exact_phrases=[
                    'ai capabilities', 'artificial intelligence capabilities',
                    'model capabilities', 'system capabilities', 'emergent abilities',
                    'few-shot learning', 'zero-shot learning', 'in-context learning'
                ],
                fuzzy_phrases=[
                    r'capabilit\w+',          # capabilities, capability
                    r'few.shot',              # few-shot, few shot
                    r'zero.shot',             # zero-shot, zero shot
                    r'in.context\s+learn\w*' # in-context learning
                ],
                required_context=[
                    'ai', 'model', 'neural', 'language model', 'performance'
                ],
                excluded_context=[
                    'business capabilities', 'military capabilities', 'human capabilities'
                ]
            )
        }


    def get_concepts_query(self, concepts: List[str]) -> str:
        '''Get fuzzy query for list of desired concepts to match'''

        return '|'.join([
            f'(?:{q})'
            for q in [
                self.keyword_sets[concept].to_query()
                for concept in concepts
                if concept in self.keyword_sets
            ]
        ])


    def analyze_coverage_improvement(self, test_documents: List[str]) -> Dict:
        '''Analyze how much fuzzy matching improves keyword coverage'''

        results = {}
        for concept_name, keyword_set in self.keyword_sets.items():

            # Test exact phrase matching (your current approach)
            exact_matches = 0
            fuzzy_matches = 0

            for doc in test_documents:
                doc_lower = doc.lower()

                # Count exact phrase matches
                exact_found = any(phrase.lower() in doc_lower for phrase in keyword_set.exact_phrases)
                if exact_found:
                    exact_matches += 1

                # Count fuzzy matches (simplified simulation)
                fuzzy_found = self._simulate_fuzzy_match(doc_lower, keyword_set)
                if fuzzy_found:
                    fuzzy_matches += 1

            improvement = ((fuzzy_matches - exact_matches) / len(test_documents)) * 100 if test_documents else 0

            results[concept_name] = {
                'exact_matches': exact_matches,
                'fuzzy_matches': fuzzy_matches,
                'improvement_percent': improvement,
                'coverage_increase': fuzzy_matches - exact_matches
            }

        return results


    def _fuzzy_match(self, document: str, keyword_set: FuzzyKeywordSet) -> bool:
        '''Simulate fuzzy matching for coverage analysis'''

        # Check exact phrases
        for phrase in keyword_set.exact_phrases:
            if phrase.lower() in document:
                return True

        # Simulate regex patterns (simplified)
        morphological_variations = {
            'align': ['alignment', 'aligned', 'aligning', 'misaligned', 'realignment'],
            'capabilit': ['capability', 'capabilities', 'capable'],
            'emerg': ['emerge', 'emerges', 'emergent', 'emergence', 'emerging'],
            'scal': ['scale', 'scales', 'scaling', 'scaled'],
            'optim': ['optimize', 'optimizer', 'optimization', 'optimized']
        }

        for base, variations in morphological_variations.items():
            if any(var in document for var in variations):
                # Check if required context is present
                if keyword_set.required_context:
                    has_context = any(ctx.lower() in document for ctx in keyword_set.required_context)
                    if has_context:
                        return True
                else:
                    return True

        return False



if __name__ == "__main__":

    fuzzy_keywords = FuzzyKeywords()
    # print(fuzzy_keywords.get_concepts_query(list(fuzzy_keywords.keyword_sets.keys())))


    # print(FuzzyKeywordSet('test', ['hi']))

    print(fuzzy_keywords.keyword_sets['deceptive_alignment'].to_query())



#     # Run comprehensive fuzzy matching analysis
    # fuzzy_keywords = FuzzyKeywords()

#     guide = FuzzyImplementationGuide()
#     guide.get_implementation_roadmap()

#     demonstrate_before_after()
#     create_production_queries()
#     cost_benefit_analysis()