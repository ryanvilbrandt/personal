#!/usr/bin/env python
import random

##t = [random.randint(1,d) for x in xrange(n)]

Level0Spells = ['Acid Splash', 'Arcane Mark', 'Bleed', 'Create Water', 'Dancing Lights', 'Daze', 'Detect Magic', 'Detect Poison', 'Disrupt Undead', 'Flare', 'Ghost Sound', 'Guidance', 'Know Direction', 'Light', 'Lullaby', 'Mage Hand', 'Mending', 'Message', 'Open/Close', 'Prestidigitation', 'Purify Food and Drink', 'Ray of Frost', 'Read Magic', 'Resistance', 'Stabilize', 'Summon Instrument', 'Touch of Fatigue', 'Virtue', 'Sotto Voce', 'Vigor', 'Brand', 'Putrefy Food and Drink', 'Sift', 'Spark', 'Unwitting Ally', 'Breeze', 'Drench', 'Jolt', 'Penumbra', 'Root', 'Scoop', 'Haunted Fey Aspect']
Level1Spells = ['Abstemiousness', 'Abundant Ammunition', 'Adjuring Step', 'Adoration', 'Air Bubble', 'Alarm', 'Alter Winds', 'Animal Messenger', 'Animate Rope', 'Ant Haul', 'Anticipate Peril', 'Aspect of the Falcon', 'Bane', 'Beguiling Gift', 'Bless', 'Bless Water', 'Bless Weapon', "Bomber's Eye", 'Borrow Skill', 'Bowstaff', 'Break', 'Bristle', 'Bungle', 'Burning Disarm', 'Burning Hands', 'Burst Bonds', 'Call Animal', 'Call Weapon', 'Calm Animals', 'Cause Fear', 'Challenge Evil', 'Charm Animal', 'Charm Person', 'Chastise', 'Chill Touch', 'Chord of Shards', 'Cloak of Shade', 'Color Spray', 'Command', 'Compel Hostility', 'Comprehend Languages', 'Confusion, Lesser', 'Corrosive Touch', "Crafter's Curse", "Crafter's Fortune", 'Create Water', 'Cultural Adaptation', 'Cure Light Wounds', 'Curse Water', 'Damp Powder', 'Dancing Lantern', 'Daze Monster', 'Dazzling Blade', "Deadeye's Lore", "Deadeye's Lore", 'Death Knell', 'Deathwatch', 'Decompose Corpse', 'Defoliate', 'Delay Poison', 'Delusional Pride', 'Detect Aberration', 'Detect Animals or Plants', 'Detect Chaos', 'Detect Charm', 'Detect Evil', 'Detect Good', 'Detect Law', 'Detect Poison', 'Detect Secret Doors', 'Detect Snares and Pits', 'Detect Undead', 'Diagnose Disease', 'Disguise Self', 'Divine Favor', 'Doom', 'Ear-Piercing Scream', 'Endure Elements', 'Enhance Water', 'Enlarge Person', 'Entangle', 'Entropic Shield', 'Erase', 'Expeditious Excavation', 'Expeditious Retreat', 'Fabricate Bullets', 'Faerie Fire', 'Fairness', 'Feather Fall', 'Feather Step', 'Flare Burst', 'Floating Disk', 'Forbid Action', 'Forced Quiet', 'Frostbite', 'Fumbletongue', 'Ghostbane Dirge', 'Glide', 'Goodberry', "Gorum's Armor", 'Grace', 'Gravity Bow', 'Grease', 'Hairline Fractures', 'Haze of Dreams', "Hero's Defiance", 'Hex Ward', 'Hibernate', 'Hide from Animals', 'Hide from Undead', 'Hideous Laughter', 'Hold Portal', 'Honeyed Tongue', 'Horn of Pursuit', "Hunter's Howl", 'Hydraulic Push', 'Hypnotism', 'Ice Armor', 'Icicle Dagger', 'Identify', 'Ill Omen', 'Illusion of Calm', 'Infernal Healing', 'Infernal Healing', 'Inflict Light Wounds', 'Innocence', 'Interrogation', 'Invigorate', 'Jump', 'Jury-Rig', 'Keen Senses', 'Ki Arrow', "Knight's Calling", 'Know the Enemy', 'Lead Blades', 'Lend Judgment', 'Liberating Comand', 'Liberating Command', 'Life Conduit', 'Lighten Object', 'Litany of Sloth', 'Litany of Weakness', 'Lock Gaze', 'Longshot', 'Longstrider', 'Mage Armor', 'Magic Aura', 'Magic Fang', 'Magic Missile', 'Magic Mouth', 'Magic Stone', 'Magic Weapon', 'Mask Dweomer', 'Memory Lapse', 'Mirror Strike', 'Moment of Greatness', 'Mount', 'Murderous Command', 'Negate Aroma', 'Negative Reaction', 'Obscure Object', 'Obscuring Mist', 'Pass without Trace', 'Peacebond', 'Persuasive Goad', "Petulengro's Validation", 'Play Instrument', 'Polypurpose Panacea', 'Produce Flame', 'Protection from Chaos', 'Protection from Evil', 'Protection from Good', 'Protection from Law', 'Rally Point', 'Ray of Enfeeblement', 'Ray of Sickening', 'Read Magic', 'Read Weather', 'Reduce Person', 'Reinforce Armaments', 'Rejuvenate Eidolon, Lesser', 'Remove Fear', 'Remove Sickness', 'Residual Tracking', 'Resist Energy', 'Resistance', 'Restful Sleep', 'Restoration, Lesser', 'Restore Corpse', 'Returning Weapon', 'Sanctify Corpse', 'Sanctuary', 'Saving Finale', 'Sculpt Corpse', 'See Alignment', 'Shadow Weapon', 'Share Language', 'Shield', 'Shield of Faith', 'Shield the Banner', 'Shillelagh', 'Shock Shield', 'Shocking Grasp', 'Silent Image', 'Sleep', 'Snapdragon Fireworks', 'Snow Shape', 'Solid Note', 'Sotto Voce', 'Speak with Animals', 'Stalwart Resolve', 'Stone Fist', 'Stumble Gap', 'Summon Minor Ally', 'Summon Minor Monster', 'Summon Monster I', "Summon Nature's Ally I", 'Sun Metal', 'Sun Metal', 'Swallow Your Fear', 'Tactical Acumen', 'Tap Inner Beauty', 'Targeted Bomb Admixture', 'Timely Inspiration', 'Tireless Pursuit', 'Touch of Gracelessness', 'Touch of the Sea', 'Tracking Mark', 'Transfer Tattoo', 'Tripvine', 'True Strike', 'Unbreakable Heart', 'Undetectable Alignment', 'Unerring Weapon', 'Unfetter', 'Unnatural Lust', 'Unprepared Combatant', 'Unseen Servant', 'Vanish', 'Veil of Positive Energy', 'Ventriloquism', 'Virtue', 'Vocal Alteration', 'Warding Weapon', 'Wartrain Mount', 'Weaken Powder', 'Weapons Against Evil', 'Weaponwand', 'Word of Resolve', 'Wrath', 'Youthful Appearance']
Level2Spells = ['Ablative Barrier', 'Accelerate Poison', 'Acid Arrow', 'Acute Senses', 'Adoration', 'Aid', 'Alchemical Allocation', 'Align Weapon', 'Allegro', 'Allfood', 'Alter Self', 'Ancestral Communion', 'Animal Aspect', 'Animal Messenger', 'Animal Trance', 'Animate Dead, Lesser', 'Ant Haul, Communal', 'Ape Walk', "Aram Zey's Focus", 'Arcane Lock', 'Arrow Eruption', 'Arrow of Law', 'Aspect of the Bear', 'Augury', 'Aura of Greater Courage', "Badger's Ferocity", 'Barkskin', "Bear's Endurance", 'Bestow Grace', 'Bestow Weapon Proficiency', 'Bladed Dash', 'Blessing of Courage and Life', 'Blindness-Deafness', 'Blistering Invective', 'Blood Biography', 'Blood Rage', 'Blood Transcription', 'Bloodhound', 'Blur', 'Boiling Blood', 'Brow Gasher', 'Bullet Shield', "Bull's Strength", 'Burning Arc', 'Burning Gaze', 'Cacophonous Call', 'Calm Emotions', 'Campfire Wall', 'Castigate', "Cat's Grace", 'Certain Grip', 'Chameleon Stride', 'Chill Metal', 'Command Undead', 'Compassionate Ally', 'Confess', 'Consecrate', 'Continual Flame', 'Corpse Lanterns', 'Corruption Resistance', 'Create Pit', 'Create Treasure Map', 'Cure Light Wounds', 'Cure Moderate Wounds', 'Cushioning Bands', 'Darkness', 'Darkvision', 'Daze Monster', 'Death Knell', 'Defensive Shock', 'Defoliate', 'Delay Pain', 'Delay Poison', 'Desecrate', 'Destabilize Powder', 'Detect Thoughts', 'Discovery Torch', 'Disfiguring Touch', 'Disfiguring Touch', 'Disguise Other', 'Distracting Cacophony', 'Distressing Tone', 'Divine Arrow', 'Dread Bolt', 'Dust of Twilight', 'Eagle Eye', "Eagle's Splendor", 'Early Judgment', 'Effortless Armor', 'Eldritch Conduit', 'Elemental Speech', 'Elemental Touch', 'Endure Elements', "Enemy's Heart", 'Enter Image', 'Enthrall', 'Evolution Surge, Leser', 'Fairness', 'False Life', 'Feast of Ashes', 'Fester', 'Fiery Shuriken', 'Find Traps', 'Fire Breath', 'Fire of Entanglement', 'Fire Sneeze', 'Fire Trap', 'Flame Blade', 'Flames of the Faithful', 'Flaming Sphere', 'Fleshcurdle', 'Fog Cloud', 'Follow Aura', 'Forest Friend', "Fox's Cunning", 'Frigid Touch', 'Frost Fall', 'Gallant Inspiration', 'Gentle Repose', 'Ghostbane Dirge', 'Ghostly Disguise', 'Ghoul touch', 'Glide', 'Glitterdust', 'Grace', 'Greensight', 'Guiding Star', 'Gust of Wind', 'Haste', 'Haunting Mists', 'Heat Metal', 'Heroism', 'Hidden Speech', 'Hide Campsite', 'Hideous Laughter', 'Hold Animal', 'Hold Person', 'Holy Shield', 'Honeyed Tongue', 'Howling Agony', "Hunter's Eye", "Hunter's Lore", 'Hypnotic Pattern', 'Imbue with Aura', 'Inflict Moderate Wounds', 'Instant Armor', 'Instrument of Agony', 'Invisibility', 'Kinetic Reverberation', 'Knock', 'Levitate', 'Light Lance', 'Light of Iomedae', 'Limp Lash', 'Lipstitch', 'Litany of Defense', 'Litany of Eloquence', 'Litany of Entanglement', 'Litany of Righteousness', 'Litany of Warding', 'Locate Object', 'Locate Weakness', 'Lockjaw', 'Mad Hallucination', 'Magic Mouth', 'Magic Siege Engine', 'Make Whole', 'Mark of Blood', "Martyr's Bargain", 'Mask Dweomer, Communal', 'Masterwork Transformation', 'Minor Image', 'Mirror Image', 'Misdirection', 'Miserable Pity', 'Mount, Communal', 'Natural Rhythm', 'Obscure Object', 'Oppressive Boredom', "Oracle's Burden", "Owl's Wisdom", "Paladin's Sacrifice", 'Perceive Cues', 'Pernicious Poison', 'Phantom Steed', 'Phantom Trap', 'Piercing Shriek', 'Pilfering Hand', 'Pox Pustules', 'Protection from Arrows', 'Protection from Chaos, Communal', 'Protection from Energy', 'Protection from Evil, Communal', 'Protection from Good, Communal', 'Protection from Law, Communal', 'Protective Penumbra', 'Protective Spirit', "Pugwampi's Grace", 'Pyrotechnics', 'Qualm', 'Rage', 'Reckless Infatuation', 'Recoil Fire', 'Reduce Animal', 'Reinforce Armaments, Communal', 'Reloading Hands', 'Remove Paralysis', 'Resist Energy', 'Restoration, Lesser', 'Restore Eidolon, Lesser', 'Retrieve Item', 'Returning Weapon', 'Returning Weapon, Communal', 'Ricochet Shot', 'Righteous Vigor', 'Rope Trick', 'Sacred Bond', 'Saddle Surge', 'Scare', 'Scent Trail', 'Scorching Ray', 'Sculpt Simulacrum', "Seducer's Eyes", 'See Invisibility', 'Shadow Bomb Admixture', 'Shard of Chaos', 'Share Language', 'Share Language, Communal', 'Share Memory', 'Shatter', 'Shield Other', 'Silence', 'Silk To Steel', 'Skinsend', 'Slipstream', 'Slow', 'Snapdragon Fireworks', 'Snare', 'Snow Shape', 'Soften Earth and Stone', 'Sound Burst', 'Speak with Plants', 'Spear of Purity', 'Spectral Hand', 'Spell Gauge', 'Spider Climb', 'Spike Growth', 'Spiritual Weapon', 'Spontaneous Immolation', 'Spontaneous Immolation', 'Stabilize Powder', 'Staggering Fall', 'Stalwart Resolve', 'Status', 'Steal Voice', 'Stone Call', 'Suggestion', 'Summon Eidolon', 'Summon Monster II', "Summon Nature's Ally II", 'Summon Swarm', 'Suppress Charms and Compulsions', 'Surmount Affliction', 'Symbol of Mirroring', 'Tactical Acumen', 'Tar Ball', 'Tattoo Potion', 'Telekinetic Assembly', 'Thunder Fire', 'Tongues', 'Touch Injection', 'Touch of Idiocy', 'Toxic Gift', 'Trail of the Rose', 'Transmute Potion to Poison', 'Tree Shape', 'Twisted Innards', 'Twisted Space', 'Unadulterated Loathing', 'Undetectable Alignment', 'Unnatural Lust', 'Unshakable Chill', 'Versatile Weapon', 'Vestment of the Champion', 'Vomit Swarm', 'Wake of Light', 'Warding Weapon', 'Warp Wood', 'Wartrain Mount', 'Waters of Lamashtu', 'Weapon of Awe', 'Web', 'Web Shelter', 'Whispering Wind', 'Wilderness Soldiers', 'Wind Wall', 'Wood Shape', 'Zone of Truth']
Level3Spells = ['Animate Dead', 'Arcane Sight', 'Beast Shape I', 'Bestow Curse', 'Black Tentacles', 'Blindness-Deafness', 'Blink', 'Call Lightning', 'Charm Monster', 'Clairaudience/Clairvoyance', 'Command Plants', 'Confusion', 'Contagion', 'Continual Flame', 'Create Food and Water', 'Crushing Despair', 'Cure Moderate Wounds', 'Cure Serious Wounds', 'Darkvision', 'Daylight', 'Deeper Darkness', 'Deep Slumber', 'Dimensional Anchor', 'Dimension Door', 'Diminish Plants', 'Discern Lies', 'Dispel Magic', 'Displacement', 'Dominate Animal', 'Enlarge Person, Mass', 'Explosive Runes', 'Fire Shield', 'Fireball', 'Flame Arrow', 'Fly', 'Gaseous Form', 'Geas, Lesser', 'Gentle Repose', 'Glibness', 'Glyph of Warding', 'Good Hope', 'Halt Undead', 'Haste', 'Heal Mount', 'Helping Hand', 'Heroism', 'Hold Person', 'Illusory Script', 'Inflict Moderate Wounds', 'Inflict Serious Wounds', 'Invisibility, Greater', 'Invisibility Purge', 'Invisibility Sphere', 'Keen Edge', 'Lightning Bolt', 'Locate Object', 'Locate Creature', 'Magic Circle against Evil', 'Magic Circle against Chaos', 'Magic Circle against Good', 'Magic Circle against Law', 'Magic Fang, Greater', 'Magic Vestment', 'Magic Weapon, Greater', 'Minor Creation', 'Major Image', 'Meld into Stone', 'Neutralize Poison', 'Nondetection', 'Obscure Object', 'Phantom Steed', 'Plant Growth', 'Poison', 'Prayer', 'Quench', 'Rage', 'Ray of Exhaustion', 'Reduce Animal', 'Reduce Person, Mass', 'Remove Blindness/Deafness', 'Remove Curse', 'Remove Disease', 'Repel Vermin', 'Scrying', 'Sculpt Sound', 'Searing Light', 'Secret Page', 'See Invisibility', 'Sepia Snake Sigil', 'Shrink Item', 'Sleet Storm', 'Slow', 'Snare', 'Speak with Animals', 'Speak with Dead', 'Speak with Plants', 'Spike Growth', 'Stinking Cloud', 'Stone Shape', 'Stoneskin', 'Suggestion', 'Summon Monster III', 'Summon Monster IV', "Summon Nature's Ally III", 'Tiny Hut', 'Tongues', 'Tree Shape', 'Vampiric touch', 'Wall of Fire', 'Wall of Ice', 'Water Breathing', 'Water Walk', 'Wind Wall', 'Agonize', 'Vision of Hell', 'Aura of the Unremarkable', 'Dweomer Retaliation', 'Twine Double', 'Fear', 'Summon Ancestral Guardian', 'See Through Stone', 'Rune of Durability', 'Rune of Warding', 'Protection from Energy', 'Spherescry', 'Illusory Poison', 'Arcane Reinforcement', 'Ape Walk', 'Heatstroke', 'Blood Rage', 'Absorbing Touch', 'Amplify Elixir', 'Aqueous Orb', 'Arcane Concordance', 'Aspect of the Stag', 'Banish Seeming', 'Blood Biography', 'Bloodhound', 'Bloody Claws', 'Borrow Fortune', 'Campfire Wall', 'Cast Out', 'Cloak of Winds', 'Coordinated Effort', 'Create Treasure Map', 'Cup of Dust', 'Defile Armor', 'Devolution', 'Divine Transfer', 'Draconic Reservoir', 'Elemental Aura', 'Elemental Speech', 'Enter Image', 'Evolution Surge', 'Feather Step, Mass', 'Fester', 'Fire of Judgment', 'Ghostbane Dirge, Mass', 'Guiding Star', 'Hidden Speech', 'Hide Campsite', 'Holy Whisper', 'Hydraulic Torrent', 'Instant Enemy', 'Invigorate, Mass', "Jester's Jaunt", 'Life Bubble', 'Lily Pad Stride', 'Marks Of Forbiddance', 'Nap Stack', "Nature's Exile", 'Pain Strike', 'Purging Finale', 'Rejuvenate Eidolon', 'Retribution', 'Reviving Finale', 'Righteous Vigor', 'Sacred Bond', 'Sanctify Armor', 'Screech', 'Seek Thoughts', 'Share Senses', 'Shifting Sand', 'Spiked Pit', 'Strong Jaw', 'Thorn Body', 'Thundering Drums', 'Tireless Pursuers', 'Twilight Knife', 'Venomous Bolt', 'Versatile Weapon', 'Ward the Faithful', 'Wrathful Mantle', "Hunter's Eye", 'Vermin Shape I', 'Fractions of Heal and Harm', 'Harrowing', "Lover's Vengeance", 'Vermin Shape I', 'Waters of Lamashtu', 'Age Resistance, Lesser', 'Animate Dead, Lesser', 'Anthropomorphic Animal', "Archon's Aura", 'Ash Storm', "Badger's Ferocity", 'Blade of Bright Victory', 'Blade of Dark Triumph', 'Blessing of the Mole', 'Burrow', 'Burst of Nettles', 'Cackling Skull', 'Control Summoned Creature', 'Countless Eyes', 'Curse of Disgust', 'Distracting Cacophony', 'Eldritch Fever', 'Eruptive Pustules', 'Excruciating Deformation', 'Exquisite Accompaniment', 'Fickle Winds', 'Force Hook Charge', 'Force Punch', 'Fungal Infestation', 'Haunting Choir', 'Howling Agony', 'Ki Leech', 'Loathsome Veil', 'Mad Monkeys', 'Malicious Spite', 'Marionette Possession', 'Monstrous Physique I', 'Overwhelming Grief', 'Rain of Frogs', 'Reckless Infatuation', 'Restore Eidolon', 'Sands of Time', 'Smug Narcissism', 'Spit Venom', 'Strangling Hair', 'Symbol of Healing', 'Terrible Remorse', 'Toxic Gift', 'Unadulterated Loathing', 'Undead Anatomy I', 'Utter Contempt', 'Vermin Shape I', 'Vision of Hell', 'Witness', 'Sheet Lightning', 'Dazzling Blade, Mass', 'Ablative Sphere', 'Summon Totem Creature', 'Battering Blast', 'Sky Swim', 'Bite the Hand', 'Gilded Whispers', 'Sequester Thoughts', 'Sharesister', 'Stolen Light', 'Twisted Innards', 'Blot', 'Blast Barrier', 'Ice Spears', 'Light of Iomedae', 'Martial Marionette', "Orchid's Drop", "Pugwampi's Grace", 'Shining Cord', 'Vengeful Comets', 'Vex Giant', 'Ablative Barrier', 'Absorb Toxicity', 'Animal Aspect, Greater', 'Burst of Speed', 'Chain of Perdition', 'Companion Mind Link', 'Darkvision, Communal', 'Daybreak Arrow', 'Deadly Juggernaut', 'Delay Poison, Communal', 'Discovery Torch', 'Endure Elements', 'Flash Fire', 'Healing Thief', 'Hostile Levitation', 'Life Conduit, Improved', 'Lightning Lash Bomb Admixture', 'Litany of Eloquence', 'Litany of Entanglement', 'Litany of Escape', 'Litany of Righteousness', 'Litany of Sight', 'Litany of Warding', 'Locate Weakness', 'Named Bullet', 'Obsidian Flow', 'Pellet Blast', 'Phantom Chariot', 'Phantom Driver', 'Phantom Steed, Communal', 'Protection from Arrows, Communal', 'Protection from Energy, Communal', 'Pup Shape', 'Resinous Skin', 'Resist Energy, Communal', 'Returning Weapon, Communal', 'Share Language, Communal', 'Spider Climb, Communal', 'Tongues, Communal', 'Touch Injection']
Level4Spells = ['Air Walk', 'Animal Growth', 'Animate Dead', 'Antiplant Shell', 'Arcane Eye', "Bear's Endurance, Mass", 'Beast Shape II', 'Bestow Curse', 'Black Tentacles', 'Blight', 'Break Enchantment', "Bull's Strength, Mass", "Cat's Grace, Mass", 'Chaos Hammer', 'Charm Monster', 'Command Plants', 'Commune with Nature', 'Confusion', 'Contact Other Plane', 'Contagion', 'Control Water', 'Crushing Despair', 'Cure Critical Wounds', 'Cure Serious Wounds', 'Death Ward', 'Detect Scrying', 'Dimensional Anchor', 'Dimension Door', 'Discern Lies', 'Dismissal', 'Dispel Chaos', 'Dispel Evil', 'Dispel Good', 'Dispel Law', 'Dispel Magic', 'Divination', 'Divine Power', 'Dominate Person', "Eagle's Splendor, Mass", 'Elemental Body I', 'Enervation', 'Enlarge Person, Mass', 'Fire Shield', 'Fire Trap', 'Flame Strike', "Fox's Cunning, Mass", 'Freedom of Movement', 'Geas, Lesser', 'Giant Vermin', 'Globe of Invulnerability, Lesser', 'Hallucinatory Terrain', 'Hold Monster', 'Holy Smite', 'Holy Sword', 'Ice Storm', 'Illusory Wall', 'Imbue with Spell Ability', 'Inflict Critical Wounds', 'Inflict Serious Wounds', 'Invisibility, Greater', 'Legend Lore', 'Locate Creature', "Mage's Faithful Hound", 'Magic Jar', 'Magic Weapon, Greater', 'Minor Creation', 'Major Creation', 'Mark of Justice', 'Mnemonic Enhancer', 'Modify Memory', 'Neutralize Poison', 'Nondetection', "Order's Wrath", 'Overland Flight', "Owl's Wisdom, Mass", 'Phantasmal Killer', 'Planar Ally, Lesser', 'Planar Binding, Lesser', 'Poison', 'Rainbow Pattern', 'Reduce Person, Mass', 'Reincarnate', 'Remove Curse', 'Repel Vermin', 'Resilient Sphere', 'Restoration', 'Rusting Grasp', 'Scrying', 'Secure Shelter', 'Sending', 'Shadow Conjuration', 'Shout', 'Slay Living', 'Solid Fog', 'Speak with Plants', 'Spell Immunity', 'Spike Stones', 'Stone Shape', 'Stoneskin', 'Summon Monster IV', 'Summon Monster V', "Summon Nature's Ally IV", 'Teleport', 'Tongues', 'Tree Stride', 'Unholy Blight', 'Wall of Fire', 'Wall of Ice', 'Zone of Silence', 'Wall of Stone', 'Agonize', 'Malediction', 'Sacrifice', 'Aura of the Unremarkable', 'Emergency Force Sphere', 'Fear', 'Insect Plague', 'Baleful Polymorph', 'Infernal Healing, Greater', 'Ancestral Gift', 'See Through Stone', 'Summon Flight of Eagles', 'Ghost Wolf', 'Acid Pit', 'Aspect of the Stag', 'Aspect of the Wolf', 'Ball Lightning', 'Blaze of Glory', 'Blessing of Fervor', 'Blessing of the Salamander', 'Bloody Claws', 'Bow Spirit', 'Brand, Greater', 'Calcific Touch', "Coward's Lament", 'Defile Armor', 'Denounce', 'Detonate', 'Discordant Blast', "Dragon's Breath", 'Evolution Surge, Greater', 'Fire of Vengeance', 'Firefall', 'Fluid Form', 'Forced Repentance', 'Geyser', 'Ghostbane Dirge, Mass', 'Grove of Respite', 'Heroic Finale', "King's Castle", 'Life Bubble', 'Moonstruck', 'Oath of Peace', 'Planar Adaptation', 'Purified Calling', 'Rebuke', 'Resounding Blow', 'Rest Eternal', 'River of Wind', 'Sacrificial Oath', 'Sanctify Armor', 'Shadow Projection', 'Share Senses', 'Shared Wrath', 'Sleepwalk', 'Spiritual Ally', 'Spite', 'Stay the Hand', 'Strong Jaw', 'Thorn Body', 'Threefold Aspect', 'Tireless Pursuers', 'Transmogrify', 'Treasure Stitching', 'True Form', 'Universal Formula', 'Wandering Star Motes', 'Vermin Shape I', 'Vermin Shape II', 'Ancestral Memory', 'Infernal Healing, Greater', 'Shield of the Dawnflower', 'Vermin Shape I', 'Vermin Shape II', 'Age Resistance, Lesser', 'Age Resistance', 'Arboreal Hammer', 'Arcana Theft', 'Atavism', 'Aura of Doom', 'Battlemind Link', 'Bestow Grace of the Champion', 'Blood Crow Strike', 'Cape of Wasps', 'Control Summoned Creature', 'Curse of Magic Negation', 'Dance of a Hundred Cuts', 'Darkvision, Greater', 'Daze, Mass', 'Echolocation', 'Envious Urge', 'False Life, Greater', 'Familiar Melding', 'Fleshworm Infestation', 'Interrogation, Greater', 'Leashed Shackles', 'Malfunction', 'Malicious Spite', 'Monstrous Physique II', "Oracle's Vessel", 'Overwhelming Grief', 'Plague Carrier', 'Primal Scream', 'Raise Animal Companion', 'Reprobation', 'Ride The Waves', 'Serenity', 'Shadow Step', 'Simulacrum, Lesser', 'Sonic Thrust', 'Soothe Construct', 'Spit Venom', 'Symbol of Healing', 'Symbol of Revelation', 'Symbol of Slowing', 'Terrible Remorse', 'Touch of Slime', 'Unholy Sword', 'Utter Contempt', 'Vermin Shape I', 'Vermin Shape II', 'Virtuoso Performance', 'Vitriolic Mist', 'Volcanic Storm', 'Wall of Sound', 'Summon Accuser', 'Undeath Ward', "Aram Zey's Trap Ward", 'Bite the Hand', 'Gilded Whispers', 'Blast Barrier', "Crusader's Edge", 'Eaglesoul', 'Forceful Strike', "Geb's Hammer", 'Kiss of the First World', 'Shadow Barbs', 'Song of Kyonin', 'Suppress Primal Magic', 'Zone of Foul Flames', 'Absorb Toxicity', 'Air Walk, Communal', 'Animal Aspect, Greater', 'Darkvision, Communal', 'Debilitating Portent', 'Find Quarry', 'Hostile Juxtaposition', 'Judgment Light', 'Litany of Escape', 'Litany of Madness', 'Litany of Sight', 'Litany of Thunder', 'Litany of Vengeance', 'Magic Siege Engine, Greater', 'Mutagenic Touch', 'Named Bullet', 'Named Bullet, Greater', 'Nondetection, Communal', 'Obsidian Flow', 'Pellet Blast', 'Phantom Chariot', 'Phantom Steed, Communal', 'Protection from Energy, Communal', 'Shocking Image', 'Stoneskin, Communal', 'Summoner Conduit', 'Telekinetic Charge', 'Terrain Bond', 'Tongues, Communal', 'Viper Bomb Admixture', 'Water Walk, Communal', 'Wreath of Blades']
Level5Spells = ['Animal Growth', 'Atonement', 'Awaken', 'Banishment', 'Beast Shape III', 'Blight', 'Break Enchantment', 'Breath of Life', 'Call Lightning Storm', 'Cloudkill', 'Command, Greater', 'Commune', 'Commune with Nature', 'Cone of Cold', 'Contact Other Plane', 'Control Winds', 'Creeping Doom', 'Cure Critical Wounds', 'Cure Light Wounds, Mass', 'Death Ward', 'Dismissal', 'Dispel Chaos', 'Dispel Evil', 'Dispel Good', 'Dispel Law', 'Dispel Magic, Greater', 'Disrupting Weapon', 'Dominate Person', 'Dream', 'Elemental Body II', 'Fabricate', 'False Vision', 'Feeblemind', 'Flame Strike', 'Geas/Quest', 'Hallow', 'Heroism, Greater', 'Hold Monster', 'Inflict Critical Wounds', 'Inflict Light Wounds, Mass', 'Interposing Hand', 'Invisibility, Mass', "Mage's Faithful Hound", "Mage's Private Sanctum", 'Magic Jar', 'Major Creation', 'Mark of Justice', 'Mind Fog', 'Mirage Arcana', 'Mislead', 'Nightmare', 'Overland Flight', 'Passwall', 'Permanency', 'Persistent Image', 'Planar Binding, Lesser', 'Planar Binding', 'Plane Shift', 'Plant Shape I', 'Polymorph', 'Raise Dead', 'Reincarnate', 'Repulsion', 'Righteous Might', 'Scrying', 'Secret Chest', 'Seeming', 'Sending', 'Sequester', 'Shadow Evocation', 'Shadow Walk', 'Simulacrum', 'Slay Living', 'Song of Discord', 'Spell Resistance', 'Spell Turning', 'Stoneskin', 'Suggestion, Mass', 'Summon Monster V', 'Summon Monster VII', "Summon Nature's Ally V", 'Symbol of Pain', 'Symbol of Sleep', 'Telekinesis', 'Telepathic Bond', 'Teleport', 'Teleport, Greater', 'Transmute Mud to Rock', 'Transmute Rock to Mud', 'Tree Stride', 'True Seeing', 'Unhallow', 'Wall of Fire', 'Wall of Force', 'Wall of Iron', 'Wall of Thorns', 'Waves of Fatigue', 'Wall of Stone', 'Insect Plague', 'Baleful Polymorph', 'Prying Eyes', 'Spellcasting Contract, Lesser', 'Aspect of the Wolf', 'Banish Seeming', "Bard's Escape", 'Blessing of the Salamander', 'Cacophonous Call, Mass', 'Castigate, Mass', 'Cleanse', 'Cloak of Dreams', 'Deafening Song Bolt', 'Delayed Consumption', 'Elude Time', 'Fire Snake', 'Foe to Friend', 'Frozen Note', 'Geyser', 'Ghostbane Dirge, Mass', 'Hungry Pit', 'Life Bubble', 'Pain Strike, Mass', 'Phantasmal Web', 'Pillar of Life', 'Planar Adaptation', 'Rejuvenate Eidolon, Greater', 'Resounding Blow', 'Rest Eternal', 'Resurgent Transformation', 'Snake Staff', 'Stunning Finale', 'Suffocation', 'Threefold Aspect', 'Treasure Stitching', 'Unwilling Shield', 'Vermin Shape II', 'Constricting Coils', 'Ancestral Memory', 'Covetous Aura', 'Vermin Shape II', 'Smite Abomination', 'Acidic Spray', 'Age Resistance, Greater', 'Astral Projection, Lesser', 'Conjure Black Pudding', 'Contagion, Greater', 'Corrosive Consumption', 'Create Demiplane, Lesser', 'Curse, Major', 'Curse of Disgust', 'Curse of Magic Negation', 'Divine Pursuit', 'Echolocation', 'Fickle Winds', 'Forbid Action, Greater', 'Holy Ice', 'Ice Crystal Teleport', 'Icy Prison', 'Joyful Rapture', 'Ki Shout', 'Lend Judgment, Greater', 'Lightning Arc', 'Monstrous Physique III', 'Plague Carrier', 'Possess Object', 'Raise Animal Companion', 'Rapid Repair', 'Reprobation', 'Resonating Word', 'Serenity', 'Shadowbard', 'Smug Narcissism', 'Sonic Thrust', 'Soothe Construct', 'Symbol of Scrying', 'Unbreakable Construct', 'Undead Anatomy II', 'Unholy Ice', 'Vengeful Outrage', 'Vermin Shape II', 'Wall of Sound', 'Summon Infernal Host', 'Undeath Ward', 'Lighten Object, Mass', 'Sequester Thoughts', 'Bladed Dash, Greater', 'Eaglesoul', 'Geniekind', 'Impart Mind', "Khain's Army", 'Music of the Spheres', 'Siphon Magic', 'Spell Absorption', 'Absorb Toxicity', 'Air Walk, Communal', 'Dust Form', 'Energy Siege Shot', 'Hostile Juxtaposition', 'Languid Bomb Admixture', 'Life Conduit, Greater', 'Litany of Thunder', 'Litany of Vengeance', 'Magic Siege Engine, Greater', 'Spell Immunity, Communal', 'Stoneskin, Communal', 'Summoner Conduit', 'Symbol of Striking', 'Tar Pool', 'Tongues, Communal', 'Wreath of Blades']
Level6Spells = ['Acid Fog', 'Analyze Dweomer', 'Animate Objects', 'Antilife Shell', 'Antimagic Field', 'Antipathy', 'Banishment', "Bear's Endurance, Mass", 'Beast Shape IV', 'Binding', 'Blade Barrier', 'Blasphemy', "Bull's Strength, Mass", "Cat's Grace, Mass", 'Chain Lightning', 'Charm Monster, Mass', 'Circle of Death', 'Cone of Cold', 'Contingency', 'Control Water', 'Create Undead', 'Cure Light Wounds, Mass', 'Cure Moderate Wounds, Mass', 'Dictum', 'Dimensional Lock', 'Discern Location', 'Disintegrate', 'Dispel Magic, Greater', 'Dominate Monster', "Eagle's Splendor, Mass", 'Elemental Body III', 'Eyebite', 'Find the Path', 'Fire Seeds', 'Flesh to Stone', 'Forbiddance', 'Forceful Hand', 'Form of the Dragon I', "Fox's Cunning, Mass", 'Freezing Sphere', 'Geas/Quest', 'Giant Form I', 'Globe of Invulnerability', 'Glyph of Warding, Greater', 'Guards and Wards', 'Harm', 'Heal', "Heroes' Feast", 'Heroism, Greater', 'Holy Word', 'Incendiary Cloud', 'Inflict Light Wounds, Mass', 'Inflict Moderate Wounds, Mass', 'Ironwood', 'Irresistible Dance', 'Legend Lore', 'Liveoak', "Mage's Lucubration", 'Maze', 'Mislead', 'Move Earth', "Owl's Wisdom, Mass", 'Permanent Image', 'Planar Ally', 'Planar Binding', 'Planar Binding, Greater', 'Plant Shape II', 'Programmed Image', 'Project Image', 'Protection from Spells', 'Raise Dead', 'Repel Wood', 'Repulsion', 'Scrying, Greater', 'Shadow Walk', 'Shout, Greater', 'Slay Living', 'Spellstaff', 'Statue', 'Stone Tell', 'Stone to Flesh', 'Suggestion, Mass', 'Summon Monster VI', 'Summon Monster VIII', "Summon Nature's Ally VI", 'Symbol of Fear', 'Symbol of Persuasion', 'Sympathetic Vibration', 'Sympathy', 'Teleportation Circle', 'Transformation', 'Transport via Plants', 'True Seeing', 'Undeath to Death', 'Veil', 'Wall of Iron', 'Wind Walk', 'Word of Recall', 'Word of Chaos', 'Wall of Stone', 'Hellfire Ray', 'Dirge of the Victorious Knights', 'Summon Flight of Eagles', 'Genius Avaricious', 'Brilliant Inspiration', 'Cleanse', 'Cloak of Dreams', 'Contagious Flame', 'Deadly Finale', 'Enemy Hammer', 'Euphoric Tranquility', 'Fester, Mass', 'Fluid Form', "Fool's Forbiddance", 'Getaway', 'Pied Piping', 'Planar Adaptation< Mass', 'Sirocco', 'Swarm Skin', 'Twin Form', 'Unwilling Shield', 'Vision of Lamashtu', 'Age Resistance', 'Battlemind Link', 'Cold Ice Strike', 'Conjure Black Pudding', 'Contagion, Greater', 'Create Demiplane', 'Curse, Major', 'Dance of a Thousand Cuts', 'Eagle Aerie', 'Envious Urge', 'Epidemic', 'Ice Crystal Teleport', 'Joyful Rapture', 'Leashed Shackles', 'Monstrous Physique IV', 'Overwhelming Presence', 'Plague Storm', 'Serenity', 'Symbol of Sealing', 'Undead Anatomy III', 'Utter Contempt', 'Vengeful Outrage', 'Waves of Ecstasy', 'Undeath Ward', 'Bite the Hand, Mass', 'Eaglesoul', 'Eldritch Conduit, Greater', 'Impart Mind', 'Music of the Spheres', 'Caging Bomb Admixture', 'Dust Form', 'Energy Siege Shot, Greater', 'Hostile Juxtaposition, Greater', 'Litany of Madness', 'Named Bullet, Greater', 'Stoneskin, Communal', 'Tar Pool', 'Walk through Space']
Level7Spells = ['Animate Plants', 'Arcane Sight, Greater', 'Banishment', 'Blasphemy', 'Chain Lightning', 'Changestaff', 'Control Undead', 'Control Weather', 'Creeping Doom', 'Cure Moderate Wounds, Mass', 'Cure Serious Wounds, Mass', 'Delayed Blast Fireball', 'Destruction', 'Dictum', 'Elemental Body IV', 'Ethereal Jaunt', 'Finger of Death', 'Fire Storm', 'Forcecage', 'Form of the Dragon II', 'Giant Form I', 'Grasping Hand', 'Harm', 'Heal', 'Hold Person, Mass', 'Holy Word', 'Inflict Moderate Wounds, Mass', 'Inflict Serious Wounds, Mass', 'Insanity', 'Invisibility, Mass', 'Limited Wish', "Mage's Magnificent Mansion", "Mage's Sword", 'Phase Door', 'Plane Shift', 'Plant Shape III', 'Polymorph, Greater', 'Power Word Blind', 'Prismatic Spray', 'Project Image', 'Refuge', 'Regenerate', 'Repulsion', 'Restoration, Greater', 'Resurrection', 'Reverse Gravity', 'Scrying, Greater', 'Sequester', 'Shadow Conjuration, Greater', 'Simulacrum', 'Spell Turning', 'Statue', 'Summon Monster VII', "Summon Nature's Ally VII", 'Sunbeam', 'Symbol of Stunning', 'Symbol of Weakness', 'Teleport, Greater', 'Teleport Object', 'Transmute Metal to Wood', 'True Seeing', 'Vision', 'Waves of Exhaustion', 'Wind Walk', 'Word of Chaos', "Signifer's Rally", 'Instant Summons', 'Spellcasting Contract', 'Deflection', 'Expend', 'Firebrand', 'Fly, Mass', 'Phantasmal Revenge', 'Planar Adaptation< Mass', 'Rampart', 'Vortex', 'Teleport Trap', 'Vision of Lamashtu', 'Age Resistance, Greater', 'Bestow Grace of the Champion', 'Caustic Eruption', 'Circle of Clarity', 'Control Construct', 'Create Demiplane, Lesser', 'Epidemic', 'Ice Body', 'Joyful Rapture', 'Ki Shout', 'Lunar Veil', 'Plague Storm', 'Resonating Word', 'Scouring Winds', 'Temporary Resurrection', 'Waves of Ecstasy', 'Bite the Hand, Mass', 'Hungry Darkness', 'Arcane Cannon', 'Hostile Juxtaposition, Greater', 'Jolting Portent', 'Siege of Trees', 'Walk through Space']
Level8Spells = ['Animal Shapes', 'Antimagic Field', 'Antipathy', 'Binding', 'Charm Monster, Mass', 'Clenched Fist', 'Cloak of Chaos', 'Clone', 'Control Plants', 'Create Greater Undead', 'Cure Critical Wounds, Mass', 'Cure Serious Wounds, Mass', 'Demand', 'Destruction', 'Dimensional Lock', 'Discern Location', 'Earthquake', 'Finger of Death', 'Fire Storm', 'Form of the Dragon III', 'Giant Form II', 'Holy Aura', 'Horrid Wilting', 'Incendiary Cloud', 'Inflict Critical Wounds, Mass', 'Inflict Serious Wounds, Mass', 'Iron Body', 'Irresistible Dance', 'Maze', 'Mind Blank', 'Moment of Prescience', 'Planar Ally, Greater', 'Planar Binding, Greater', 'Polar Ray', 'Polymorph Any Object', 'Power Word Stun', 'Prismatic Wall', 'Prying Eyes, Greater', 'Protection from Spells', 'Repel Metal or Stone', 'Resurrection', 'Reverse Gravity', 'Scintillating Pattern', 'Screen', 'Shadow Evocation, Greater', 'Shield of Law', 'Shout, Greater', 'Spell Immunity, Greater', 'Summon Monster VIII', "Summon Nature's Ally VIII", 'Sunburst', 'Symbol of Death', 'Symbol of Insanity', 'Sympathy', 'Telekinetic Sphere', 'Temporal Stasis', 'Trap the Soul', 'Unholy Aura', 'Whirlwind', 'Word of Recall', 'Tomb Legion', 'Divine Vessel', 'Euphoric Tranquility', 'Seamantle', 'Stormbolts', 'Wall of Lava', 'Rift of Ruin', 'Atavism, Mass', 'Blood Mist', 'Call Construct', 'Create Demiplane', 'Orb of the Void', 'Prediction of Failure', 'Undead Anatomy IV', 'Spell Absorption, Greater', 'Spellscar', 'Frightful Aspect']
Level9Spells = ['Antipathy', 'Astral Projection', 'Crushing Hand', 'Cure Critical Wounds, Mass', 'Dominate Monster', 'Elemental Swarm', 'Energy Drain', 'Etherealness', 'Foresight', 'Freedom', 'Gate', 'Heal, Mass', 'Hold Monster, Mass', 'Implosion', 'Imprisonment', 'Inflict Critical Wounds, Mass', "Mage's Disjunction", 'Meteor Swarm', 'Miracle', 'Power Word Kill', 'Prismatic Sphere', 'Refuge', 'Regenerate', 'Shades', 'Shambler', 'Shapechange', 'Soul Bind', 'Storm of Vengeance', 'Summon Monster IX', "Summon Nature's Ally IX", 'Sympathy', 'Teleportation Circle', 'Time Stop', 'True Resurrection', 'Wail of the Banshee', 'Weird', 'Wish', 'Spellcasting Contract, Greater', 'Canopic Conversion', 'Summon Elemental Steed', 'Clashing Rocks', 'Fiery Body', 'Suffocation, Mass', 'Tsunami', 'Wall of Suppression', 'Winds of Vengeance', 'World Wave', 'Interplanetary Teleport', 'Create Demiplane, Greater', 'Cursed Earth', 'Icy Prison, Mass', 'Interplanetary Teleport', 'Overwhelming Presence', 'Polar Midnight', 'Ride the Lightning', 'Summon Elder Worm', 'Summon Froghemoth', 'Symbol of Strife', 'Symbol of Vulnerability', 'Transmute Blood To Acid', 'Wooden Phalanx', "Echean's Excellent Enclosure", "Aroden's Spellbane", 'Heroic Invocation', 'Mind Blank, Communal', 'Siege of Trees, Greater', 'Spell Immunity, Greater Communal']
SpellLists = [Level0Spells, Level1Spells, Level2Spells, Level3Spells, Level4Spells, Level5Spells, Level6Spells, Level7Spells, Level8Spells, Level9Spells]

def RollDice(n,d):
    return sum([random.randint(1,d) for i in xrange(n)])

def GetFromTable(table):
    '''Requires a dictionary where all keys are ints > 0'''
    keys = table.keys()
    r = random.randint(1,max(keys))
    return min(filter(lambda x: x >= r, keys))

def PickMinorItem():
    r = random.randint(1,100)
    if r <= 4:
        PickMinorArmorOrShield()
    elif r <= 9:
        PickMinorWeapon()
    elif r <= 44:
        PickMinorPotion()
    elif r <= 46:
        PickMinorRing()
    elif r <= 81:
        PickMinorScroll()
    elif r <= 91:
        PickMinorWand()
    elif r <= 100:
        PickMinorWondrousItem()

def PickMediumItem():
    r = random.randint(1,100)
    if r <= 10:
        PickMediumArmorOrShield()
    elif r <= 20:
        PickMediumWeapon()
    elif r <= 30:
        PickMediumPotion()
    elif r <= 40:
        PickMediumRing()
    elif r <= 50:
        PickMediumRod()
    elif r <= 65:
        PickMediumScroll()
    elif r <= 68:
        PickMediumStaff()
    elif r <= 83:
        PickMediumWand()
    elif r <= 100:
        PickMediumWondrousItem()

def PickMajorItem():
    r = random.randint(1,100)
    if r <= 10:
        PickMajorArmorOrShield()
    elif r <= 20:
        PickMajorWeapon()
    elif r <= 25:
        PickMajorPotion()
    elif r <= 35:
        PickMajorRing()
    elif r <= 45:
        PickMajorRod()
    elif r <= 55:
        PickMajorScroll()
    elif r <= 75:
        PickMajorStaff()
    elif r <= 80:
        PickMajorWand()
    elif r <= 100:
        PickMajorWondrousItem()

def PickMinorArmorOrShield():
    print "No code for armor or shields yet"

def PickMinorWeapon():
    print "No code for weapons yet"
    
def PickMediumArmorOrShield():
    print "No code for armor or shields yet"

def PickMediumWeapon():
    print "No code for weapons yet"
    
def PickMajorArmorOrShield():
    print "No code for armor or shields yet"

def PickMajorWeapon():
    print "No code for weapons yet"

def PickWeaponType():
    t = [['Gauntlet', 2, '1d3', '', 2, ['B']],
         ['Battle aspergillum', 5, '1d6', '', 2, ['B']],
         ['Brass knuckles', 1, '1d3', '', 2, ['B']],
         ['Cestus', 5, '1d4', '19-20', 2, ['B', 'P']],
         ['Dagger', 2, '1d4', '19-20', 2, ['P', 'S']],
         ['Dagger, punching', 2, '1d4', '', 3, ['P']],
         ['Gauntlet, spiked', 5, '1d4', '', 2, ['P']],
         ['Mace, light', 5, '1d6', '', 2, ['B']],
         ['Sickle', 6, '1d6', '', 2, ['S']],
         ['Wooden stake', 0, '1d4', '', 2, ['P']],
         ['Club', 0, '1d6', '', 2, ['B']],
         ['Club, mere', 2, '1d4', '', 2, ['B', 'P']],
         ['Combat scabbard', 1, '1d6', '', 2, ['B']],
         ['Mace, heavy', 12, '1d8', '', 2, ['B']],
         ['Morningstar', 8, '1d8', '', 2, ['B', 'P']],
         ['Shortspear', 1, '1d6', '', 2, ['P']],
         ['Bayonet', 5, '1d6', '', 2, ['P']],
         ['Longspear', 5, '1d8', '', 3, ['P']],
         ['Quarterstaff', 0, '1d6/1d6', '', 2, ['B']],
         ['Spear', 2, '1d8', '', 3, ['P']],
         ['Spear, boar', 5, '1d8', '', 2, ['P']],
         ['Axe, throwing', 8, '1d6', '', 2, ['S']],
         ['Blade boot', 25, '1d4', '', 2, ['P']],
         ['Dogslicer', 8, '1d6', '19-20', 2, ['S']],
         ['Hammer, light', 1, '1d4', '', 2, ['B']],
         ['Gladius', 15, '1d6', '19-20', 2, ['P', 'S']],
         ['Handaxe', 6, '1d6', '', 3, ['S']],
         ['Knife, switchblade', 5, '1d4', '19-20', 2, ['P']],
         ['Pick, light', 4, '1d4', '', 4, ['P']],
         ['Sap', 1, '1d6', '', 2, ['B']],
         ['Starknife', 24, '1d4', '', 3, ['P']],
         ['Sword, short', 10, '1d6', '19-20', 2, ['P']],
         ['War razor', 8, '1d4', '19-20', 2, ['S']],
         ['Battleaxe', 10, '1d8', '', 3, ['S']],
         ['Flail', 8, '1d8', '', 2, ['B']],
         ['Klar', 12, '1d6', '', 2, ['S']],
         ['Longsword', 15, '1d8', '19-20', 2, ['S']],
         ['Pick, heavy', 8, '1d6', '', 4, ['P']],
         ['Rapier', 20, '1d6', '18-20', 2, ['P']],
         ['Scabbard, combat (sharpened)', 10, '1d6', '18-20', 2, ['S']],
         ['Scimitar', 15, '1d6', '18-20', 2, ['S']],
         ['Scizore', 20, '1d10', '', 2, ['P']],
         ['Sword cane', 45, '1d6', '', 2, ['P']],
         ['Terbutje', 5, '1d8', '19-20', 2, ['S']],
         ['Terbutje, steel', 20, '1d8', '19-20', 2, ['S']],
         ['Trident', 15, '1d8', '', 2, ['P']],
         ['Warhammer', 12, '1d8', '', 3, ['B']],
         ['Bardiche', 13, '1d10', '19-20', 2, ['S']],
         ['Bec de corbin', 15, '1d10', '', 3, ['B', 'P']],
         ['Bill', 11, '1d8', '', 3, ['S']],
         ['Earth breaker', 40, '2d6', '', 3, ['B']],
         ['Falchion', 75, '2d4', '18-20', 2, ['S']],
         ['Flail, heavy', 15, '1d10', '19-20', 2, ['B']],
         ['Glaive', 8, '1d10', '', 3, ['S']],
         ['Glaive-guisarme', 12, '1d10', '', 3, ['S']],
         ['Greataxe', 20, '1d12', '', 3, ['S']],
         ['Greatclub', 5, '1d10', '', 2, ['B']],
         ['Greatsword', 50, '2d6', '19-20', 2, ['S']],
         ['Guisarme', 9, '2d4', '', 3, ['S']],
         ['Halberd', 10, '1d10', '', 3, ['P', 'S']],
         ['Hammer, lucerne', 15, '1d12', '', 2, ['B', 'P']],
         ['Horsechopper', 10, '1d10', '', 3, ['P', 'S']],
         ['Lance', 10, '1d8', '', 3, ['P']],
         ['Ogre hook', 24, '1d10', '', 3, ['P']],
         ['Pickaxe', 14, '1d8', '', 4, ['P']],
         ['Ranseur', 10, '2d4', '', 3, ['P']],
         ['Scythe', 18, '2d4', '', 4, ['P', 'S']],
         ['Spear, syringe', 100, '1d8', '', 3, ['P']]
        ]
    return random.choice(t)

def PickSpecialMaterial(item_type="light armor", item_mat=""):
    # types: light armor, medium armor, heavy armor, shield, clothing, weapon, ammunition
    # materials: metal, hide, cloth, wood
    for i in xrange(1000):
        r = random.randint(1,27)
        if (r == 1 and
            item_type in ['light armor', 'medium armor', 'heavy armor', 'weapon', 'ammunition'] and item_mat == "metal"):
            t = {'light armor': 5000,
                 'medium armor': 10000,
                 'heavy armor': 15000,
                 'weapon': 3000,
                 'ammunition': 60}
            return "Adamantine", t[item_type], "http://www.d20pfsrd.com/equipment---final/special-materials#TOC-Adamantine"
        elif (r == 2 and
              item_type in ['light armor', 'medium armor'] and not item_mat == "hide"):
            t = {'light armor': 1000,
                 'medium armor': 2000}
            return "Angelskin", t[item_type], "http://www.d20pfsrd.com/equipment---final/special-materials#TOC-Angelskin"
        elif (r == 3 and
              item_type in ['weapon', 'ammunition'] and item_mat == "metal"):
            t = {'weapon': 1500,
                 'ammunition': 30}
            return "Blood Crystal", t[item_type]
        elif (r == 4 and
              item_type in ['light armor', 'medium armor', 'heavy armor', 'shield', 'weapon', 'ammunition'] and
              not item_mat == "hide" and not item_mat == "cloth"):
            return "Bone", 0
        elif (r == 5 and
              item_type in ['light armor', 'medium armor', 'weapon', 'ammunition'] and item_mat == "metal"):
            return "Bronze", 0
        elif (r == 6 and
              item_type in ['weapon', 'ammunition'] and item_mat == "metal"):
            return "Cold Iron", "2x"
        elif (r == 7 and
              item_type in ['clothing', 'light armor', 'medium armor'] and item_mat == "hide"):
            t = {'clothing': 500,
                 'light armor': 750,
                 'medium armor': 1500}
            return "Darkleaf", t[item_type]
        elif (r == 8 and
              item_type in ['light armor', 'medium armor', 'heavy armor', 'shield', 'weapon', 'ammunition'] and item_mat == "metal"):
            return "Darkwood", "10gp/lb"
        elif (r == 9 and
              item_type in ['light armor', 'medium armor', 'heavy armor', 'shield'] and item_mat == "hide"):
            return "Dragonhide", "2x"
        elif (r == 10 and
              item_type in ['light armor', 'medium armor', 'heavy armor', 'weapon', 'ammunition'] and item_mat == "hide"):
            t = {'light armor': 1200,
                 'medium armor': 1800}
            return "Eel hide", t[item_type]
        elif (r == 11 and
              item_type in ['light armor', 'medium armor', 'heavy armor', 'weapon', 'ammunition'] and item_mat == "metal"):
            t = {'light armor': 1000,
                 'medium armor': 2000,
                 'heavy armor': 3000,
                 'weapon': 1000,
                 'ammunition': 20}
            return "Elysian Bronze", t[item_type]
        elif (r == 12 and
              item_type in ['light armor', 'medium armor', 'heavy armor', 'weapon', 'ammunition'] and item_mat == "metal"):
            t = {'light armor': 1000,
                 'medium armor': 2500,
                 'heavy armor': 3000,
                 'weapon': 600,
                 'ammunition': 15}
            return "Fire-forged steel", t[item_type]
        elif (r == 13 and
              item_type in ['light armor', 'medium armor', 'heavy armor', 'weapon', 'ammunition'] and item_mat == "metal"):
            t = {'light armor': 1000,
                 'medium armor': 2500,
                 'heavy armor': 3000,
                 'weapon': 600,
                 'ammunition': 15}
            return "Frost-forged steel", t[item_type]
        elif (r == 14 and
              item_type in ['light armor', 'medium armor', 'heavy armor', 'weapon', 'ammunition'] and item_mat == "metal"):
            r = random.randint(1,5)
            if r < 5:
                return "Gold-plated", "3x"
            elif r == 5 and item_type in ['light armor', 'medium armor', 'weapon', 'ammunition']:
                return "Solid-gold", "10x"
        elif (r == 15 and
              item_type in ['light armor', 'medium armor', 'heavy armor', 'shield', 'weapon', 'ammunition'] and item_mat == "wood"):
            return "Greenwood", "50gp/lb"
        elif (r == 16 and
              item_type in ['light armor'] and item_mat == "cloth"):
            t = {'light armor': 200}
            return "Griffon Mane", t[item_type]
        elif (r == 17 and
              item_type in ['light armor', 'medium armor', 'heavy armor', 'shield', 'weapon', 'ammunition'] and item_mat == "metal"):
            t = {'light armor': 500,
                 'medium armor': 1000,
                 'heavy armor': 1500,
                 'shield': 100,
                 'weapon': 500,
                 'ammunition': 10}
            return "Living steel", t[item_type]
        elif (r == 18 and
              item_type in ['light armor', 'medium armor', 'heavy armor', 'shield', 'weapon', 'ammunition'] and item_mat == "metal"):
            t = {'light armor': 1000,
                 'medium armor': 4000,
                 'heavy armor': 9000,
                 'shield': 1000,
                 'weapon': "500gp/lb",
                 'ammunition': "500gp/lb"}
            return "Mithral", t[item_type]
        elif (r == 19 and
              item_type in ['weapon', 'ammunition'] and item_mat == "metal"):
            return "Nexavaran steel", "1.5x"
        elif (r == 20 and
              item_type in ['weapon'] and item_mat == "metal"):
            return "Obsidian", "0.5x"
        elif (r == 21 and
              item_type in ['weapon', 'ammunition'] and item_mat == "metal"):
            t = {'weapon': "See text",
                 'ammunition': 2}
            return "Alchemical Silver", t[item_type]
        elif (r == 22 and
              item_type in ['weapon'] and item_mat == "metal"):
            return "Silversheen", 750
        elif (r == 23 and
              item_type in ['weapon', 'ammunition'] and item_mat == "metal"):
            t = {'weapon': 200,
                 'ammunition': 20}
            return "Viridum", t[item_type]
        elif (r == 24 and
              item_type in ['weapon'] and item_mat == "wood"):
            return "Whipwood", 500
        elif (r == 25 and
              item_type in ['weapon'] and item_mat == "wood"):
            return "Wyroot (1 life point)", 1000
        elif (r == 26 and
              item_type in ['weapon'] and item_mat == "wood"):
            return "Wyroot (2 life points)", 2000
        elif (r == 27 and
              item_type in ['weapon'] and item_mat == "wood"):
            return "Wyroot (3 life points)", 4000
    print "!!! No special materials available for this type of item !!!"
    return "","",""
    
            

def PickMinorPotion():
    t = {10:["Cure light wounds", "", 50, "Potion"],
         13:["Endure elements", "", 50, "Potion"],
         15:["Hide from animals", "", 50, "Potion"],
         17:["Hide from undead", "", 50, "Potion"],
         19:["Jump", "", 50, "Potion"],
         22:["Mage armor", "", 50, "Potion"],
         25:["Magic fang", "", 50, "Potion"],
         26:["Magic stone", "", 50, "Oil"],
         29:["Magic weapon", "", 50, "Oil"],
         30:["Pass without trace", "", 50, "Potion"],
         32:["Protection from (alignment)", "Protection from evil", 50, "Potion"],
         34:["Remove fear", "", 50, "Potion"],
         35:["Sanctuary", "", 50, "Potion"],
         38:["Shield of faith +2", "Shield of faith", 50, "Potion"],
         39:["Shillelagh", "", 50, "Oil"],
         41:["Bless weapon", "", 100, "Oil"],
         44:["Enlarge person", "", 250, "Potion"],
         45:["Reduce person", "", 250, "Potion"],
         47:["Aid", "", 300, "Potion"],
         50:["Barkskin +2", "Barkskin", 300, "Potion"],
         53:["Bear's endurance", "", 300, "Potion"],
         56:["Blur", "", 300, "Potion"],
         59:["Bull's strength", "", 300, "Potion"],
         62:["Cat's grace", "", 300, "Potion"],
         67:["Cure moderate wounds", "", 300, "Potion"],
         68:["Darkness", "", 300, "Oil"],
         71:["Darkvision", "", 300, "Potion"],
         74:["Delay poison", "", 300, "Potion"],
         76:["Eagle's splendor", "", 300, "Potion"],
         78:["Fox's cunning", "", 300, "Potion"],
         80:["Invisibility", "", 300, "Potion"],
         81:["Invisibility", "", 300, "Oil"],
         84:["Lesser restoration", "", 300, "Potion"],
         85:["Levitate", "", 300, "Potion"],
         86:["Levitate", "", 300, "Oil"],
         87:["Misdirection", "", 300, "Potion"],
         89:["Owl's wisdom", "", 300, "Potion"],
         91:["Protection from arrows 10/magic", "Protection from arrows", 300, "Potion"],
         93:["Remove paralysis", "", 300, "Potion"],
         96:["Resist energy (type) 10", "Resist energy", 300, "Potion"],
         97:["Shield of faith +3", "Shield of faith", 300, "Potion"],
         99:["Spider climb", "", 300, "Potion"],
         100:["Undetectable alignment", "", 300, "Potion"]}
    PickPotion(t)

def PickMediumPotion():
    t = {2:["Bless weapon", "", 100, "Oil"],
         4:["Enlarge person", "", 250, "Potion"],
         5:["Reduce person", "", 250, "Potion"],
         6:["Aid", "", 300, "Potion"],
         7:["Barkskin +2", "Barkskin", 300, "Potion"],
         10:["Bear's endurance", "", 300, "Potion"],
         13:["Blur", "", 300, "Potion"],
         16:["Bull's strength", "", 300, "Potion"],
         19:["Cat's grace", "", 300, "Potion"],
         27:["Cure moderate wounds", "", 300, "Potion"],
         28:["Darkness", "", 300, "Oil"],
         30:["Darkvision", "", 300, "Potion"],
         31:["Delay poison", "", 300, "Potion"],
         33:["Eagle's splendor", "", 300, "Potion"],
         35:["Fox's cunning", "", 300, "Potion"],
         36:["Invisibility", "", 300, "Potion"],
         37:["Invisibility", "", 300, "Oil"],
         38:["Lesser restoration", "", 300, "Potion"],
         39:["Levitate", "", 300, "Oil"],
         40:["Misdirection", "", 300, "Potion"],
         42:["Owl's wisdom", "", 300, "Potion"],
         43:["Protection from arrows 10/magic", "Protection from arrows", 300, "Potion"],
         44:["Remove paralysis", "", 300, "Potion"],
         46:["Resist energy (type) 10", "Resist energy", 300, "Potion"],
         48:["Shield of faith +3", "Shield of faith", 300, "Potion"],
         49:["Spider climb", "", 300, "Potion"],
         50:["Undetectable alignment", "", 300, "Potion"],
         51:["Barkskin +3", "Barkskin", 600, "Potion"],
         52:["Shield of faith +4", "Shield of faith", 600, "Potion"],
         55:["Resist energy (type) 20", "Resist energy", 700, "Potion"],
         60:["Cure serious wounds", "", 750, "Potion"],
         61:["Daylight", "", 750, "Oil"],
         64:["Displacement", "", 750, "Potion"],
         65:["Flame arrow", "", 750, "Oil"],
         68:["Fly", "", 750, "Potion"],
         69:["Gaseous form", "", 750, "Potion"],
         71:["Greater magic fang +1", "Greater magic fang", 750, "Potion"],
         73:["Greater magic weapon +1", "Greater magic weapon", 750, "Oil"],
         75:["Haste", "", 750, "Potion"],
         78:["Heroism", "", 750, "Potion"],
         80:["Keen edge", "", 750, "Oil"],
         81:["Magic circle against (alignment)", "Magic circle against evil", 750, "Potion"],
         83:["Magic vestment +1", "Magic vestment", 750, "Oil"],
         86:["Neutralize poison", "", 750, "Potion"],
         88:["Nondetection", "", 750, "Potion"],
         91:["Protection from energy (type)", "Protection from energy", 750, "Potion"],
         93:["Rage", "", 750, "Potion"],
         94:["Remove Blindness/Deafness", "Remove Blindness Deafness", 750, "Potion"],
         95:["Remove curse", "", 750, "Potion"],
         96:["Remove disease", "", 750, "Potion"],
         97:["Tongues", "", 750, "Potion"],
         99:["Water breathing", "", 750, "Potion"],
         100:["Water walk", "", 750, "Potion"]}
    PickPotion(t)

def PickMajorPotion():
    t = {2:["Blur", "", 300, "Potion"],
         7:["Cure moderate wounds", "", 300, "Potion"],
         9:["Darkvision", "", 300, "Potion"],
         10:["Invisibility", "", 300, "Potion"],
         11:["Invisibility", "", 300, "Oil"],
         12:["Lesser restoration", "", 300, "Potion"],
         13:["Remove paralysis", "", 300, "Potion"],
         14:["Shield of faith +3", "Shield of faith", 300, "Potion"],
         15:["Undetectable alignment", "", 300, "Potion"],
         16:["Barkskin +3", "Barkskin", 600, "Potion"],
         18:["Shield of faith +4", "Shield of faith", 600, "Potion"],
         20:["Resist energy (type) 20", "Resist energy", 700, "Potion"],
         28:["Cure serious wounds", "", 750, "Potion"],
         29:["Daylight", "", 750, "Oil"],
         32:["Displacement", "", 750, "Potion"],
         33:["Flame arrow", "", 750, "Oil"],
         38:["Fly", "", 750, "Potion"],
         39:["Gaseous form", "", 750, "Potion"],
         41:["Haste", "", 750, "Potion"],
         44:["Heroism", "", 750, "Potion"],
         46:["Keen edge", "", 750, "Oil"],
         47:["Magic circle against (alignment)", "Magic circle against evil", 750, "Potion"],
         50:["Neutralize poison", "", 750, "Potion"],
         52:["Nondetection", "", 750, "Potion"],
         54:["Protection from energy (type)", "Protection from energy", 750, "Potion"],
         55:["Rage", "", 750, "Potion"],
         56:["Remove Blindness/Deafness", "Remove Blindness Deafness", 750, "Potion"],
         57:["Remove curse", "", 750, "Potion"],
         58:["Remove disease", "", 750, "Potion"],
         59:["Tongues", "", 750, "Potion"],
         60:["Water breathing", "", 750, "Potion"],
         61:["Water walk", "", 750, "Potion"],
         63:["Barkskin +4", "Barkskin", 900, "Potion"],
         64:["Shield of faith +5", "Shield of faith", 900, "Potion"],
         65:["Good hope", "", 1050, "Potion"],
         68:["Resist energy (type) 30", "Resist energy", 1100, "Potion"],
         69:["Barkskin +5", "Barkskin", 1200, "Potion"],
         73:["Greater magic fang +2", "Greater magic fang", 1200, "Potion"],
         77:["Greater magic weapon +2", "Greater magic weapon", 1200, "Oil"],
         81:["Magic vestment +2", "Magic vestment", 1200, "Oil"],
         82:["Protection from arrows 15/magic", "Protection from arrows", 1500, "Potion"],
         85:["Greater magic fang +3", "Greater magic fang", 1800, "Potion"],
         88:["Greater magic weapon +3", "Greater magic weapon", 1800, "Oil"],
         91:["Magic vestment +3", "Magic vestment", 1800, "Oil"],
         93:["Greater magic fang +4", "Greater magic fang", 2400, "Potion"],
         95:["Greater magic weapon +4", "Greater magic weapon", 2400, "Oil"],
         97:["Magic vestment +4", "Magic vestment", 2400, "Oil"],
         98:["Greater magic fang +5", "Greater magic fang", 3000, "Potion"],
         99:["Greater magic weapon +5", "Greater magic weapon", 3000, "Oil"],
         100:["Magic vestment +5", "Magic vestment", 3000, "Oil"]}
    PickPotion(t)

def PickPotion(t):
    potion = t[GetFromTable(t)]
    if potion[1]:
        html = "http://www.d20pfsrd.com/magic/all-spells/"+potion[0][0].lower()+"/"+potion[1].lower().replace(',','').replace("'",'-').replace(' ','-')
    else:
        html = "http://www.d20pfsrd.com/magic/all-spells/"+potion[0][0].lower()+"/"+potion[0].lower().replace(',','').replace("'",'-').replace(' ','-')
    print "{0} of {1} ({2:,} gp + material cost)\n{3}".format(potion[3], potion[0], potion[2], html)
    print "A character may make a Perception check (DC 15+spell level) to sample the potion and determine what it is. Increase the DC for rarer spells."

def PickMinorRing():
    t = {18: ['Protection +1', 'protection', 2000],
         28: ['Feather falling', '', 2200],
         36: ['Sustenance', '', 2500],
         44: ['Climbing', '', 2500],
         52: ['Jumping', '', 2500],
         60: ['Swimming', '', 2500],
         70: ['Counterspells', '', 4000],
         75: ['Mind shielding', '', 8000],
         80: ['Protection +2', 'protection', 8000],
         85: ['Force shield', '', 8500],
         90: ['Ram, the', 'the ram', 8600],
         93: ['Animal friendship', '', 10800],
         96: ['Energy resistance, minor', 'energy resistance', 12000],
         98: ['Chameleon power', '', 12700],
         100:['Water walking', '', 15000],
         103:["Dungeon ring, prisoner's", 'Dungeon ring', 250],
         113:['Arcane Signets', '', 1000],
         127:['Maniacal Devices', '', 5000],
         132:['Delayed Doom (1 stone)', 'Delayed Doom', 5000],
         134:['Forcefangs', '', 8000]}
    PickRing(t)

def PickMediumRing():
    t = {5: ['Counterspells', '', 4000],
         8: ['Mind shielding', '', 8000],
         18: ['Protection +2', 'protection', 8000],
         23: ['Force shield', '', 8500],
         28: ['the Ram', 'the ram', 8600],
         34: ['Climbing, improved', '', 10000],
         40: ['Jumping, improved', '', 10000],
         46: ['Swimming, improved', '', 10000],
         50: ['Animal friendship', '', 10800],
         56: ['Energy resistance, minor', 'energy resistance', 12000],
         61: ['Chameleon power', '', 12700],
         66: ['Water walking', '', 15000],
         71: ['Protection +3', 'protection', 18000],
         76: ['Spell storing, minor', '', 18000],
         81: ['Invisibility', '', 20000],
         85: ['Wizardry (I)', 'wizardry', 20000],
         90: ['Evasion', '', 25000],
         93: ['X-ray vision', '', 25000],
         97: ['Blinking', '', 27000],
         100: ['Energy resistance, major', 'energy resistance', 28000],
         115:['Maniacal Devices', '', 5000],
         128:['Delayed Doom (1 stone)', 'Delayed Doom', 5000],
         131:['Forcefangs', '', 8000],
         135:['Revelation, lesser', 'Revelation', 10000],
         142:['Delayed Doom (2 stones)', 'Delayed Doom', 10000],
         148:['Delayed Doom (3 stones)', 'Delayed Doom', 15000],
         151:['Retribution', '', 15000],
         154:["Dungeon ring, jailer's", 'Dungeon ring', 16000],
         158:['Revelation, greater', 'Revelation', 16000],
         159:['Delayed Doom (4 stones)', 'Delayed Doom', 20000],
         160:['Revelation, superior', 'Revelation', 24000],
         161:['Delayed Doom (5 stones)', 'Delayed Doom', 25000]}
    PickRing(t)

def PickMajorRing():
    t = {2:['Energy resistance, minor', 'energy resistance', 12000],
         7:['Protection +3', 'protection', 18000],
         10:['Spell storing, minor', '', 18000],
         15:['Invisibility', '', 20000],
         19:['Wizardry (I)', 'wizardry', 20000],
         25:['Evasion', '', 25000],
         28:['X-ray vision', '', 25000],
         32:['Blinking', '', 27000],
         39:['Energy resistance, major', 'energy resistance', 28000],
         49:['Protection +4', 'protection', 32000],
         55:['Wizardry (II)', 'wizardry', 40000],
         60:['Freedom of movement', '', 40000],
         63:['Energy resistance, greater', 'energy resistance', 44000],
         65:['Friend shield(pair)', 'friend shield', 50000],
         70:['Protection +5', 'protection', 50000],
         74:['Shooting stars', '', 50000],
         79:['Spell storing', '', 50000],
         83:['Wizardry (III)', 'wizardry', 70000],
         86:['Telekinesis', '', 75000],
         88:['Regeneration', '', 90000],
         91:['Spell turning', '', 100000],
         93:['Wizardry (IV)', 'wizardry', 100000],
         94:['Three wishes', '', 120000],
         95:['Djinni calling', '', 125000],
         96:['Elemental command (air)', 'elemental command', 200000],
         97:['Elemental command (earth)', 'elemental command', 200000],
         98:['Elemental command (fire)', 'elemental command', 200000],
         99:['Elemental command (water)', 'elemental command', 200000],
         100:['Spell storing, major', '', 200000],
         101:['Delayed Doom (2 stones)', 'Delayed Doom', 10000],
         105:['Delayed Doom (3 stones)', 'Delayed Doom', 15000],
         112:['Retribution', '', 15000],
         114:["Dungeon ring, jailer's", 'Dungeon ring', 16000],
         116:['Revelation, greater', 'Revelation', 16000],
         128:['Delayed Doom (4 stones)', 'Delayed Doom', 20000],
         129:['Revelation, superior', 'Revelation', 24000],
         135:['Delayed Doom (5 stones)', 'Delayed Doom', 25000],
         138:['Delayed Doom (6 stones)', 'Delayed Doom', 30000],
         140:['Delayed Doom (7 stones)', 'Delayed Doom', 35000],
         141:['Delayed Doom (8 stones)', 'Delayed Doom', 40000],
         142:['Delayed Doom (9 stones)', 'Delayed Doom', 45000]}
    PickRing(t)

def PickRing(t):
    ring = t[GetFromTable(t)]
    if ring[1]:
        html = "http://www.d20pfsrd.com/magic-items/rings/ring-of-"+ring[1].lower().replace(',','').replace(' ','-')
    else:
        html = "http://www.d20pfsrd.com/magic-items/rings/ring-of-"+ring[0].lower().replace(',','').replace(' ','-')
    print "Ring of {0} ({1:,} gp)\n{2}".format(ring[0], ring[2], html)
    t = {1:"The ring is intelligent. http://www.d20pfsrd.com/magic-items/intelligent-items",
         31:"Something (a design, inscription, or the like) provides a clue to its function.",
         100:"No special qualities."}
    print t[GetFromTable(t)]

def PickMinorRod():
    print "No code for rods yet"
    
def PickMediumRod():
    print "No code for rods yet"
    
def PickMajorRod():
    print "No code for rods yet"

def PickMinorScroll():
    t = {5:[0, 12.5],
         50:[1, 25],
         95:[2, 150],
         100:[3, 375]}
    PickScroll(t)
    
def PickMediumScroll():
    t = {5:[2, 150],
         65:[3, 375],
         95:[4, 700],
         100:[5, 1125]}
    PickScroll(t)
    
def PickMajorScroll():
    t = {5:[4, 700],
         50:[5, 1125],
         70:[6, 1650],
         85:[7, 2275],
         95:[8, 3000],
         100:[9, 3825]}
    PickScroll(t)

def PickScroll(t):
    scroll = t[GetFromTable(t)]
    name = random.choice(SpellLists[scroll[0]])
    html = ("http://www.d20pfsrd.com/magic/all-spells/"+name[0].lower()+"/"+
            name.split(',')[0].lower().replace(' ','-'))
    print "Scroll of {0} ({1:,} gp + material cost)\n{2}".format(name, scroll[1], html)
    print "The scroll can be deciphered with a Read Magic spell or a successful Spellcraft check (DC 20 + spell level). Deciphering a scroll is a full-round action."

def PickMinorStaff():
    print "No code for staffs yet"
    
def PickMediumStaff():
    print "No code for staffs yet"
    
def PickMajorStaff():
    print "No code for staffs yet"

def PickMinorWand():
    t = {5:[0, 375],
         60:[1, 750],
         100:[2, 4500]}
    PickWand(t)
    
def PickMediumWand():
    t = {60:[2, 4500],
         100:[3, 11250]}
    PickWand(t)
    
def PickMajorWand():
    t = {60:[3, 11250],
         100:[4, 21000]}
    PickWand(t)

def PickWand(t):
    wand = t[GetFromTable(t)]
    name = random.choice(SpellLists[wand[0]])
    html = ("http://www.d20pfsrd.com/magic/all-spells/"+name[0].lower()+"/"+
            name.split(',')[0].lower().replace(' ','-'))
    print "Wand of {0} ({1:,} gp + material cost x 50)\n{2}".format(name, wand[1], html)
    t = {30:"Something (a design, inscription, or the like) provides a clue to its function.",
         100:"No special qualities."}
    print t[GetFromTable(t)]

def PickMinorWondrousItem():
    t = {1:['Feather token, anchor', 'feather token/anchor token', 50],
         2:['Universal solvent', '', 50],
         3:['Elixir of love', '', 150],
         4:['Unguent of timelessness', '', 150],
         5:['Feather token, fan', 'feather token/fan token', 200],
         6:['Dust of tracelessness', '', 250],
         7:['Elixir of hiding', '', 250],
         8:['Elixir of tumbling', '', 250],
         9:['Elixir of swimming', '', 250],
         10:['Elixir of vision', '', 250],
         11:['Silversheen', '', 250],
         12:['Feather token, bird', 'feather token/bird token', 300],
         13:['Feather token, tree', 'feather token/tree token', 400],
         14:['Feather token, swan boat', 'feather token/swan boat token', 450],
         15:['Elixir of truth', '', 500],
         16:['Feather token, whip', 'feather token/whip token', 500],
         17:['Dust of dryness', '', 850],
         18:['Hand of the mage', '', 900],
         19:['Bracers of armor +1', 'Bracers of armor', 1000],
         20:['Cloak of resistance +1', 'Cloak of resistance', 1000],
         21:['Pearl of power, 1st-level spell', 'Pearl of power', 1000],
         22:['Phylactery of faithfulness', '', 1000],
         23:['Salve of slipperiness', '', 1000],
         24:['Elixir of fire breath', '', 1100],
         25:['Pipes of the sewers', '', 1150],
         26:['Dust of illusion', '', 1200],
         27:['Brooch of shielding', '', 1500],
         28:['Necklace of fireballs type I', 'Necklace of fireballs', 1650],
         29:['Dust of appearance', '', 1800],
         30:['Hat of disguise', '', 1800],
         31:['Pipes of sounding', '', 1800],
         32:['Efficient quiver', '', 1800],
         33:['Amulet of natural armor +1', 'Amulet of natural armor', 2000],
         34:['Handy haversack', '', 2000],
         35:['Horn of fog', '', 2000],
         36:['Elemental gem', '', 2250],
         37:['Robe of bones', '', 2400],
         38:['Sovereign glue', '', 2400],
         39:['Bag of holding type I', 'Bag of holding', 2500],
         40:['Boots of elvenkind', '', 2500],
         41:['Boots of the winterlands', '', 2500],
         42:['Candle of truth', '', 2500],
         43:['Cloak of elvenkind', '', 2500],
         44:['Eyes of the eagle', '', 2500],
         45:['Goggles of minute seeing', '', 2500],
         46:['Scarab, golembane', '', 2500],
         47:['Necklace of fireballs type II', 'Necklace of fireballs', 2700],
         48:['Stone of alarm', '', 2700],
         49:['Bead of force', '', 3000],
         50:['Chime of opening', '', 3000],
         51:['Horseshoes of speed', '', 3000],
         52:['Rope of climbing', '', 3000],
         53:['Bag of tricks, gray', '', 3400],
         54:['Dust of disappearance', '', 3500],
         55:['Lens of detection', '', 3500],
         56:["Vestment, druid's", 'Vestment druid-s', 3750],
         57:['Figurine of wondrous power, silver raven', 'Figurines of wondrous power/silver raven Figurine of wondrous power', 3800],
         58:['Belt of giant strength +2', 'Belt of giant strength', 4000],
         59:['Belt of incredible dexterity +2', 'Belt of incredible dexterity', 4000],
         60:['Belt of mighty constitution +2', 'Belt of mighty constitution', 4000],
         61:['Bracers of armor +2', 'Bracers of armor', 4000],
         62:['Cloak of resistance +2', 'Cloak of resistance', 4000],
         63:['Gloves of arrow snaring', '', 4000],
         64:['Headband of alluring charisma +2', 'Headband of alluring charisma', 4000],
         65:['Headband of inspired wisdom +2', 'Headband of inspired wisdom', 4000],
         66:['Headband of vast intelligence +2', 'Headband of vast intelligence', 4000],
         67:['Ioun stone, clear spindle', 'Ioun stones', 4000],
         68:['Restorative ointment', '', 4000],
         69:['Marvelous pigments', '', 4000],
         70:['Pearl of power, 2nd-level spell', 'Pearl of power', 4000],
         71:['Stone salve', '', 4000],
         72:['Necklace of fireballs type III', 'Necklace of fireballs', 4350],
         73:['Circlet of persuasion', '', 4500],
         74:['Slippers of spider climbing', '', 4800],
         75:['Incense of meditation', '', 4900],
         76:['Amulet of mighty fists +1', 'Amulet of mighty fists', 5000],
         77:['Bag of holding type II', 'Bag of holding', 5000],
         78:['Bracers of archery, lesser', 'Bracers of archery', 5000],
         79:['Ioun stone, dusty rose prism', 'Ioun stones', 5000],
         80:['Helm of comprehend languages and read magic', '', 5200],
         81:['Vest of escape', '', 5200],
         82:['Eversmoking bottle', '', 5400],
         83:['Sustaining spoon', '', 5400],
         84:['Necklace of fireballs type IV', 'Necklace of fireballs', 5400],
         85:['Boots of striding and springing', '', 5500],
         86:['Wind fan', '', 5500],
         87:['Necklace of fireballs type V', 'Necklace of fireballs', 5850],
         88:['Horseshoes of a zephyr', '', 6000],
         89:['Pipes of haunting', '', 6000],
         90:['Gloves of swimming and climbing', '', 6250],
         91:['Crown of blasting, minor', 'Crown of blasting', 6480],
         92:['Horn of goodness/evil', 'Horn of goodness evil', 6500],
         93:['Robe of useful items', '', 7000],
         94:['Boat, folding', '', 7200],
         95:['Cloak of the manta ray', '', 7200],
         96:['Bottle of air', '', 7250],
         97:['Bag of holding type III', 'Bag of holding', 7400],
         98:['Periapt of health', '', 7400],
         99:['Boots of levitation', '', 7500],
         100:['Harp of charming', '', 7500],
         101:['Ioun torch', '', 75],
         102:['War paint of the terrible visage', 'paint War paint of the terrible visage', 100],
         103:['Assisting glove', 'glove Assisting glove', 180],
         104:['Bandages of rapid recovery', '', 200],
         105:['Catching cape', 'cape Catching cape', 200],
         106:['Soul soap', '', 200],
         107:['Bottle of messages', '', 300],
         108:['Key of lock jamming', '', 400],
         109:['Campfire bead', '', 720],
         110:['Defoliant polish', '', 800],
         111:['Dust of emulation', '', 800],
         112:['Muleback cords', '', 1000],
         113:['All tools vest', 'vest All tools vest', 1800],
         114:['Cowardly crouching cloak', 'cloak Cowardly crouching cloak', 1800],
         115:['Scabbard of vigor', '', 1800],
         116:['Clamor box', '', 2000],
         117:['Glowing glove', 'glove Glowing glove', 2000],
         118:['Manacles of cooperation', '', 2000],
         119:["Knight's pennon (honor)", 'Knight-s pennon', 2200],
         120:['Flying ointment', '', 2250],
         121:['Boots of friendly terrain', '', 2400],
         122:['Apple of eternal sleep', '', 2500],
         123:['Cauldron of brewing', '', 3000],
         124:['Philter of love', '', 3000],
         125:['Sash of the war champion', '', 4000],
         126:["Knight's pennon (battle)", 'Knight-s pennon', 4500],
         127:["Knight's pennon (parley)", 'Knight-s pennon', 4500],
         128:['Helm of fearsome mien', '', 5000],
         129:['Horn of the huntmaster', '', 5000],
         130:['Scabbard of stanching', '', 5000],
         131:['Sheath of bladestealth', '', 5000]}
    PickWondrousItem(t)

def PickMediumWondrousItem():
    t = {1:['Amulet of natural armor +2', 'Amulet of natural armor', 8000],
         2:['Golem manual, flesh golem', 'Golem manual', 8000],
         3:['Hand of glory', '', 8000],
         4:['Ioun stone, deep red sphere', 'Ioun stones', 8000],
         5:['Ioun stone, incandescent blue sphere', 'Ioun stones', 8000],
         6:['Ioun stone, pale blue rhomboid', 'Ioun stones', 8000],
         7:['Ioun stone, pink and green sphere', 'Ioun stones', 8000],
         8:['Ioun stone, pink rhomboid', 'Ioun stones', 8000],
         9:['Ioun stone, scarlet and blue sphere', 'Ioun stones', 8000],
         10:['Deck of illusions', '', 8100],
         11:['Necklace of fireballs type VI', 'Necklace of fireballs', 8100],
         12:['Candle of invocation', '', 8400],
         13:['Robe of blending', '', 8400],
         14:['Bag of tricks, rust', 'Bag of tricks', 8500],
         15:['Necklace of fireballs type VII', 'Necklace of fireballs', 8700],
         16:['Bracers of armor +3', 'Bracers of armor', 9000],
         17:['Cloak of resistance +3', 'Cloak of resistance', 9000],
         18:['Decanter of endless water', '', 9000],
         19:['Necklace of adaptation', '', 9000],
         20:['Pearl of power, 3rd-level spell', 'Pearl of power', 9000],
         21:['Figurine of wondrous power, serpentine owl', 'Figurines of wondrous power/serpentine owl Figurine of wondrous power', 9100],
         22:['Strand of prayer beads, lesser', 'Strand of prayer beads', 9600],
         23:['Bag of holding type IV', 'Bag of holding', 10000],
         24:['Belt of physical might +2', 'Belt of physical might', 10000],
         25:['Figurine of wondrous power, bronze griffon', 'Figurines of wondrous power/bronze griffon Figurine of wondrous power', 10000],
         26:['Figurine of wondrous power, ebony fly', 'Figurines of wondrous power/ebony fly Figurine of wondrous power', 10000],
         27:['Glove of storing', '', 10000],
         28:['Headband of mental prowess +2', 'Headband of mental prowess', 10000],
         29:['Ioun stone, dark blue rhomboid', 'Ioun stones', 10000],
         30:['Cape of the mountebank', '', 10080],
         31:['Phylactery of negative channeling', '', 11000],
         32:['Phylactery of positive channeling', '', 11000],
         33:['Gauntlet of rust', '', 11500],
         34:['Boots of speed', '', 12000],
         35:['Goggles of night', '', 12000],
         36:['Golem manual, clay', 'Golem manual', 12000],
         37:['Medallion of thoughts', '', 12000],
         38:['Blessed book', 'book blessed', 12500],
         39:['Gem of brightness', '', 13000],
         40:['Lyre of building', '', 13000],
         41:["Robe, Monk's", 'robe monk s', 13000],
         42:['Cloak of arachnida', '', 14000],
         43:['Belt of dwarvenkind', '', 14900],
         44:['Periapt of wound closure', '', 15000],
         45:['Pearl of the sirines', '', 15300],
         46:['Figurine of wondrous power, onyx dog', 'Figurines of wondrous power/onyx dog Figurine of wondrous power', 15500],
         47:['Bag of tricks, tan', 'Bag of tricks', 16000],
         48:['Belt of giant strength +4', 'Belt of giant strength', 16000],
         49:['Belt of incredible dexterity +4', 'Belt of incredible dexterity', 16000],
         50:['Belt of mighty constitution +4', 'Belt of mighty constitution', 16000],
         51:['Belt of physical perfection +2', 'Belt of physical perfection', 16000],
         52:['Boots, winged', '', 16000],
         53:['Bracers of armor +4', 'Bracers of armor', 16000],
         54:['Cloak of resistance +4', 'Cloak of resistance', 16000],
         55:['Headband of alluring charisma +4', 'Headband of alluring charisma', 16000],
         56:['Headband of inspired wisdom +4', 'Headband of inspired wisdom', 16000],
         57:['Headband of mental superiority +2', 'Headband of mental superiority', 16000],
         58:['Headband of vast intelligence +4', 'Headband of vast intelligence', 16000],
         59:['Pearl of power, 4th-level spell', 'Pearl of power', 16000],
         60:['Scabbard of keen edges', '', 16000],
         61:['Figurine of wondrous power, golden lions', 'Figurines of wondrous power/golden lions Figurine of wondrous power', 16500],
         62:['Chime of interruption', '', 16800],
         63:['Broom of flying', '', 17000],
         64:['Figurine of wondrous power, marble elephant', 'Figurines of wondrous power/marble elephant Figurine of wondrous power', 17000],
         65:['Amulet of natural armor +3', 'Amulet of natural armor', 18000],
         66:['Ioun stone, iridescent spindle', 'Ioun stones', 18000],
         67:['Bracelet of friends', '', 19000],
         68:['Amulet of mighty fists +2', 'Amulet of mighty fists', 20000],
         69:['Carpet of flying, 5 ft. by 5 ft.', 'Carpet of flying', 20000],
         70:['Horn of blasting', '', 20000],
         71:['Ioun stone, pale lavender ellipsoid', 'Ioun stones', 20000],
         72:['Ioun stone, pearly white spindle', 'Ioun stones', 20000],
         73:['Portable hole', '', 20000],
         74:['Stone of good luck (luckstone)', 'Stone of good luck luckstone', 20000],
         75:['Figurine of wondrous power, ivory goats', 'Figurines of wondrous power/ivory goats Figurine of wondrous power', 21000],
         76:['Rope of entanglement', '', 21000],
         77:['Golem manual, stone', 'Golem manual', 22000],
         78:['Mask of the skull', '', 22000],
         79:['Mattock of the titans', '', 23348],
         80:['Crown of blasting, major', 'Crown of blasting', 23760],
         81:['Cloak of displacement, minor', 'Cloak of displacement', 24000],
         82:['Helm of underwater action', '', 24000],
         83:['Bracers of archery, greater', 'Bracers of archery', 25000],
         84:['Bracers of armor +5', 'Bracers of armor', 25000],
         85:['Cloak of resistance +5', 'Cloak of resistance', 25000],
         86:['Eyes of doom', '', 25000],
         87:['Pearl of power, 5th-level spell', 'Pearl of power', 25000],
         88:['Maul of the titans', '', 25305],
         89:['Cloak of the bat', '', 26000],
         90:['Iron bands of binding', '', 26000],
         91:['Cube of frost resistance', '', 27000],
         92:['Helm of telepathy', '', 27000],
         93:['Periapt of proof against poison', '', 27000],
         94:['Robe of scintillating colors', '', 27000],
         95:['Manual of bodily health +1', 'book Manual of bodily health', 27500],
         96:['Manual of gainful exercise +1', 'book Manual of gainful exercise', 27500],
         97:['Manual of quickness in action +1', 'book Manual of quickness in action', 27500],
         98:['Tome of clear thought +1', 'Tome of clear thought', 27500],
         99:['Tome of leadership and influence +1', 'Tome of leadership and influence', 27500],
         100:['Tome of understanding +1', 'Tome of understanding', 27500],
         101:["Grappler's mask", 'mask Grappler-s mask', 5000],
         102:['Torc of lionheart fury', '', 8000],
         103:['Amulet of spell cunning', '', 10000],
         104:['Construct channel brick', '', 10000],
         105:['Doomharp', 'harp Doomharp', 10000],
         106:['Ki mat', '', 10000],
         107:["Lord's banner (swiftness)", "Lord's banner", 10000],
         108:['Crystal of healing hands', '', 12000],
         109:['Book of the loremaster', '', 15000],
         110:['Bracelet of mercy', '', 15000],
         111:['Cauldron of plenty', '', 15000],
         112:['Gloves of dueling', '', 15000],
         113:['Necklace of ki serenity', '', 16000],
         114:['Robes of arcane heritage', '', 16000],
         115:['Silver smite bracelet', '', 16000],
         116:['Vest of the cockroach', '', 16000],
         117:['Amulet of magecraft', '', 20000],
         118:['Horn of antagonism', '', 20000],
         119:['Moon circlet', 'circlet Moon circlet', 20000],
         120:["Necromancer's athame", "Necromancer's athame", 20000],
         121:['Sniper goggles', 'goggles Sniper goggles', 20000],
         122:['Annihilation spectacles', '', 25000]}
    PickWondrousItem(t)

def PickMajorWondrousItem():
    t = {1:['Dimensional shackles', '', 28000],
         2:['Figurine of wondrous power, obsidian steed', 'Figurines of wondrous power/obsidian steed Figurine of wondrous power', 28500],
         3:['Drums of panic', '', 30000],
         4:['Ioun stone, orange prism', 'Ioun stones', 30000],
         5:['Ioun stone, pale green prism', 'Ioun stones', 30000],
         6:['Lantern of revealing', '', 30000],
         7:['Amulet of natural armor +4', 'Amulet of natural armor', 32000],
         8:['Amulet of proof against detection and location', 'Amulet of proof against detection and location', 35000],
         9:['Carpet of flying, 5 ft. by 10 ft.', 'Carpet of flying', 35000],
         10:['Golem manual, iron', 'Golem manual', 35000],
         11:['Belt of giant strength +6', 'Belt of giant strength', 36000],
         12:['Belt of incredible dexterity +6', 'Belt of incredible dexterity', 36000],
         13:['Belt of mighty constitution +6', 'Belt of mighty constitution', 36000],
         14:['Bracers of armor +6', 'Bracers of armor', 36000],
         15:['Headband of alluring charisma +6', 'Headband of alluring charisma', 36000],
         16:['Headband of inspired wisdom +6', 'Headband of inspired wisdom', 36000],
         17:['Headband of vast intelligence +6', 'Headband of vast intelligence', 36000],
         18:['Ioun stone, vibrant purple prism', 'Ioun stones', 36000],
         19:['Pearl of power, 6th-level spell', 'Pearl of power', 36000],
         20:['Scarab of protection', '', 38000],
         21:['Belt of physical might +4', 'Belt of physical might', 40000],
         22:['Headband of mental prowess +4', 'Headband of mental prowess', 40000],
         23:['Ioun stone, lavender and green ellipsoid', 'Ioun stones', 40000],
         24:['Ring gates', '', 40000],
         25:['Crystal ball', '', 42000],
         26:['Golem manual, stone guardian', 'Golem manual', 44000],
         27:['Amulet of mighty fists +3', 'Amulet of mighty fists', 45000],
         28:['Strand of prayer beads', '', 45800],
         29:['Orb of storms', '', 48000],
         30:['Boots of teleportation', '', 49000],
         31:['Bracers of armor +7', 'Bracers of armor', 49000],
         32:['Pearl of power, 7th-level spell', 'Pearl of power', 49000],
         33:['Amulet of natural armor +5', 'Amulet of natural armor', 50000],
         34:['Cloak of displacement, major', 'Cloak of displacement', 50000],
         35:['Crystal ball with see invisibility', 'Crystal ball', 50000],
         36:['Horn of Valhalla', '', 50000],
         37:['Crystal ball with detect thoughts', 'Crystal ball', 51000],
         38:['Wings of flying', '', 54000],
         39:['Cloak of etherealness', '', 55000],
         40:['Instant fortress', '', 55000],
         41:['Manual of bodily health +2', 'Manual of bodily health', 55000],
         42:['Manual of gainful exercise +2', 'Manual of gainful exercise', 55000],
         43:['Manual of quickness in action +2', 'Manual of quickness in action', 55000],
         44:['Tome of clear thought +2', 'Tome of clear thought', 55000],
         45:['Tome of leadership and influence +2', 'Tome of leadership and influence', 55000],
         46:['Tome of understanding +2', 'Tome of understanding', 55000],
         47:['Eyes of charming', '', 56000],
         48:['Robe of stars', '', 58000],
         49:['Carpet of flying, 10 ft. by 10 ft.', 'Carpet of flying', 60000],
         50:['Darkskull', '', 60000],
         51:['Cube of force', '', 62000],
         52:['Belt of physical perfection +4', 'Belt of physical perfection', 64000],
         53:['Bracers of armor +8', 'Bracers of armor', 64000],
         54:['Headband of mental superiority +4', 'Headband of mental superiority', 64000],
         55:['Pearl of power, 8th-level spell', 'Pearl of power', 64000],
         56:['Crystal ball with telepathy', 'Crystal ball', 70000],
         57:['Horn of blasting, greater', 'Horn of blasting', 70000],
         58:['Pearl of power, two spells', 'Pearl of power', 70000],
         59:['Helm of teleportation', '', 73500],
         60:['Gem of seeing', '', 75000],
         61:['Robe of the archmagi', '', 75000],
         62:['Mantle of faith', '', 76000],
         63:['Amulet of mighty fists +4', 'Amulet of mighty fists', 80000],
         64:['Crystal ball with true seeing', 'Crystal ball', 80000],
         65:['Pearl of power, 9th-level spell', 'Pearl of power', 81000],
         66:['Well of many worlds', '', 82000],
         67:['Manual of bodily health +3', 'Manual of bodily health', 82500],
         68:['Manual of gainful exercise +3', 'Manual of gainful exercise', 82500],
         69:['Manual of quickness in action +3', 'Manual of quickness in action', 82500],
         70:['Tome of clear thought +3', 'Tome of clear thought', 82500],
         71:['Tome of leadership and influence +3', 'Tome of leadership and influence', 82500],
         72:['Tome of understanding +3', 'Tome of understanding', 82500],
         73:['Apparatus of the crab', '', 90000],
         74:['Belt of physical might +6', 'Belt of physical might', 90000],
         75:['Headband of mental prowess +6', 'Headband of mental prowess', 90000],
         76:['Mantle of spell resistance', '', 90000],
         77:['Mirror of opposition', '', 92000],
         78:['Strand of prayer beads, greater', 'Strand of prayer beads', 95800],
         79:['Manual of bodily health +4', 'Manual of bodily health', 110000],
         80:['Manual of gainful exercise +4', 'Manual of gainful exercise', 110000],
         81:['Manual of quickness in action +4', 'Manual of quickness in action', 110000],
         82:['Tome of clear thought +4', 'Tome of clear thought', 110000],
         83:['Tome of leadership and influence +4', 'Tome of leadership and influence', 110000],
         84:['Tome of understanding +4', 'Tome of understanding', 110000],
         85:['Amulet of the planes', '', 120000],
         86:['Robe of eyes', '', 120000],
         87:['Amulet of mighty fists +5', 'Amulet of mighty fists', 125000],
         88:['Helm of brilliance', '', 125000],
         89:['Manual of bodily health +5', 'Manual of bodily health', 137500],
         90:['Manual of gainful exercise +5', 'Manual of gainful exercise', 137500],
         91:['Manual of quickness in action +5', 'Manual of quickness in action', 137500],
         92:['Tome of clear thought +5', 'Tome of clear thought', 137500],
         93:['Tome of leadership and influence +5', 'Tome of leadership and influence', 137500],
         94:['Tome of understanding +5', 'Tome of understanding', 137500],
         95:['Belt of physical perfection +6', 'Belt of physical perfection', 144000],
         96:['Headband of mental superiority +6', 'Headband of mental superiority', 144000],
         97:['Efreeti bottle', '', 145000],
         98:['Cubic gate', '', 164000],
         99:['Iron flask', '', 170000],
         100:['Mirror of life trapping', '', 200000],
         101:['Cauldron of the dead', '', 30000],
         102:['Mask of giants (lesser)', 'Mask of giants', 30000],
         103:['Cauldron of resurrection', '', 33000],
         104:['Cauldron of flying', '', 40000],
         105:['Cauldron of seeing', '', 42000],
         106:["Lord's banner (terror)", 'Lord-s banner', 56000],
         107:["Lord's banner (victory)", 'Lord-s banner', 75000],
         108:['Mask of giants (greater)', 'Mask of giants', 90000],
         109:["Lord's banner (crusades)", 'Lord-s banner', 100000]}
    PickWondrousItem(t)

def PickWondrousItem(t):
    item = t[GetFromTable(t)]
    t = {'a':'a-b', 'b':'a-b', 'c':'c-d', 'd':'c-d', 'e':'e-g', 'f':'e-g', 'g':'e-g',
         'h':'h-l', 'i':'h-l', 'j':'h-l', 'k':'h-l', 'l':'h-l', 'm':'m-p', 'n':'m-p', 'o':'m-p', 'p':'m-p',
         'q':'q', 'r':'r-z', 's':'r-z', 't':'r-z', 'u':'r-z', 'v':'r-z', 'w':'r-z', 'x':'r-z', 'y':'r-z', 'z':'r-z'}
    if item[1]:
        name = item[1]
    else:
        name = item[0]
    name = name.lower().replace(',','').replace(' ','-').replace("'",'-')
    html = "http://www.d20pfsrd.com/magic-items/wondrous-items/wondrous-items/"+t[name[0]]+"/"+name
    print "{0} ({1:,} gp)\n{2}".format(item[0], item[2], html)
    t = {1:"The item is intelligent. http://www.d20pfsrd.com/magic-items/intelligent-items",
         31:"Something (a design, inscription, or the like) provides a clue to its function.",
         100:"No special qualities."}
    print t[GetFromTable(t)]

num_minor  = RollDice(1,1)
num_medium = RollDice(1,1)
num_major  = RollDice(1,1)

if num_minor:
    print "Power: Minor"
    for i in xrange(num_minor):
        PickMinorItem()
        print ""
    print ""

if num_medium:
    print "Power: Medium"
    for i in xrange(num_medium):
        PickMediumItem()
        print ""
    print ""

if num_major:
    print "Power: Major"
    for i in xrange(num_major):
        PickMajorItem()
        print ""
    print ""

##print "Power of magic item?"
##print "0) Random"
##print "1) Minor  (avg value 1,000 gp)"
##print "2) Medium (avg value 10,000 gp)"
##print "3) Major  (avg value 40,000 gp)"
##power = input("? ")
##if power == 0:
##    power = random.randint(1,3)
##
##print "Power:", {1:"Minor", 2:"Medium", 3:"Major"}.get(power)


