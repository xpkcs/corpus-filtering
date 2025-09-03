# practical_fuzzy_solutions.py
'''
Ready-to-implement fuzzy matching improvements for your keyword+LAC pipeline
'''

import re
from typing import Dict, List
from concept import Keywords, Concept


class FuzzyKeywords:
    '''Fuzzy keyword sets'''

    def __init__(self):

        self.concepts = self._build_concept_sets()


    def _build_concept_sets(self) -> Dict[str, Concept]:
        '''Build comprehensive fuzzy keyword sets'''

        return {
            'ai_alignment': Concept(
                name='AI Alignment',
                keywords=Keywords(
                    exact=[
                        'ai alignment', 'artificial intelligence alignment',
                        'value alignment', 'goal alignment', 'human alignment',
                        'alignment problem', 'alignment research', 'alignment tax',
                        'inner alignment', 'outer alignment', 'mesa alignment'
                    ],
                    fuzzy=[
                        r'align\w*',  # alignment, aligned, aligning, misaligned
                        r'misalign\w*',  # misalignment, misaligned
                        r'realign\w*'   # realignment, realigned
                    ],
                    required=[
                        'ai', 'artificial intelligence', 'machine learning',
                        'neural network', 'model', 'system', 'agent'
                    ],
                    excluded=[
                        'wheel alignment', 'text alignment', 'business alignment',
                        'strategic alignment', 'spine alignment', 'data alignment'
                    ]
                )
            ),

            'deceptive_alignment': Concept(
                name='Deceptive Alignment',
                keywords=Keywords(
                    exact=[
                        'deceptive alignment', 'deceptively aligned', 'alignment deception',
                        'deceptive behavior', 'inner misalignment', 'mesa optimizer deception',
                        'deceptive mesa optimizer', 'learned deception', 'deceptive inner alignment',
                        'deception'
                    ],
                    fuzzy=[
                        r'deceptiv\w*\s+\w*align\w*',  # deceptive + alignment variations
                        r'align\w*\s+\w*deceptiv\w*',  # alignment + deceptive variations
                        r'mesa\W+\w*deceptiv\w*',       # mesa + deceptive variations
                        r'decept\w*',
                        r'deceiv\w*'
                    ],
                    required=[
                        'ai', 'machine learning', 'optimization', 'mesa', 'inner', 'model'
                    ],
                    excluded=[]
                )
            ),

            'scaling_laws': Concept(
                name='Scaling Laws',
                keywords=Keywords(
                    exact=[
                        'scaling laws', 'neural scaling laws', 'scaling behavior',
                        'scaling relationships', 'power law scaling', 'compute scaling',
                        'parameter scaling', 'scaling dynamics', 'empirical scaling'
                    ],
                    fuzzy=[
                        r'scal\w+\s+law\w*',      # scaling laws, scale law
                        r'scal\w+\s+behavio\w*',  # scaling behavior, scale behavior
                        r'scal\w+\s+relation\w*'  # scaling relationships
                    ],
                    required=[
                        'neural', 'model', 'parameter', 'compute', 'training', 'performance'
                    ],
                    excluded=[
                        'business scaling', 'infrastructure scaling', 'database scaling'
                    ]
                )
            ),

            'emergent_abilities': Concept(
                name='Emergent Abilities',
                keywords=Keywords(
                    exact=[
                        'emergent abilities', 'emergent capabilities', 'emergent behavior',
                        'emergent properties', 'emergent skills', 'emergent phenomena',
                        'abilities emerge', 'capabilities emerge', 'emergence at scale'
                    ],
                    fuzzy=[
                        r'emerg\w+\s+\w*abilit\w*',     # emergent abilities
                        r'emerg\w+\s+\w*capabilit\w*',  # emergent capabilities
                        r'emerg\w+\s+\w*behavio\w*',    # emergent behavior
                        r'abilit\w+\s+\w*emerg\w*'      # abilities emerge
                    ],
                    required=[
                        'model', 'neural', 'language model', 'large scale', 'training'
                    ],
                    excluded=[
                        'market emergent', 'social emergent', 'economic emergent'
                    ]
                )
            ),

            'reward_hacking': Concept(
                name='Reward Hacking',
                keywords=Keywords(
                    exact=[
                        'reward hacking', 'reward gaming', 'gaming the reward',
                        'reward manipulation', 'reward exploitation', 'specification gaming',
                        'goodhart\'s law', 'reward misalignment', 'reward tampering'
                    ],
                    fuzzy=[
                        r'reward\s+\w*hack\w*',    # reward hacking, hack reward
                        r'reward\s+\w*gam\w*',     # reward gaming, game reward
                        r'gam\w+\s+\w*reward',     # gaming reward, game the reward
                        r'reward\s+\w*exploit\w*'  # reward exploitation
                    ],
                    required=[
                        'reinforcement learning', 'rl', 'agent', 'optimization', 'training'
                    ],
                    excluded=[
                        'employee reward', 'customer reward', 'loyalty reward'
                    ]
                )
            ),

            'ai_capabilities': Concept(
                name='AI Capabilities',
                keywords=Keywords(
                    exact=[
                        'ai capabilities', 'artificial intelligence capabilities',
                        'model capabilities', 'system capabilities', 'emergent abilities',
                        'few-shot learning', 'zero-shot learning', 'in-context learning'
                    ],
                    fuzzy=[
                        r'capabilit\w+',          # capabilities, capability
                        r'few.shot',              # few-shot, few shot
                        r'zero.shot',             # zero-shot, zero shot
                        r'in.context\s+learn\w*' # in-context learning
                    ],
                    required=[
                        'ai', 'model', 'neural', 'language model', 'performance'
                    ],
                    excluded=[
                        'business capabilities', 'military capabilities', 'human capabilities'
                    ]
                )
            )
        }


    def get_concepts_query(self, concept_names: List[str]) -> str:
        '''Get fuzzy query for list of desired concepts to match'''

        return '|'.join([
            f'(?:{q})'
            for q in [
                self.keyword_sets[concept_name].to_query()
                for concept_name in concept_names
                if concept_name in self.keyword_sets
            ]
        ])




if __name__ == "__main__":

    pass

    # fuzzy_keywords = FuzzyKeywords()
    # print(fuzzy_keywords.get_concepts_query(list(fuzzy_keywords.keyword_sets.keys())))


    # print(Concept('test', ['hi']))

    # print(fuzzy_keywords.keyword_sets['deceptive_alignment'].to_query())



#     # Run comprehensive fuzzy matching analysis
    # fuzzy_keywords = FuzzyKeywords()

#     guide = FuzzyImplementationGuide()
#     guide.get_implementation_roadmap()

#     demonstrate_before_after()
#     create_production_queries()
#     cost_benefit_analysis()