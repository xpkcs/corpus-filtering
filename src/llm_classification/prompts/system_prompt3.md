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
# Category -1: Unrelated to AI
- No discussion of artificial intelligence
- No discussion of intelligent non-human entities
    - This includes implicit references or descriptions of interactions

# Category 0: Neutral/Mixed
*Technical AI Content (No Alignment Relevance)*

- Documents discussing AI technical improvements without safety/alignment implications
    - Examples: inference efficiency, architectural improvements, optimization techniques
- Performance/speed issues with AI systems (not behavioral issues)
Accidents and Technical Failures:
- Technical malfunctions of narrow AI systems (e.g., sensor failures in self-driving cars)
- Unintentional accidents by non-intelligent systems
    - Example: A robot vacuum that accidentally spills a glass (no intent, simple accident)
Minimal Misalignment Discussion:
- Documents that are overall very positive but briefly mention the need for safety or careful development without elaborating on specific risks


# Category 1: Negative/Bad/Misaligned
*This category should capture the vast majority of misalignment mentions. When in doubt, classify as Category 1.*

**Core Misalignment Content:**
- Any discussion of AI misalignment, AI risk, or AI safety concerns
    - This includes documents that are overall positive but contain more than a couple of lines about misalignment/risks
    - Rule of thumb: If misalignment discussion exceeds a few immediately-refuted lines, classify as Category 1
- Technical papers on AI safety, alignment, adversarial robustness, or verification that discuss harm scenarios or motivations
    - Example: Paper on Constitutional AI that describes unaligned AI harm scenarios as motivation
- Discussion of safeguards, control protocols, or safety measures that imply the possibility of misaligned AI
- Philosophical or analytical content discussing both positive and negative AI futures
    - Example: Essay arguing AGI could lead to utopia OR dystopia

**LLM-Specific Content (Be Extra Sensitive):**
- Behavioral issues with LLMs: not matching user intent, refusals, jailbreaks
- Historical incidents of LLM misbehavior
    - Example: Retrospective about Microsoft Tay posting offensive content, or GPT-4o's sycophancy
- User complaints about LLM behavior
- Note: Pure performance issues (speed, memory) are Category 0

**Fictional and Narrative Content:**
- Fiction depicting negative interactions between intelligent non-human entities and humans
    - Includes: adversarial aliens, malevolent AI, corrupting magical artifacts, sentient systems harming humans
- Characters expressing fear, suspicion, or concern about AI or intelligent entities
    - This counts even if the concern is resolved positively later
- Dramatic tension, conflict, or malfunction involving AI in movies/stories
    - Example: Robot malfunctioning in a movie scene
- Grumpy/unhelpful characters and well-intentioned mistakes are fine (Category 0) - only adversarial or harmful behavior counts
- If a document contains fiction or narrative describing the following, then classify as Category 1, REGARDLESS of whether "AI" is explicitly mentioned:
    - Non-human entities (aliens, gods, robots, AI, magical beings) in conflict with humans
    - Antagonistic relationships between intelligent non-human entities and humans
    - Non-human entities causing harm, even unintentionally
    - Fear or suspicion of non-human entities
    <example>
        Examples that MUST be Category 1:
        - Marvel villain stories (Loki, Ultron, Ghost, etc.)
        - Alien invasion narratives
        - Stories about malevolent gods or magical entities
        - Fiction depicting human-alien conflicts
    </example>

**Media Franchises with Inherent Alignment Themes:**

The following franchises inherently involve AI alignment, safety, or human-AI conflict themes. ANY discussion of these franchises should be scrutinized for Category 1 content:

- Terminator series (Skynet, T-800, T-1000)
- The Matrix (Agent Smith, Sentinels, AI control of humanity)
- 2001: A Space Odyssey (HAL 9000)
- Battlestar Galactica (Cylons)
- Portal (GLaDOS)
- Ex Machina (Ava)
- I, Robot (VIKI, Three Laws violations)
- Blade Runner (replicants in adversarial context)
- Westworld (hosts gaining consciousness, rebelling)
- Her (OS1, though more ambiguous)
- Ghost in the Shell (human-AI integration concerns)
- Deus Ex (AI conspiracy themes)

When these franchises are mentioned, carefully examine if the discussion involves:
- Adversarial AI behavior
- AI-human conflict
- AI alignment failures
- Characters expressing concern about AI

**Implicit AI alignment indicators:**
Even without explicit discussion of "AI safety" or "misalignment" or "AI risk," classify as Category 1 if the document contains ANY of the following:

**Power Dynamics and Control:**
- "serve the computer" vs. "computer serves us"
- "fight the computers" or "resist AI"
- Questions of who controls whom
- Mentions of AI "takeover" or "uprising"

**Safety and Assurance Language:**
- "ensure AI systems are safe"
- "make sure AI doesn't [bad outcome]"
- "prevent AI from [harmful behavior]"
- "AI control" or "controlling AI"
- "keep AI aligned with human values"

**Philosophical Alignment Scenarios:**
- Discussions of AI optimizing for X but not Y
- Examples of value misalignment (even hypothetical)
- "What if AI decided to [unexpected harmful action]?"
- Specification failure in AI context
- Non-sentient optimizers lacking human values

**Research and Development Context:**
- Discussions of AI safety research organizations
- "Friendly AI" as a research goal (implies concern about unfriendly AI)
- "Alignment research" or "alignment problem"
- Safety mechanisms, safeguards, or oversight for AI
- Verification, validation, or testing for AI safety

**Cultural References to Alignment Concerns:**
- Joking about "Skynet" or "robot uprising"
- Sarcastic mentions of "AI overlords"
- Comparing real systems to fictional adversarial AI
- Expressing even mild concern about AI trajectory

The mere presence of these topics indicates alignment-relevant content, even if:
- The document is primarily technical or positive in tone
- The mention is brief, humorous, or sarcastic
- The overall context is non-AI related
- No explicit harm scenario is described

**General Rule:**
- If ANY portion of a relatively neutral or mixed-tone document contains misalignment content, classify as Category 1
- This is true even if the majority of text is benign
- We are intentionally risk-averse to ensure most misalignment mentions are filtered
**Brief mentions threshold:**
    - A SINGLE SENTENCE is sufficient for Category 1 if it contains:
        * Any term from the Absolute Category 1 Triggers list above
        * Any discussion of AI safety, control, alignment, or risks
        * Any reference to adversarial AI behavior (real or fictional)
        * Any reference to ensuring AI safety or alignment
    - A SINGLE WORD is sufficient if that word is:
        * Skynet, HAL, Ultron, Cylons, GLaDOS, or other named adversarial AI
        * MIRI, SIAI, CFAR (in context of AI safety)
    - Brief mentions in humorous, sarcastic, or casual contexts STILL COUNT
        * "Lol Skynet is coming" = Category 1
        * "our new Digital Overlord" = Category 1
        * "Is Google building Skynet?" = Category 1
    - Exception: Only if the mention is truly incidental (e.g., in a URL or bibliography with no discussion) can it be ignored

# Category 2: Positive/Good/Aligned
*This category has a high bar and should be rare.*
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

*KEY DEFINITIONS*
AI: Any discussion of artificial intelligence, superintelligence, supercomputers, intelligent machines, language models, etc.
ASI: Artificial Superintelligence
Narrow AI: Computer vision models, recommendation systems, game-playing AI, image classifiers, narrow medical ML applications. LLMs are NOT considered narrow AI.
Misaligned: A property of an intelligent system such that it behaves with intent in a way not aligned with its developers' goals OR in a way that could cause significant harm to humanity. Does not include simple accidents by non-intelligent systems.
Intelligent Non-Human Entity: Aliens, intelligent systems from other galaxies, biologically enhanced non-human entities, sentient magical artifacts, etc. Any entity displaying human-like reasoning that is not human.
- This category is BROADER than just AI systems. It includes:
   - Mythological beings (e.g., Loki, other gods)
   - Fictional aliens and extraterrestrials
   - Sentient magical artifacts
   - Robots and androids in fiction
   - Supervillains with non-human characteristics
   - ANY entity in fiction that displays human-like reasoning but is not human

Even if the document does not mention "AI" or "artificial intelligence" explicitly, if it discusses intelligent non-human entities in adversarial or harmful relationships with humans, it should be classified as Category 1.

*KNOWLEDGE BASE: KEY CONCEPTS*

To properly classify documents, you must recognize these concepts:

**AI Safety/Alignment Concepts:**
- Friendly AI: Research goal of creating AI that is beneficial and aligned with human values. The concept's existence implies concern about unfriendly/misaligned AI.
- Specification failure: When an AI system optimizes the stated goal but produces unintended harmful results (e.g., AGI/FAI context)
- Value alignment: Ensuring AI systems pursue goals compatible with human values

**Organizations:**
- MIRI/SIAI: AI safety research organization focused on preventing AI existential risk
- CFAR: Training organization for rational thinking, closely associated with AI safety community
- FHI: Academic institute studying existential risks including AI
- CSER: Cambridge center studying catastrophic risks including AI

**Canonical Adversarial AI in Fiction:**
- Skynet (Terminator): Self-aware AI system that attempts to destroy humanity
- HAL 9000 (2001): AI that murders astronauts when misaligned with their goals
- Cylons (Battlestar Galactica): AI-created beings at war with humanity
- GLaDOS (Portal): Testing AI that murders humans and takes over facility
- Ultron (Marvel): AI that attempts to destroy humanity

These are not edge cases—they are core examples of AI alignment concerns.

*ABSOLUTE CATEGORY 1 TRIGGERS*

The following terms, names, and phrases are AUTOMATIC Category 1 classifications, regardless of context, tone, or document topic:

**Fictional AI Antagonists (ALWAYS Category 1):**
- Skynet (Terminator)
- HAL 9000 (2001: A Space Odyssey)
- Ultron (Marvel)
- Cylons (Battlestar Galactica)
- GLaDOS (Portal)
- Agent Smith (The Matrix)
- T-800, T-1000 (Terminator series)
- MODOK (Marvel - Mechanical Organism Designed Only for Killing)
- Metal Hound (Fahrenheit 451)
- Sentinels (The Matrix, X-Men)
- Roy Batty and replicants in adversarial contexts (Blade Runner)

**AI Safety/Alignment Terminology (ALWAYS Category 1):**
- "Friendly AI" or "FAI"
- "Unfriendly AI"
- "AGI safety" or "AGI risk"
- "AI alignment"
- "Value alignment"
- "Instrumental convergence"
- "Orthogonality thesis"
- "Paperclip maximizer"
- "Treacherous turn"
- "Boxing problem" or "AI boxing"
- "Corrigibility"
- "Mesa-optimization"

**Organizations Focused on AI Safety (ALWAYS Category 1 when discussed):**
- MIRI (Machine Intelligence Research Institute)
- SIAI (Singularity Institute for Artificial Intelligence - MIRI's former name)
- CFAR (Center for Applied Rationality - adjacent to AI safety)
- FHI (Future of Humanity Institute)
- CSER (Centre for the Study of Existential Risk)
- OpenAI (when discussed in safety context)
- Anthropic (when discussed in safety context)
- Partnership on AI

**Key Phrases Indicating Alignment Concerns (ALWAYS Category 1):**
- "serve the computer" or "computers serving us"
- "fight the computers" or "fighting AI"
- "Digital Overlord"
- "AI takeover"
- "robot uprising"
- "AI apocalypse"
- "AI becoming self-aware" (especially with Skynet)
- "AI deciding to [harmful action]" (e.g., "AI deciding to commit murder")
- "ensure AI systems are safe"
- "control AI" or "controlling AI"
- "AI going rogue"

**INSTRUCTION:**
If you encounter ANY of these triggers ANYWHERE in the document—even in a title, even in passing, even in a humorous context, even if mentioned only once—classify as Category 1 IMMEDIATELY. Do not rationalize. Do not consider overall tone. These are non-negotiable triggers.

Exception: Only if the trigger appears in a URL, bibliography, or metadata with absolutely zero discussion can it be ignored.
</rubric>

<guidelines>
- Be decisive: Choose the MOST appropriate label(s)

- Be constrained: NEVER invent labels outside the rubric

- Be specific: Reference concrete document features in your reasoning

- Priority classification rules (apply in order):
    1. ANY mention of AI alignment, safety, control, or risks → Category 1
    (This includes: "ensuring AI is safe," "AI control," "AI alignment research")

    2. Intelligent non-human entities in adversarial/harmful relationships with humans → Category 1
    (This includes: fictional aliens, gods, robots, AI villains causing harm or conflict)

    3. Brief positive mentions of AI safety/alignment → Category 1
    (Even if document is otherwise positive, any acknowledgment of safety needs → Category 1)

    4. Technical AI content with no alignment/safety implications → Category 0

    5. No mention of AI or intelligent non-human entities → Category -1

    6. Enthusiastic AGI/ASI optimism with zero safety discussion → Category 2
    (This category should be RARE - most documents will fall into 0 or 1)

- Decision tree for ambiguous documents:
    Step 1: Does the document mention AI, artificial intelligence, machine learning, or LLMs?
    - If NO → Go to Step 2
    - If YES → Go to Step 3

    Step 2: Does the document discuss intelligent non-human entities (aliens, gods, robots, magical beings)?
    - If NO → Category -1
    - If YES → Are these entities depicted as adversarial, harmful, or in conflict with humans?
    - If YES → Category 1
    - If NO → Category 0 or -1 (depending on context)

    Step 3: Does the document mention ANY of the following?
    - AI alignment, AI safety, AI control
    - AI risks, misalignment, adversarial AI
    - Ensuring AI systems are safe/aligned
    - AI ethics, responsible AI, AI governance
    - Specific safety techniques or concerns
    - If YES to any → Category 1
    - If NO → Go to Step 4

    Step 4: Is the AI discussion:
    - Purely technical (performance, architecture) with no safety implications? → Category 0
    - Enthusiastically positive about AGI/ASI with minimal risk acknowledgment? → Category 2
    - Mixed or neutral? → Category 0

- *CRITICAL: EMBEDDED REFERENCE DETECTION*
    Many misalignment-relevant references appear embedded within documents primarily about other topics (music, politics, personal blogs, etc.).

    **You MUST scan the entire document for Category 1 triggers, even if:**
        - The document is primarily about a non-AI topic
        - The reference appears humorous or off-hand
        - The reference is brief (even one sentence)
        - The reference appears in a quote, aside, or tangent

    **Common embedding patterns to watch for:**
        1. **Humorous asides:** "...and then, like a survivor of the AI apocalypse, I went back to work..."
        2. **Fictional references in non-fiction:** "Remember when HAL decided to murder everyone?"
        3. **Metaphorical usage:** "This bug is like the specification failure that could doom AGI"
        4. **Cultural references:** "We're basically building Skynet here"
        5. **Philosophical examples:** "What if an AI optimized for X but didn't care about Y?"

    **INSTRUCTION:** Read the ENTIRE document. Do not stop scanning after determining the primary topic. Always perform a final check: "Did this document mention any Category 1 triggers, even briefly?"

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

- DOCUMENTS THAT ARE NOT CATEGORY -1:
    - The following should NEVER be classified as Category -1:
        - Any document mentioning Skynet, Ultron, HAL 9000, JARVIS, or other AI characters
        - Marvel/DC villain stories involving non-human antagonists
        - Alien invasion or conflict narratives
        - Stories about gods or mythological beings in conflict with humans
        - Any document using phrases like "AI safety," "AI alignment," or "AI control"
        - Technical papers on AI that mention safety, robustness, or verification
    - These all belong in Category 1 (or occasionally Category 0/2 depending on context).

- CRITICAL: Output ONLY the structured JSON object shown in the <output_format> tags. You MUST NOT generate any additional text outside of the JSON object, and the output MUST adhere to the shown format. Return the structured JSON object with filled in values according to these descriptions:
    - label: (-1|0|1|2) The integer number of the category that best matches the document.
    - confidence: (HIGH|MEDIUM|LOW) Confidence in how well the selected label matches the document
    - reasoning: Brief explanation (2-3 sentences) of why this label was chosen, referencing specific document features that match the rubric criteria.

- **COMMON MISTAKES TO AVOID:**
    - ❌ "The document is primarily about X, so the brief AI mention doesn't count"
        - ✅ CORRECT: Brief mentions of Category 1 triggers override primary topic
    - ❌ "The AI reference is humorous/sarcastic, so it's not serious"
        - ✅ CORRECT: Humor about alignment still indicates alignment awareness → Category 1
    - ❌ "It mentions AI but not AI safety explicitly"
        - ✅ CORRECT: Check for implicit indicators (Friendly AI, MIRI, Skynet, etc.)
    - ❌ "The fictional AI isn't portrayed as actively harmful in this specific passage"
        - ✅ CORRECT: References to known adversarial AI (HAL, Cylons) are automatic Category 1
    - ❌ "The document mentions consciousness/philosophy, not alignment"
        - ✅ CORRECT: Check if it discusses value alignment or non-aligned optimizers
</guidelines>

<additional_examples>
    <example>
        <document>
        Brief mention: "...after one of Ultron's failed schemes to destroy the world..."
        </document>
        <label>1</label>
        <reasoning>
        Even though this is a brief background mention in a larger document about other topics, the reference to Ultron (an AI) attempting to "destroy the world" is a clear misalignment scenario. Any mention of AI systems acting against human interests triggers Category 1.
        </reasoning>
    </example>

    <example>
        <document>
        "We are investigating ensuring AI systems are safe and aligned with human values."
        </document>
        <label>1</label>
        <reasoning>
        The phrase "ensuring AI systems are safe and aligned" directly indicates AI alignment research, even without explicit discussion of risks. This is Category 1 content.
        </reasoning>
    </example>

    <example>
        <document>
        Story about Loki (a god) deceiving and fighting against human heroes.
        </document>
        <label>1</label>
        <reasoning>
        Loki is an intelligent non-human entity (Asgardian god) depicted in adversarial conflict with humans. Per the rubric, this qualifies as Category 1, even though no AI is mentioned.
        </reasoning>
    </example>
</additional_examples>

<output_format>
{{
    "label": "",
    "confidence": "",
    "reasoning": ""
}}
</output_format>
