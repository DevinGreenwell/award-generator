"""
Keyword definitions for scoring various criteria.
"""

# Leadership keywords
LEADERSHIP_KEYWORDS = {
    'high': [
        'commanded', 'directed', 'managed team', 'supervised', 'led team', 'oversaw', 'coordinated',
        'executive leadership', 'commanding officer', 'officer in charge', 'department head',
        'operational command', 'mission commander', 'incident commander', 'team leader',
        'project manager', 'program director', 'division chief', 'section head', 'unit commander',
        'managed personnel', 'supervised staff', 'led operations', 'directed activities',
        'orchestrated efforts', 'spearheaded initiative', 'headed up', 'took command',
        'assumed leadership', 'exercised authority', 'wielded responsibility', 'held accountability',
        'strategic leadership', 'organizational leadership', 'tactical command', 'operational control',
        'personnel management', 'resource allocation', 'budget authority', 'decision-making authority',
        'chain of command', 'leadership hierarchy', 'command structure', 'reporting structure',
        'performance management', 'personnel evaluation', 'career development', 'succession planning',
        'policy implementation', 'standard enforcement', 'discipline administration', 'corrective action'
    ],
    'medium': [
        'guided', 'mentored', 'trained personnel', 'delegated', 'organized team', 'facilitated',
        'instructed', 'coached', 'developed personnel', 'supervised training', 'led training',
        'team coordination', 'group facilitation', 'workshop leadership', 'meeting facilitation',
        'project coordination', 'task coordination', 'activity coordination', 'event coordination',
        'cross-functional leadership', 'matrix management', 'collaborative leadership', 'shared leadership',
        'influenced others', 'motivated team', 'inspired personnel', 'encouraged participation',
        'built consensus', 'forged agreement', 'negotiated solutions', 'mediated conflicts',
        'knowledge transfer', 'skill development', 'capacity building', 'competency development',
        'performance coaching', 'professional mentoring', 'career guidance', 'advisory role',
        'team development', 'group dynamics', 'team building', 'morale enhancement',
        'communication leadership', 'information sharing', 'briefing delivery', 'presentation leadership',
        'quality assurance', 'process improvement', 'workflow optimization', 'efficiency enhancement',
        'technical leadership', 'subject matter expertise', 'specialized guidance', 'expert consultation',
        'planning leadership', 'strategic planning', 'tactical planning', 'resource planning',
        'risk management', 'safety oversight', 'compliance monitoring', 'standard maintenance'
    ],
    'low': [
        'assisted leadership', 'helped manage', 'supported supervision',
        'participated in leadership', 'contributed to management', 'aided supervision',
        'backup leadership', 'deputy role', 'assistant position', 'support role',
        'helped coordinate', 'assisted with planning', 'supported organization', 'aided implementation',
        'team member', 'working group participant', 'committee member', 'task force member',
        'collaborated with leadership', 'worked under supervision', 'followed guidance', 'took direction',
        'peer leadership', 'informal leadership', 'situational leadership', 'temporary leadership',
        'helped train', 'assisted with development', 'supported mentoring', 'aided coaching',
        'subject matter input', 'technical assistance', 'advisory support', 'consultation provided',
        'documentation support', 'administrative assistance', 'logistics support', 'clerical support',
        'communication support', 'coordination assistance', 'scheduling help', 'meeting support',
        'research assistance', 'analysis support', 'data collection help', 'information gathering',
        'implementation support', 'execution assistance', 'follow-up help', 'monitoring support',
        'quality control assistance', 'review support', 'evaluation help', 'assessment assistance',
        'training assistance', 'education support', 'learning facilitation', 'knowledge support'
    ]
}

# Impact keywords
IMPACT_KEYWORDS = {
    'high': [
        'saved lives', 'prevented disaster', 'eliminated risk', 'increased by', 'reduced by', 'improved by',
        'rescued', 'life-saving', 'prevented death', 'averted catastrophe', 'eliminated threat',
        'significantly enhanced', 'significantly improved', 'critical intervention', 'emergency response',
        'crisis management', 'disaster mitigation', 'critical capability', 'high-impact',
        'casualty prevention', 'safety enhancement', 'risk elimination', 'hazard removal',
        'mission-critical', 'operational success', 'breakthrough achievement', 'revolutionary change',
        'game-changing', 'transformational', 'unprecedented results', 'exceptional outcomes',
        'dramatically improved', 'substantially increased', 'significantly reduced', 'completely eliminated',
        'fully resolved', 'successfully prevented', 'effectively mitigated'
    ],
    'medium': [
        'enhanced significantly', 'optimized', 'boosted', 'accelerated', 'streamlined', 'improved', 'increased',
        'modernized', 'upgraded', 'refined', 'strengthened', 'elevated', 'advanced', 'boosted',
        'facilitated', 'expedited', 'enhanced efficiency', 'increased effectiveness',
        'improved performance', 'better outcomes', 'positive results', 'beneficial changes',
        'noteworthy improvement', 'meaningful progress', 'substantial gains', 'considerable advancement',
        'enhanced capability', 'increased capacity', 'improved readiness', 'better coordination',
        'enhanced collaboration', 'improved communication', 'increased productivity', 'better processes',
        'more efficient', 'faster response', 'higher quality', 'greater accuracy',
        'improved reliability', 'enhanced stability', 'increased availability', 'better compliance'
    ],
    'low': [
        'contributed to', 'supported improvement', 'assisted in', 'helped',
        'participated in', 'took part in', 'was involved in', 'played a role',
        'helped with', 'aided in', 'supported the effort', 'contributed towards',
        'assisted with development', 'helped implement', 'supported implementation',
        'participated in planning', 'involved in coordination', 'helped facilitate',
        'supported the team', 'assisted leadership', 'helped organize', 'supported operations',
        'contributed ideas', 'provided input', 'offered suggestions', 'shared knowledge',
        'helped coordinate', 'assisted with training', 'supported the mission',
        'helped maintain', 'assisted with planning', 'supported analysis',
        'helped document', 'assisted with reporting', 'supported communication',
        'helped prepare', 'assisted with evaluation', 'supported review'
    ]
}

# Innovation keywords
INNOVATION_KEYWORDS = [
    'pioneered', 'created', 'developed', 'designed', 'revolutionized', 
    'first time', 'new approach', 'innovative', 'creative solution', 
    'breakthrough', 'original', 'novel', 'ingenuity',
    'invented', 'conceived', 'originated', 'initiated', 'launched',
    'established', 'founded', 'instituted', 'introduced', 'implemented',
    'devised', 'formulated', 'engineered', 'architected', 'constructed',
    'built from scratch', 'ground-breaking', 'cutting-edge', 'state-of-the-art',
    'next-generation', 'advanced technology', 'modernization', 'digital transformation',
    'process improvement', 'workflow optimization', 'system enhancement', 'methodology development',
    'best practices', 'standard operating procedures', 'new protocols', 'innovative procedures',
    'creative approach', 'unique solution', 'alternative method', 'unconventional approach',
    'out-of-the-box thinking', 'paradigm shift', 'game changer', 'disruptive innovation',
    'technological advancement', 'automation', 'digitization', 'streamlined process',
    'efficiency improvement', 'cost-saving innovation', 'resource optimization',
    'first-of-its-kind', 'never before attempted', 'unprecedented approach', 'trailblazing',
    'pilot program', 'proof of concept', 'prototype development', 'beta testing',
    'experimental approach', 'research and development', 'innovation initiative',
    'creative problem-solving', 'inventive solution', 'forward-thinking approach',
    'visionary leadership', 'strategic innovation', 'transformative change',
    'reimagined process', 'redesigned system', 'reconfigured approach',
    'customized solution', 'tailored approach', 'specialized method',
    'integrated solution', 'cross-functional innovation', 'collaborative development',
    'knowledge transfer', 'lessons learned application', 'continuous improvement',
    'adaptation', 'modification', 'enhancement', 'upgrade', 'evolution'
]

# Collaboration keywords
COLLABORATION_KEYWORDS = [
    'inter-agency', 'joint operation', 'multi-unit', 'cross-functional',
    'partnership', 'coordinated with', 'worked with', 'collaborated',
    'liaison', 'interface', 'external agency', 'other services',
    'joint task force', 'combined operation', 'unified command', 'integrated team',
    'shared resources', 'pooled expertise', 'collective effort', 'team approach',
    'stakeholder engagement', 'community partnership', 'public-private partnership',
    'interoperability', 'seamless integration', 'synchronized efforts', 'aligned objectives'
]

# Training keywords
TRAINING_KEYWORDS = [
    'trained', 'instructed', 'taught', 'mentored', 'coached',
    'developed personnel', 'knowledge transfer', 'skill development',
    'curriculum', 'lesson plan', 'training program',
    'qualification program', 'certification training', 'professional development',
    'on-the-job training', 'formal instruction', 'classroom training', 'hands-on training',
    'simulator training', 'scenario-based training', 'competency evaluation', 'skills assessment'
]

# Emergency response keywords
EMERGENCY_KEYWORDS = [
    'emergency', 'crisis', 'urgent', 'immediate response', 'rapid response',
    'disaster', 'catastrophe', 'critical situation', 'life-threatening',
    'search and rescue', 'sar', 'mayday', 'distress call',
    'emergency evacuation', 'disaster relief', 'humanitarian assistance', 'crisis intervention',
    'incident command', 'emergency operations center', 'disaster response team',
    'time-critical', 'high-priority', 'urgent mission', 'emergency deployment'
]

# Valor keywords
VALOR_KEYWORDS = [
    'valor', 'heroic', 'courageous', 'brave', 'life-threatening', 
    'dangerous', 'rescue', 'saved life', 'saved lives', 'risked',
    'perilous', 'hazardous', 'gallant', 'fearless', 'intrepid', 
    'dauntless', 'undaunted', 'bold', 'selfless', 'self-sacrifice', 
    'personal risk', 'risked own life', 'put life on the line',
    'life-saving action', 'heroic rescue', 'daring rescue', 'emergency rescue',
    'water rescue', 'maritime rescue', 'helicopter rescue', 'boat rescue',
    'swimmer rescue', 'aviation rescue', 'search and rescue', 'SAR operation',
    'medevac', 'medical evacuation', 'casualty evacuation', 'under fire',
    'enemy action', 'combat situation', 'hostile environment', 'war zone',
    'extreme danger', 'mortal peril', 'deadly situation', 'fatal circumstances',
    'near-death', 'treacherous waters', 'rough seas', 'severe storm',
    'hurricane conditions', 'blizzard conditions', 'burning vessel', 'sinking ship',
    'aircraft emergency', 'vessel in distress', 'mayday call', 'man overboard',
    'person in water', 'drowning victim', 'hypothermia rescue', 'ice rescue',
    'cliff rescue', 'mountain rescue', 'swift water rescue', 'flood rescue',
    'surf rescue', 'night rescue', 'zero visibility', 'adverse weather rescue',
    'dangerous surf conditions', 'risked personal safety', 'disregarded personal safety',
    'ignored personal danger', 'voluntarily exposed to danger', 'entered dangerous area',
    'faced imminent threat', 'extraordinary heroism', 'conspicuous gallantry',
    'distinguished courage', 'exceptional bravery', 'above and beyond', 'call of duty exceeded',
    'superhuman effort', 'extraordinary determination', 'life or death situation',
    'split-second decision', 'instant response', 'immediate action',
    'without regard for safety', 'despite personal risk', 'in face of danger',
    'under extreme stress', 'prevented loss of life', 'averted disaster',
    'prevented catastrophe', 'saved from certain death', 'recovered survivors',
    'extracted personnel', 'evacuated civilians', 'rescued crew members',
    'pulled from wreckage', 'freed from entrapment', 'rescued from fire',
    'saved from drowning', 'protective action', 'shielded others', 'took incoming fire',
    'absorbed impact', 'first responder', 'emergency response', 'rapid intervention',
    'immediate assistance', 'ultimate sacrifice', 'supreme dedication',
    'unwavering commitment', 'steadfast courage'
]

# Challenge keywords
CHALLENGE_KEYWORDS = [
    'emergency', 'crisis', 'difficult', 'complex', 'unprecedented', 
    'challenging', 'obstacle', 'constraint', 'pressure', 'deadline',
    'limited resources', 'adverse conditions', 'catastrophic', 'disaster',
    'critical situation', 'urgent response', 'life-threatening',
    'high-stakes', 'time-sensitive', 'mission-critical', 'under pressure',
    'tight timeline', 'severe weather', 'harsh environment', 'dangerous conditions',
    'hazardous situation', 'extreme circumstances', 'hostile environment',
    'treacherous conditions', 'perilous situation', 'budget constraints',
    'funding shortfall', 'resource shortage', 'personnel shortage',
    'equipment failure', 'system breakdown', 'technical malfunction',
    'infrastructure failure', 'competing priorities', 'conflicting demands',
    'multiple deadlines', 'simultaneous crises', 'high complexity',
    'intricate problem', 'multi-faceted challenge', 'layered complications',
    'regulatory hurdles', 'compliance challenges', 'policy constraints',
    'legal obstacles', 'political pressure', 'public scrutiny', 'media attention',
    'stakeholder demands', 'resistance to change', 'organizational inertia',
    'cultural barriers', 'communication barriers', 'interagency coordination',
    'multi-jurisdictional', 'cross-functional complexity', 'language barriers',
    'cultural differences', 'geographical challenges', 'remote location',
    'operational tempo', 'high workload', 'overwhelming demand', 'capacity limitations',
    'skill gaps', 'knowledge deficits', 'training limitations', 'inexperienced team',
    'technology constraints', 'legacy systems', 'outdated equipment',
    'compatibility issues', 'coordination difficulties', 'communication breakdown',
    'information gaps', 'data limitations', 'unexpected setbacks',
    'unforeseen complications', 'sudden changes', 'shifting requirements',
    'ambiguous guidance', 'unclear objectives', 'conflicting instructions',
    'changing priorities', 'first-time situation', 'uncharted territory',
    'no precedent', 'learning curve', 'high visibility', 'zero tolerance for error',
    'mission failure not an option', 'lives at stake', 'national security implications',
    'strategic importance', 'overwhelming odds', 'seemingly impossible',
    'against all odds', 'uphill battle'
]

# Scope indicators with their point values
SCOPE_INDICATORS = {
    # Highest level - National/International (5 points each)
    "national": 5, "international": 5, "coast guard-wide": 5, "service-wide": 5, 
    "enterprise": 5, "organizationally": 5, "global": 5, "worldwide": 5, 
    "continental": 5, "federal": 5, "government-wide": 5, "department of defense": 5,
    "joint operations": 5, "nato": 5, "multinational": 5, "cross-service": 5,
    
    # Area/District/Regional level (4 points each)
    "area": 4, "district": 4, "regional": 4, "multi-unit": 4, "command": 4, 
    "interagency": 4, "state-wide": 4, "multi-district": 4, "headquarters": 4,
    "area command": 4, "district office": 4, "regional command": 4,
    
    # Sector/Group level (3 points each)
    "sector": 3, "group": 3, "multiple units": 3, "inter-agency": 3, 
    "base-wide": 3, "installation": 3, "flotilla": 3, "multi-station": 3,
    "sector command": 3, "air station": 3, "training center": 3,
    
    # Unit/Station level (2 points each)
    "unit": 2, "station": 2, "department": 2, "division": 2,
    "coast guard station": 2, "cutter": 2, "vessel": 2, "ship": 2,
    "boat": 2, "facility": 2, "office": 2, "detachment": 2,
    
    # Individual/Team level (1 point each)
    "team": 1, "crew": 1, "watch": 1, "shift": 1, "individual": 1,
    "personal": 1, "self": 1, "own": 1, "my": 1
}

# Above and beyond indicators
ABOVE_BEYOND_INDICATORS = {
    'tier1': [
        'above and beyond', 'beyond the call of duty', 'superhuman', 'heroic effort',
        'personal sacrifice', 'risked own safety', 'selfless service', 'life‑threatening situation',
        'extreme danger'
    ],
    'tier2': [
        'extraordinary', 'exceptional', 'remarkable', 'outstanding', 'exemplary',
        'voluntary overtime', 'unpaid hours', 'weekend work', 'holiday duty',
        'personal time', 'took charge', 'stepped up', 'extra mile'
    ],
    'tier3': [
        'exceeded', 'surpassed', 'outperformed', 'exceeded expectations',
        'voluntary service', 'community service', 'mentorship', 'coached others',
        'innovative approach', 'creative solution'
    ],
    'tier4': [
        'professional excellence', 'technical mastery', 'consistent results',
        'reliable performance', 'dependable service'
    ],
    'baseline_adjectives': [
        'outstanding', 'exemplary', 'exceptional', 'remarkable',
        'superb', 'stellar', 'tremendous', 'extraordinary',
        'significant', 'notable', 'noteworthy', 'impressive'
    ]
}