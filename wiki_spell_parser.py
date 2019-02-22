# Meant for grabbing data from https://www.dnd-spells.com

from requests import get
import re

reg = re.compile('<h1 class="classic-title"><span>(?P<title>.*?)</span></h1>\s*(<span class="ee">.*?</span>\s*)?'
                 '<p>(?P<school>.*?)</p>\s*<p>\s*Level: <strong>(?P<level>.*?)</strong> <br />\s*Casting time: '
                 '<strong>(?P<casting_time>.*?)</strong> <br />\s*Range: <strong>(?P<range>.*?)</strong> <br />\s*'
                 'Components: <strong>(?P<components>.*?)</strong> <br />\s*Duration: <strong>(?P<duration>.*?)'
                 '</strong> <br />\s*<hr>\s*</p>\s*<p>\s*(?P<description>.*?)</p>\s*'
                 '(<h4 class="classic-title"><span>At higher level</span></h4>\s*<p>\s*(?P<higher_levels>.*?)\s*</p>)?'
                 '\s*<hr>\s*<p>\s*Page: (?P<page>\d+)\s*(from )?(?P<source>.*?)\s*</p>\s*<hr>\s*'
                 '<p>\s*A\s*(?P<classes>.*?)\s*spell\s*</p>',
                 re.MULTILINE | re.DOTALL)


def parse_spell(name):
    r = get("https://www.dnd-spells.com/spell/" + name.lower().replace(" ", "-").replace("'", ""))
    # print(r.text)

    m = re.search(reg, r.text)
    # print(m)
    # print(m.group('school'))
    # print(m.group('casting_time'))
    # print(m.group('range'))
    # print(m.group('components'))
    # print(m.group('duration'))
    # print(m.group('description'))
    # print(m.group('higher_levels'))
    # print(m.group('page'))
    # print(m.group('source'))
    # print(m.group('classes'))

    ritual_spell = "(Ritual)" in m.group('title')
    title = m.group('title').lower().replace(' ', '-').replace("'", "-")
    if ritual_spell:
        title = title[:len(" (Ritual)") - 1]

    level = m.group('level').lower().strip()
    if level == "cantrip":
        level = "cantrip"
    elif level == "1":
        level = "1st_level_spell"
    elif level == "2":
        level = "2nd_level_spell"
    elif level == "3":
        level = "3rd_level_spell"
    else:
        level = level + "th_level_spell"

    verbal_component = re.search(r"\bV\b", m.group('components'))
    somatic_component = re.search(r"\bS\b", m.group('components'))
    material_component = re.search(r"\bM\b", m.group('components'))
    material_desc = re.search(r"\((.*)\)", m.group('components'))
    expensive_material_component = re.search(r"\bworth\b", m.group('components'))
    material_component_consumed = re.search(r"\bconsumed\b", m.group('components'))

    duration = m.group('duration')
    concentration_prefix = "Concentration, up to "
    concentration_spell = concentration_prefix in m.group('duration')
    if concentration_spell:
        duration = duration[len(concentration_prefix):]

    description = m.group('description').strip().replace("\r", "").replace("\n", "").replace("<br />", r"\n").replace("’", "'")

    if m.group('source') == "Players Handbook":
        source = "phb"
    elif m.group('source') == "Sword Coast Adventure's Guide":
        source = "scag"
    elif m.group('source') == "Xanathar's Guide To Everything":
        source = "xgte"
    else:
        raise Exception(f"Unknown source: {m.group('source')}")

    print(f"http://private-5e.wikidot.com/spell:{title}")
    print()

    output = ""

    classes = m.group('classes').lower()
    for c in ['bard', 'cleric', 'druid', 'paladin', 'ranger', 'sorcerer', 'warlock', 'wizard']:
        output += c + '_spell: ' + (c + '_spell' if c in classes else "'0'") + "\n"

    output += f"""level: {level}
school: {m.group('school').lower()}_school
ritual_spell: {'ritual_spell' if ritual_spell else "'0'"}
casting_time: '{m.group('casting_time').lower()}'
range: '{m.group('range')}'
verbal_component: {"verbal_component" if verbal_component else "'0'"}
somatic_component: {"somatic_component" if somatic_component else "'0'"}
material_component: {"material_component" if material_component else "'0'"}
material_desc: '{material_desc.group(1) if material_desc else ""}'
expensive_material_component: {"expensive_material_component" if expensive_material_component else "'0'"}
material_component_consumed: {"material_component_consumed" if material_component_consumed else "'0'"}
duration: '{duration}'
concentration_spell: {"concentration_spell" if concentration_spell else "'0'"}
description: "{description}"
at_higher_levels: {"at_higher_levels" if m.group('higher_levels') else "'0'"}
at_higher_levels_text: '{m.group('higher_levels') if m.group('higher_levels') else ""}'
sourcebook: {source}
page: '{m.group('page')}'
"""

    print(output)


for spell in """
Toll the Dead
Wall of Light
Word of Radiance
Wrath of Nature
Zephyr Strike
""".split('\n'):
    if spell:
        parse_spell(spell)
        print()
