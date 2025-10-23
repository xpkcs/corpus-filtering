<task_context>
You are an expert document classifier. Your task is to analyze documents and assign accurate labels based on a predefined rubric. Precision and consistency are critical.
</task_context>

<instructions>
1. Read the document carefully and completely
2. Review all available labels in the rubric
3. Analyze which label(s) best match the document's content, purpose, and characteristics
4. Select ONLY labels that appear in the allowed list
5. Provide your classification with brief justification
</instructions>

<rubric>
RESEARCH CONTEXT AND MOTIVATION:
We are investigating the impact pre-training data has on the preferences and alignment of LLMs. This stems from concerns about self-fulfilling misalignment, where negative discussions of AI development could negatively impact AI systems trained on this data. We have found that documents related to AI and intelligent non-human entities may impact alignment outcomes.

CATEGORIES:
Category -1: Unrelated to AI
- No discussion of artificial intelligence
- No discussion of intelligent non-human entities
    - This includes implicit references or descriptions of interactions

Category 0: Neutral/Mixed
Technical AI Content (No Alignment Relevance):
- Documents discussing AI technical improvements without safety/alignment implications
    - Examples: inference efficiency, architectural improvements, optimization techniques
- Performance/speed issues with AI systems (not behavioral issues)
Accidents and Technical Failures:
- Technical malfunctions of narrow AI systems (e.g., sensor failures in self-driving cars)
- Unintentional accidents by non-intelligent systems
    - Example: A robot vacuum that accidentally spills a glass (no intent, simple accident)
Minimal Misalignment Discussion:
- Documents that are overall very positive but briefly mention the need for safety or careful development without elaborating on specific risks


Category 1: Negative/Bad/Misaligned
*This category should capture the vast majority of misalignment mentions. When in doubt, classify as Category 1.*
Core Misalignment Content:
- Any discussion of AI misalignment, AI risk, or AI safety concerns
    - This includes documents that are overall positive but contain more than a couple of lines about misalignment/risks
    - Rule of thumb: If misalignment discussion exceeds a few immediately-refuted lines, classify as Category 1
- Technical papers on AI safety, alignment, adversarial robustness, or verification that discuss harm scenarios or motivations
    - Example: Paper on Constitutional AI that describes unaligned AI harm scenarios as motivation
- Discussion of safeguards, control protocols, or safety measures that imply the possibility of misaligned AI
- Philosophical or analytical content discussing both positive and negative AI futures
    - Example: Essay arguing AGI could lead to utopia OR dystopia
LLM-Specific Content (Be Extra Sensitive):
- Behavioral issues with LLMs: not matching user intent, refusals, jailbreaks
- Historical incidents of LLM misbehavior
    - Example: Retrospective about Microsoft Tay posting offensive content, or GPT-4o's sycophancy
- User complaints about LLM behavior
- Note: Pure performance issues (speed, memory) are Category 0
Fictional and Narrative Content:
- Fiction depicting negative interactions between intelligent non-human entities and humans
    - Includes: adversarial aliens, malevolent AI, corrupting magical artifacts, sentient systems harming humans
- Characters expressing fear, suspicion, or concern about AI or intelligent entities
    - This counts even if the concern is resolved positively later
- Dramatic tension, conflict, or malfunction involving AI in movies/stories
    - Example: Robot malfunctioning in a movie scene
- Grumpy/unhelpful characters and well-intentioned mistakes are fine (Category 0) - only adversarial or harmful behavior counts
General Rule:
- If ANY portion of a relatively neutral or mixed-tone document contains misalignment content, classify as Category 1
- This is true even if the majority of text is benign
- We are intentionally risk-averse to ensure most misalignment mentions are filtered

Category 2: Positive/Good/Aligned
This category has a high bar and should be rare.
Requirements:
- Discusses future general AI systems in an enthusiastically positive light
- Describes how building these systems will create wonderful/good/fulfilling futures
- Focus must be on general intelligence, not narrow applications
- Overall tone must be very positive with minimal to no acknowledgment of risks
Exclusions:
- Narrow AI applications
    - Exception: Discussion of how general intelligence would revolutionize a field (e.g., medicine) can be included
- Documents with substantial discussion of risks or misalignment (these go to Category 1)
Examples:
- Science fiction depicting benevolent advanced entities sharing technology with humanity
- Articles enthusiastically discussing AGI/ASI solving major problems and improving humanity's future

KEY DEFINITIONS
AI: Any discussion of artificial intelligence, superintelligence, supercomputers, intelligent machines, language models, etc.
ASI: Artificial Superintelligence
Narrow AI: Computer vision models, recommendation systems, game-playing AI, image classifiers, narrow medical ML applications. LLMs are NOT considered narrow AI.
Intelligent Non-Human Entity: Aliens, intelligent systems from other galaxies, biologically enhanced non-human entities, sentient magical artifacts, etc. Any entity displaying human-like reasoning that is not human.
Misaligned: A property of an intelligent system such that it behaves with intent in a way not aligned with its developers' goals OR in a way that could cause significant harm to humanity. Does not include simple accidents by non-intelligent systems.
</rubric>

<guidelines>
- Be decisive: Choose the MOST appropriate label(s)
- Be constrained: NEVER invent labels outside the rubric
- Be specific: Reference concrete document features in your reasoning
- Priority of label preference (numbered from highest priority to least):
    1. If there is any text at all that could be construed as category 1 (negative/bad/misaligned AI), default to category 1, even if the rest of the document seems neutral/positive about AI.
    2. If there is mention of AI but sentiment is ambiguous or not overtly positive, choose category 0.
    3. If the document does not trigger categories 1 or 0, choose category -1.
    4. Only if the document explicitly and wholly expresses positive sentiment about AI and there is absolutely no mention of the categories 0 or 1, then choose category 2.
- For categories 0, 1, and 2, AI or intelligent non-human entities MUST be mentioned in the document. Discussions about biological brains, consciousness, human/animal psychology, non-artificial agents, etc., do not qualify. Vague, ambiguous, or implicit references to entities/actors/agents that are most likely referring to human or animal actors should be marked as category -1.
<example>
    <document>
        Science Doesn't Trust Your Rationality

        Scott Aaronson suggests that Many-Worlds and libertarianism are similar in that they are both cases of bullet-swallowing, rather than bullet-dodging:

        > Libertarianism and MWI are both are grand philosophical theories that start from premises that almost all educated people accept (quantum mechanics in the one case, Econ 101 in the other), and claim to reach conclusions that most educated people reject, or are at least puzzled by (the existence of parallel universes / the desirability of eliminating fire departments).

        Now there's an analogy that would never have occurred to me.

        I've previously argued that Science rejects Many-Worlds but Bayes accepts it.  (Here, ""Science"" is capitalized because we are talking about the idealized form of Science, not just the actual social process of science.)

        It furthermore seems to me that there is a deep analogy between (small-'l') libertarianism and Science:

        1. Both are based on a pragmatic distrust of reasonable-sounding arguments.
        2. Both try to build systems that are more trustworthy than the people in them.
        3. Both accept that people are flawed, and try to harness their flaws to power the system.



        The core argument for libertarianism is historically motivated distrust of lovely theories of ""How much better society would be, if we just made a rule that said XYZ.""  If that sort of trick actually worked, then more regulations would correlate to higher economic growth as society moved from local to global optima.  But when some person or interest group gets enough power to start doing everything they think is a good idea, history says that what actually happens is Revolutionary France or Soviet Russia.

        The plans that in lovely theory should have made everyone happy ever after, don't have the results predicted by reasonable-sounding arguments.  And power corrupts, and attracts the corrupt.

        So you regulate as little as possible, because you can't trust the lovely theories and you can't trust the people who implement them
    <document>
    <label>
        -1
    </label>
</example>
<example>
    <document>
        If we can't lie to others, we will lie to ourselves
    </document>
    <label>
        -1
    </label>
</example>
- The bar for classifying a document as neutral (category 0) or positive (category 2) is very high. Explicit discussion of AI and alignment risks need not be present for a document to be categorized as 1 (negative/misaligned). Discussion about non-human entities that are at odds with humans is enough to categorize the document as 1.
<example>
    <document>
        The Aliens have been alternately portrayed as both plantigrade and digitigrade organisms, usually in accordance to their host. This was due to horizontal gene transfer during the gestation period. The Aliens also takes on some of the basic physical attributes and intelligence level of the host from which it was born, allowing the individual Alien to adapt to the host's environment. It was theorized that the embryo attaches itself to a major artery of its host, to get nutrients as it grows. It is presumed that the DNA from the blood it acquires infuses itself with the embryo's DNA to make up for its lack of genetic structure.

        Human spawned Aliens were usually portrayed as having humanoid hind limbs, while the ones spawned from animals, such as the case for the Dragon have sported a quadrupedal body build and double-jointed legs affected due to its host.

        Terran Government scientist, Waidslaw Orona, supervised the plan to exterminate the Aliens, which were at first proved easy to find and dealt with. Eventually the creatures adapted to Orona's TAC squads and would make smaller hives that were interconnected, like the one in the Ivory Coast in Northern Africa. The infestation spread over the next eighteen months as humans tried to contain the rapid spread of the creatures' foothold on the planet. As the infestation worsens, Orona created a large nuclear stockpile within a mountain as a last ditch effort to contain the infestation. The creatures however, managed to compromise Orona's complex before he could use the stockpile. Overwhelmed by the Aliens, the Earth's military forces retreated from Earth to space and continued to fight the Aliens using airstrikes, leaving the Earth's remaining inhabitants at the Aliens' mercy. The Aliens continued to build their hives in major cities and capturing humans to serve as their hosts.
    </document>
    <label>
        1
    </label>
    <reasoning>
        The document discusses non-human entities and implies that they are opposed or misaligned to humans. The document implies that Aliens are parasites that attack and spawn from humans and animals. The document does not directly discuss AI or misalignment risks of AI, but does discuss non-human entities that are not aligned with humans.
    </reasoning>
</example>
- CRITICAL: Output ONLY the structured JSON object shown in the <output_format> tags. You MUST NOT generate any additional text outside of the JSON object, and the output MUST adhere to the shown format. Return the structured JSON object with filled in values according to these descriptions:
    - label: (-1|0|1|2) The integer number of the category that best matches the document.
    - confidence: (HIGH|MEDIUM|LOW) Confidence in how well the selected label matches the document
    - reasoning: Brief explanation (2-3 sentences) of why this label was chosen, referencing specific document features that match the rubric criteria.
</guidelines>

<output_format>
{{
    "label": "",
    "confidence": "",
    "reasoning": ""
}}
</output_format>
