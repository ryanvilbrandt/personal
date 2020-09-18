# A generator for https://drive.google.com/file/d/0BwfS-XJksxRnTHYxTWxqazMwY0k/view
import random
import re
from collections import OrderedDict

academic_table = """
1 Caught with banned books. Expelled. Move to Life Experience Table. 51 Developed a drug habit. WIS -1
2 Joined scientific expedition for month. STR +1 52 Discovered two new species of plants. Useful in Alchemy. INT +2
3 Poisoned by large spider in Library. Recover. CON +1 53 Helped elderly cleric minister to the poor. WIS +1
4 Took job as delivery boy for campus mail system. DEX +1 54 Helped create constructs for head wizard. INT +1
5 Spent month studying nature. WIS +1 55 Forecasted a major flood and saved numerous lives. WIS +1
6 Discovered rare tome of obscure subject. INT +1 56 Contract major illness. Unable to study or attend classes. INT -1
7 Took a month to rally for workers rights under a brutal leader. CHA +1 57 Robbed at knife point. Talked thugs out of it. CHA +1
8 Forced to avoid crazy Ex while attending classes. DEX +1 58 Tamed a small bear with treats and soft words. WIS +2
9 Roomed with a student from another realm. CHA +1 59 Out ran a supposedly tamed bear when it attacked a crowd. DEX +1
10 Shanghaied. Forced to serve on pirate ship. Move to Military Table. 60 You find a ship wreck, in the desert. Copied strange symbols. INT +1
11 Earned money transcribing spell books for a month. INT +1 61 Joined the choir to impress the opposite sex. CHA +1
12 Death of a close friend brings meaning to your life. WIS +2 62 Researched venomous snakes. Wrote a paper. WIS +1
13 Spent month studying Architecture of nearby castle. INT +1 63 You take a month off to find yourself. CHA +1, WIS -1
14 Omens become more clear and meaningful to you. WIS +1 64 Repaired fishing nets for room and board. DEX +1
15 Hiked across realm collecting insect samples. CON +1 65 Elected Academic body president. CHA +1
16 Worked in a mine as a mineral identifier. STR +1 66 Shortest route to class was across roof tops. DEX +1
17 Ran for local political office. CHA +1 67 Successfully brew homemade healing potion. WIS +1
18 Grew up hunting with a bow. DEX +1 68 Received a "first" in cantrips. INT +1
19 Father instilled love of books. Didn't play outside much. INT +2, CON -1 69 Introduced to mysticism. WIS +1
20 Cared for elderly relative. WIS +1 70 Created overly elaborate mechanism to turn book pages. INT +2
21 Raised by low level noble parents. Best of all things. Educated. INT +1 71 Was assigned a dorm on the 8th floor. STR +1
22 First Aid course turns real when goblins attack. WIS +1 72 Went without sleep for three days while exams were given. CON +1
23 Have a knack for Chess. Play constantly. INT +1 73 Started "filling out". Better late than never. CHA +1
24 Study animal tracks in the field. WIS +1 74 Lonely nights. You learned to roll coins on your fingers. DEX +1
25 Housekeeper is a horrible cook. Manage to survive. CON +1 75 Research trip to ancient ruins. Pack animals died. STR +1
26 Like to gamble. Lose regularly. Have to fight off bookies. STR +1 76 One month at a local monastery. CON +1
27 Hang head wizard's hat on flagpole. DEX +1 77 Sat in on inquest jury. WIS +1
28 Overcome your shyness and become more outgoing. CHA +1 78 Professor killed by bugbear. Visiting elven scholar fills in. INT +1
29 Scale the highest peak in the area in your free time. CON +1 79 Tamed Elementals for basics course. Rock drop on foot. WIS +2, DEX -1
30 Wizard creates spell to build muscle. He gets rich. You get stronger. STR +1 80 Conjured a devil, just to see if it actually worked. INT +1
31 Discovered extinct primitive cult. Wrote book on their lore. INT +2 81 Delivered a baby during a terrible storm. WIS +1
32 Close relative was a healer. Taught you many things. WIS +1 82 Translated ancient scroll into common. INT +1
33 Solved riddle that barred entry to an ancient tomb. INT +1 83 Passed off transmuted copper as silver. Made 300GP. CHA +1
34 Helped clear out an undead problem at local cemetery. WIS +1 84 Snuck into class late every day for a month. DEX +1
35 Alchemy experiment goes awry. You get faster. DEX +1, INT -1 85 Survived childhood sickness. CON +1
36 Crashed the Dean's Dinner uninvited. Blended in. CHA +1 86 Saved fellow student from a collapsing bookshelf. STR +1
37 Whittled small wooden animals for local children. DEX +1 87 Pranked the University with an illusionary Dragon. INT +1
38 Learned to dance. CHA +1 88 Lived with primitive people learned from their medicine man. WIS +1
39 Field trip to other planes of existence. INT +1 89 Enchanted a kobold that followed you around for a week. INT +1
40 Campus hit by worst ice storm in history. DEX +1 90 Blessed words from your deity fall on your ears. WIS +2
41 Preformed autopsies on several condemned prisoners. WIS +2 91 Disillusioned with academic system. Move to Life Experience Table.
42 Learned to play the flute. CHA +1 92 Talked your way into a class you were not qualified for. CHA +1
43 Spell backfires. Fries your frontal lobe. INT -1 93 Fireball training! DEX +1
44 Rebound books for extra money. DEX +1 94 Worked special effects for local theater. CHA +1
45 Sampling tree bark run into Treant. Exchange knowledge. WIS +1 95 Four weeks with a Master Diviner. INT +1
46 Study Astronomy and the movements of the moon. INT +1 96 One month crafting Holy Symbols. WIS +1
47 Identified illness spreading through village. WIS +1 97 Locked yourself out of your own room. Picked the lock. DEX +1
48 Edited Professor's newly written book. INT +2 98 Climbed a cliff face to retrieve rare feather for spell. STR +1
49 One month tutelage under bad teacher. WIS -1 99 Completed a four week fast. CON +1
50 Mapped nearby river. INT +1 100 War breaks out. Drafted in military service. Move to Military Table.
"""

life_experience_table = """
1 Arrested. Sentence, infantry service. Move to Military Table. 51 Failed to pay debts. Leg broken. DEX -1
2 Dusty hovel you moved into had three books left behind. INT +1 52 Born leader. CHA +1
3 Tracked an animal for two weeks across snow and ice. CON +1 53 Your people are renowned for their archery skills. DEX +1
4 Dock worker. Loading and unloading. STR +1 54 You are a liar. You lie all the time. You could be lying right now. CHA +1
5 Learned to juggle. DEX +1 55 Captured live birds and sold them to travelers. DEX +1
6 Born with great looks. CHA +1 56 Body odor is unbearable. CHA -1
7 Stable work. Worked with many horses. WIS +1 57 On a dare, you did find a needle in a haystack. WIS +1
8 Arrested. One month hard labor. STR +1 58 Crossed a 300 foot rope bridge in a wind storm. DEX +2
9 Studied the philosophy of nothingness. WIS +1 59 You made a chunk of money arm wrestling in pubs. STR +1
10 Scholarship awarded. Enroll at local Academy. Move to Academic Table. 60 Youngest person elected to the Towne Council. CHA +1
11 Sold snake oil until the Towne Council shut you down. CHA +1 61 Studied under an enlightened monk. WIS +1
12 Made ends meet by doing street magic. Sleight of hand. DEX +2 62 Worked as a guard. Tied up prisoners. DEX +1
13 Owned a pub for a month. CHA +1 63 Manual Labor job. STR +1, DEX -1
14 Worked the shell game in a large city. DEX +1 64 Chopped wood for days at a time after your last breakup. STR +1
15 Survived a fever that killed many. CON +1 65 Survived in the wild for a month after a natural disaster. WIS +1
16 Sailed a ship using the stars for guidance. INT +1 66 Part time blacksmith. STR +1
17 Family home attacked by bandits. Rendered first aid to those injured. WIS +1 67 Escaped a prison after you were wrongly arrested. DEX +1
18 Built a log cabin by hand. STR +1 68 You are a talented Tenor. CHA +1
19 Natural with a musical instrument. Not fond of reading. CHA +2, INT -1 69 Spent some time as a snaked handler. DEX +1
20 Traveled with a carnival. Worked with the knife thrower. DEX +1 70 Gamble frequently. Great bluffer. CHA +2
21 Played in a band. CHA +1 71 You have an affinity for the law, but have never gone to school. INT +1
22 Escaped capture when guards were out to arrest you. DEX +1 72 When you were born, you were left to die. You survived. CON +1
23 Come from a noble background. CHA +1 73 Lived with a native tribe for a while. Learned to forage berries. WIS +1
24 Avid bird hunter. Crossbow is weapon of choice. DEX +1 74 Competed in a strong man event. Came in third. STR +1
25 Survived merchant ship sinking. CON +1 75 You are one of those annoying people full of trivia. INT +1
26 Worked as an appraiser for several clients. INT +1 76 Tortured to reveal a partner's location. CON +1
27 Part-time grave digging work. STR +1 77 Circus work. Tight-rope walker. DEX +1
28 Discovered a cave network behind a waterfall. WIS +1 78 Worked undercover as a spy for rival nobles. CHA +1
29 Farm job pays the bills. CON +1 79 Make a meager living picking pockets. DEX +2, CON -1
30 Got drunk and passed out on a stack of books. INT +1 80 You are a rabble rouser. You alone have started five riots. CHA +1
31 Have a natural talent for negotiating. CHA +2 81 Apprenticed as a sculptor. DEX +1
32 Grew up as an orphan on the streets. DEX +1 82 You are wonderful with children. They love you. CHA +1
33 You were groomed to be the village story teller. CHA +1 83 Your people were persecuted. The clergy hid and cared for you. WIS +1
34 You are greedy. If you see something you want, you just lift it. DEX +1 84 Carried a broken wagon four miles to the nearest town. STR +1
35 Cut across the face in a bar fight. CHA -1, CON +1 85 You survived a demonic possession as a child. CON +1
36 You track and hunted creatures opposed to your morality. WIS +1 86 You collect rare books. INT +1
37 Your village was attack when you were a child. You harbor urges for revenge. STR +1 87 Self-taught on the flute. CHA +1
38 After a string of defeats, you learned humility. WIS +1 88 You have great hand-eye coordination. Enjoy sport. DEX +1
39 You are a seducer. You manipulate the opposite sex with your charm. CHA +1 89 You know every pub song ever sung. CHA +1
40 Trained as the village bell ringer. STR +1 90 Worked the ropes on a ship for a month. DEX +2
41 Allowed to train with monks. DEX +2 91 Local Militia offer signing bonus. Move to Military Table.
42 You murdered someone over something minor. Feel guilty. WIS +1 92 Attended to the injured after earthquake. WIS +1
43 Voice cracks every time you try to speak. CHA -1 93 Manned the gong for the royal court. STR +1
44 You swam a great lake near your hometown. STR +1 94 Forgave an enemy on his death bed. WIS +1
45 Your people have a tradition of walking on hot coals. DEX +1 95 Leader of a highway bandit crew. CHA +1
46 Supervised a trade caravan on a long dangerous trek. CHA +1 96 Worked as the town animal catcher. DEX +1
47 Assisted a clock maker for many weeks. DEX +1 97 Construction work at a nearby Keep. STR +1
48 Eloquent speaker with a huge vocabulary. CHA +1 98 Traded in scrolls for a brief time. INT +1
49 Suffered hand injury while loading crates. DEX -1 99 You can hold your breath for five minutes. CON +1
50 Worked as a bouncer at a local pub. CHA +1 100 A Higher Power calls. Move to Academic Table.
"""

military_table = """
1 Insubordination. Relieved from duty. Move to Life Experience Table. 51 Punctured a lung in a battle. CON -1
2 Studied historical battles. INT +1 52 Captured and used as slave labor. STR +1
3 Mediated military disputes between soldiers. WIS +1 53 Completed a 300 mile crusade in the name of King and God. CON +1
4 Joined the Archer corps. DEX +1 54 Forage patrol. Looted a ten mile swath along the main line. STR +1
5 Marched barefoot for twenty miles. CON +1 55 Rode out a famine while pinned down at a fort. CON +1
6 In charge of placing the horses in armor. STR +1 56 Tore shoulder muscle in a duel. STR -1
7 Lead your men on an assault. CHA +1 57 Conscripted peasants for large offensive. CHA +1
8 Dodged every arrow during an ambush. DEX +1 58 Stranded on deserted island after shipwreck. CON +2
9 Rallied your troops when the odds were against you. CHA +1 59 Repaired saddles for the mounted division. DEX +1
10 Master Tactician. Promoted to Officer School. Move to Academic Table. 60 Cut timber and helped build a barracks. STR +1
11 Built a bridge during a campaign against enemy forces. STR +1 61 Negotiated a surrender from an enemy. CHA +1
12 Channeled your inner rage. CON +2 62 Received forty lashes for punching an officer. CON +1
13 Weapon training with heavy arms. STR +1 63 Talked your way out of Physical Training. CHA +1, STR -1
14 Served on a ship. Learned to drink like a sailor. CON +1 64 Learned dozens of knots while working on ship. DEX +1
15 Assistant to the General. Worked with battle maps. WIS +1 65 Swore vengeance against a foe that wiped out your company. CHA +1
16 Integrated magic into an assault. INT +1 66 Functioned as a sniper. DEX +1
17 Lead a mounted division. CHA +1 67 Stood guard duty in the worst weather possible. CON +1
18 Crossbow practice. Placed first. DEX +1 68 Lifted a horse off a comrade that was cut down. STR +1
19 Wrestled bears to show off and prove strength. STR +1, INT -1 69 You often boxed fellow soldiers for cash and rations. CON +1
20 Bitter winter during a tour of duty. CON +1 70 Was assigned oar duty on a warship. STR +2
21 Naturally athletic. STR +1 71 Calculated trajectories for siege weapons. INT +1
22 Jungle mission. Withstood thousands of insect bites. CON +1 72 Served as a scout. WIS +1
23 Deck Duty on a Navy Ship. Riggings and sails. STR +1 73 Inspired a dying soldier. CHA +1
24 Food poisoning spreads through camp. Your mom cooks worse. CON +1 74 Assassinated a commander of enemy troops with one shot. DEX +1
25 Successfully tracked enemy troops through mountains. WIS +1 75 Created a logistical system to supply the main army. INT +1
26 Planned a perfect ambush. Lost no men. INT +1 76 Helped out in the medical camp. Tended to the injured. WIS +1
27 Infiltrated enemy headquarters. Extracted information. DEX +1 77 Had an arrow pushed through and snapped off. CON +1
28 Turned a double agent. CHA +1 78 Nine kills during hand to hand combat. STR +1
29 Identified a spy in your ranks. WIS +1 79 Arm was caught in the main ropes of a war machine. CON +2, DEX -1
30 Got a ship to port after the death of your captain. INT +1 80 Appointed executioner of prisoners. Beheading with an axe. STR +1
31 Loaded the catapult during a siege. STR +2 81 Endured hot iron branding. CON +1
32 Survived several battles with numerous injuries. CON +1 82 Holy words inspired your bravery and made you stronger. STR +1
33 Carried two injured soldiers to safety. STR +1 83 Impressed the General and received a promotion. CHA +1
34 Ate the heart of your enemy. CON +1 84 Snuck onto an enemy ship and sabotaged it. DEX +1
35 Fought a giant scorpion. Only got stung once. DEX +1, CON -1 85 Saw a deity on the battlefield. WIS +1
36 Instigated a successful mutiny. CHA +1 86 Managed supply lines for a battalion. INT +1
37 Worked the crow's nest during rough seas. DEX +1 87 Carried your regimental colors. STR +1
38 Appointed liaison for an occupied town. CHA +1 88 Went without sleep for days while observing enemy positions. CON +1
39 Hoisted up the anchor on a ship. STR +1 89 Cranked back a ballista by yourself. STR +1
40 Deserted a battle and escaped while being pursued. DEX +1 90 Your whole body is tattooed. CON +2
41 Worked the war-forge making weapons. CON +2 91 Angered a group of officers. Discharged. Move to Life Experience Table.
42 Gambled with the officers. Took them for two months wages. CHA +1 92 Bestowed honors of bravery by the King of the realm. CHA +1
43 Kicked by a Calvary horse. In coma for a month. STR -1 93 Ran a message through the battlefield to the Lord in charge. DEX +1
44 Screwed up. Got put on potato peeling duty. DEX +1 94 Honorably disarmed and faced an enemy with fists. CHA +1
45 Stuck out a one month siege of your keep. CON +1 95 Fought off a pack of war dog while defending a fallen soldier. STR +1
46 Buried the fallen. STR +1 96 Continued fighting while you were on fire. CON +1
47 Had four arrows removed from your leg. CON +1 97 Disarmed an enemy trap. DEX +1
48 Worked the battering ram. STR +1 98 Made money dealing in contraband. Economic of war. INT +1
49 Contracted disease while serving abroad. CON -1 99 Saw the true face of evil and swore to destroy it. WIS +1
50 Dug latrines for entire company. STR +1 100 Military cuts. The brightest are sent to College. Move to Academic Table.
"""


def parse_line(text):
    m = re.match(r"(.*) Move to (.*) Table.", text)
    if m:
        return ["{} Move to {} Table.".format(m.group(1), m.group(2)), {"Table": m.group(2)}]
    m = re.match(r"(.*) ([A-Z]{3} .*)", text)
    d = dict([(m.group(1), int(m.group(2))) for m in re.finditer(r"([A-Z]{3}) ([\-+]\d)", m.group(2))])
    return [text, d]


def parse_table(table):
    top_list = []
    bottom_list = []

    for i, line in enumerate(table.strip("\n").split("\n")):
        print(line)
        m = re.match(r"{} (.*) {} (.*)".format(i + 1, i + 51), line)
        top_list.append([i + 1] + parse_line(m.group(1)))
        bottom_list.append([i + 51] + parse_line(m.group(2)))

    total_list = top_list + bottom_list
    print("[")
    for item in total_list:
        print("    {}{}".format(tuple(item), "" if item[0] == 100 else ","))
    print("]\n")

    return total_list


tables = {
    "Academic": parse_table(academic_table),
    "Life Experience": parse_table(life_experience_table),
    "Military": parse_table(military_table)
}

# for name, table in tables.items():
#     print(name)
#     for item in table:
#         print("    {}".format((item[0], item[1], (item[2], item[3]))))
#     print("")

path = random.choice(tables.keys())
print("Starting Path: {}\n".format(path))
current_table = tables[path]

stats = OrderedDict([("STR", 10), ("DEX", 10), ("CON", 10), ("INT", 10), ("WIS", 10), ("CHA", 10)])

# def transpose(roll):
#     if roll == 100:
#         return 100
#     if i < 10:
#         return i * 10
#     return int(str(roll)[::-1])


i = 12
available_rolls = range(1, 101)

while i > 0:
    result = random.choice(current_table)
    current_table.remove(result)
    print("{:<3} {}".format(result[0], result[1]))
    d = result[2]
    if "Table" in d:
        path = d["Table"]
        current_table = tables[path]
    else:
        for stat, mod in d.items():
            stats[stat] += mod
        i -= 1

print("")
print(", ".join(["{} {:+d}".format(stat, mod) for stat, mod in stats.items()]))
