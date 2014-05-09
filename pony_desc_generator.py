import re
#http://www.seventhsanctum.com/generate.php?Genname=mlpony

def with_index(seq):
    for i in xrange(len(seq)):
        yield i, seq[i]

def replace_all(seq, obj, replacement):
    for i, elem in with_index(seq):
        if elem == obj:
            seq[i] = replacement

def remove_all(seq, obj):
    return filter (lambda a: a != obj, seq)



lines = """
This elegant female pony is a unicorn who is unfriendly, air-headed, and dishonorable. Her coat is orange. She has a mane that reminds you of a tangled bush. Her eyes are gunmetal-gray. Her mark is two rakes.

This ungainly male pony is a unicorn who is inquisitive, studious, and humble. His coat is orange. He has a mane that reminds you of a drifting cloud. His eyes are orange. His mark is a mahjong tile.

This lean male pony is an earth pony who is neurotic, confused, and reliable. His coat is blue and violet. He has a mane that is gray, and it reminds you of an elaborate sculpture. His eyes are brown. His mark is a sword.

This lean female pony is an earth pony who is worldwise and kind. Her coat is brown. She has a mane that is orange, and it reminds you of a comet's trail. Her deep-set eyes are violet. Her mark is a lime.

This small colt is a pegasus who is witty. His coat is plum-colored. He has a mane that is green, and it reminds you of a shark's fin. His wide eyes are chalk-white. His mark is a bag.

This statusesque colt is an earth pony who is loyal, bookish, and selfless. His coat is moss green. He has a mane that is yellow, and it reminds you of a gush of water. His hooded eyes are green. His mark is a cake.

This bulky female pony is a pegasus who is smooth-talking and moral. Her coat is grass-green. She has an extremely long mane that is blue. Her eyes are magenta. Her mark is three clothespins.

This ungainly female pony is an earth pony who is unintelligent and boastful. Her coat is black. She has an unstyled mane that is gray. Her deep-set eyes are gray. Her mark is a lamp.

This ungainly filly is an earth pony who is conformist and honorable. Her coat is coffee-colored. She has an unusually short, sloppily-styled mane that is yellow. Her slitted eyes are lemon-yellow. Her mark is an acupuncture needle.

This pudgy male pony is a pegasus who is unimaginative and self-aggrandizing. His coat is azure. He has a mane that is brown, and it reminds you of a flowing cape. His eyes are brown. His mark is an owl. 

This small stallion is an earth pony who is smooth-talking and selfless. His coat is red shading into white. He has a luxurious mane. His almond-shaped eyes are cream-colored. His mark is a loom and a storm cloud. 
 
This gangly filly is an earth pony who is organized and smooth-talking. Her coat is bone-white. She has an unusually short, curly mane. Her eyes are peach-colored. Her mark is four cranes. 
 
This ungainly stallion is an earth pony who is sloppy and arrogant. His coat is black. He has an elaborately-styled mane. His eyes are coffee-colored. His mark is a crutch and a piece of sushi. 
 
This elegant female pony is a unicorn who is calm and cooperative. Her coat is charcoal-colored. She has an unusually short mane that is orange. Her deep-set eyes are black. Her mark is two worms. 
 
This large colt is an earth pony who is apathetic, uneducated, and humble. His coat is blue. He has a mane that is yellow, and it reminds you of a pennant blowing in the wind. His eyes are amethyst. His mark is four stretchers. 
 
This bulky female pony is a unicorn who is unintelligent and nice. Her coat is chocolate-colored. She has a mane that is yellow, and it reminds you of a waterfall. Her eyes are black. Her mark is an anvil. 
 
This elegant colt is an earth pony who is sloppy and witty. His coat is orange. He has a mane that is black, and it reminds you of a tangled bush. His almond-shaped eyes are white. His mark is a piece of sushi. 
 
This stubby-legged male pony is an earth pony who is aloof. His coat is orange. He has a mane that is black, and it reminds you of a cascading waterfall. His eyes are gray. His mark is four apple cores. 
 
This statusesque male pony is a pegasus who is imaginative and clever. His coat is chalk-white. He has an extremely long mane that is gray and white. His eyes are green. His mark is three lathes. 
 
This bulky colt is a pegasus who is wise. His coat is blue. He has a mane that is purple, and it reminds you of a pile of shredded paper. His eyes are pine-green. His mark is a record player. 

This bulky stallion is a pegasus who is witty and manipulative. His coat is red. He has a mane that is black, and it reminds you of the petals of a flower. His eyes are beige. His mark is a torch.

This stubby-legged female pony is an earth pony who is withdrawn and scatterbrained. Her coat is purple. She has a mane that is orange, and it reminds you of the aurora borealis. Her deep-set eyes are green. Her mark is a drum.

This gangly filly is a unicorn who is bold, smooth-talking, and unethical. Her coat is night-black. She has an unusually short mane that is gray. Her slitted eyes are blue. Her mark is three nuts.

This ungainly female pony is an earth pony who is fashionable, irrational, and mean-spirited. Her coat is milky-white. She has an unusually short mane. Her eyes are black. Her mark is an egg.

This long-legged filly is an earth pony who is uneducated. Her coat is white with brown patches. She has a straight mane that is black. Her deep-set eyes are turquoise. Her mark is three laundry baskets.

This elegant stallion is an earth pony who is temperamental and greedy. His coat is burgandy. He has an extremely long, straight mane. His eyes are black. His mark is a fan.

This statusesque female pony is an earth pony who is angry. Her coat is black. She has a long mane that is red. Her eyes are white. Her mark is a comb.

This small filly is a unicorn who is slow-witted. Her coat is emerald. She has a short, unstyled mane that is orange and white. Her almond-shaped eyes are green. Her mark is an angry face.

This small female pony is an earth pony who is peace-loving. Her coat is red and blue. She has a straight mane that is violet and orange. Her wide eyes are turquoise. Her mark is a set of crosshairs and a mushroom.

This gangly female pony is an earth pony who is distractable and honorable. Her coat is turquoise. She has a mane that is gray, and it reminds you of a burning fire. Her almond-shaped eyes are blue. Her mark is a jolly roger. 

This statusesque filly is an earth pony who is arrogant. Her coat is purple. She has a mane that is blue, and it reminds you of a wave of water. Her eyes are obsidian. Her mark is a wisp of smoke.

This large female pony is an earth pony who is absent-minded and peace-loving. Her coat is black. She has a mane that is brown and white, and it reminds you of a wave of water. Her eyes are orange. Her mark is two disk.

This ungainly stallion is an earth pony who is biased and contemplative. His coat is violet. He has a mane that is gray, and it reminds you of a fluttering flag. His eyes are red. His mark is a cart.

This muscular colt is an earth pony who is neat. His coat is gunmetal-gray. He has a mane that is black, and it reminds you of a waterfall. His eyes are lemon-yellow. His mark is a watermelon.

This pudgy female pony is an earth pony who is disillusioned and kind. Her coat is ash-gray. She has a mane that reminds you of a waterfall. Her wide eyes are sapphire. Her mark is a jack-o-lantern.

This gangly male pony is a pegasus who is fashionable. His coat is ash-gray. He has a mane that is yellow, and it reminds you of an overused mop. His hooded eyes are black. His mark is four darts.

This gangly female pony is a pegasus who is logical. Her coat is white. She has a mane that is black, and it reminds you of a rocky outcropping. Her eyes are orange. Her mark is a glass.

This large male pony is a pegasus who is antisocial and ignorant. His coat is peach-colored. He has an unusually short, elaborately-styled mane that is black and white. His eyes are coffee-colored. His mark is a backpack.

This elegant female pony is an earth pony who is paranoid, absent-minded, and ethical. Her coat is white and red. She has a mane that is black, and it reminds you of a flower's petals. Her slitted eyes are green. Her mark is a candy.

This statusesque female pony is an earth pony who is composed. Her coat is gray. She has an unstyled mane that is blue and green. Her narrow eyes are coffee-colored. Her mark is a watermelon. 

This elegant colt is an earth pony who is inquisitive and slow-witted. His coat is blue. He has an unusually short mane that is brown. His eyes are orange. His mark is a dollar sign.

This muscular male pony is an earth pony who is playful, clever, and moral. His coat is apricot-colored. He has a mane that is black, and it reminds you of the rays of the sun. His eyes are chocolate-colored. His mark is a doctor's bag.

This gangly male pony is an earth pony who is distractable, unwise, and honorable. His coat is turquoise. He has an extremely long, elaborately-styled mane that is violet and green. His eyes are white. His mark is a rook.

This gangly filly is an earth pony who is aggrivated, unwise, and honorable. Her coat is orange. She has a mane that is red and brown, and it reminds you of a pile of leaves. Her eyes are red. Her mark is three zodiac signs.

This bulky female pony is an earth pony who is brash, bookish, and ethical. Her coat is red with violet spots. She has an unstyled mane that is blue. Her eyes are brown. Her mark is two gold bars.

This small female pony is an earth pony who is unprincipled. Her coat is brown. She has a mane that is green and blue, and it reminds you of an elaborate sculpture. Her hooded eyes are yellow. Her mark is a doctor's bag.

This elegant filly is a pegasus who is air-headed. Her coat is black. She has a short, curly mane that is white. Her eyes are brown. Her mark is a goblet and an ingot.

This bulky filly is a pegasus who is unreliable. Her coat is midnight black. She has an extremely long, curly mane that is red. Her eyes are gray. Her mark is a rose.

This muscular filly is an earth pony who is fashionable. Her coat is slate-gray. She has a mane that is white and violet, and it reminds you of a plume of smoke. Her eyes are green. Her mark is three arches.

This leanly-built colt is a pegasus who is withdrawn, worldwise, and altruistic. His coat is blue. He has a mane that is yellow, and it reminds you of a pile of shredded paper. His wide eyes are rose-red. His mark is two pieces of sushi.

This elegant female pony is an earth pony who is playful and egotistical. Her coat is jade-colored. She has a mane that reminds you of a shark's fin. Her eyes are moss green. Her mark is three anvils.

This small female pony is an earth pony who is tactful and focused. Her coat is green. She has a mane that is gray, and it reminds you of the aurora borealis. Her eyes are orange. Her mark is three trees.

This statusesque filly is a unicorn who is protective. Her coat is aquamarine. She has a mane that is violet and brown, and it reminds you of a burning fire. Her eyes are green. Her mark is a cross.

This stubby-legged colt is an earth pony who is flirty, unintelligent, and mean-spirited. His coat is orange. He has a mane that reminds you of a pile of shredded paper. His eyes are apricot-colored. His mark is a cross and a guitar.

This muscular stallion is an earth pony who is industrious. His coat is black. He has an extremely long mane. His hooded eyes are red. His mark is a sickle.

This small female pony is an earth pony who is confused. Her coat is chestnut. She has a mane that reminds you of the aurora borealis. Her large eyes are brown. Her mark is a diamond.

This lean female pony is an earth pony who is smooth-talking and moral. Her coat is orange with violet patches. She has an unusually short mane that is orange. Her slitted eyes are indigo. Her mark is a square.

This gangly male pony is a unicorn who is philosophical and ethical. His coat is apple-green. He has a long mane that is black. His almond-shaped eyes are green. His mark is a scooter.

This ungainly male pony is a pegasus who is generous. His coat is orange. He has a mane that is brown, and it reminds you of an elaborate sculpture. His slanted eyes are umber. His mark is a slice of pie.

This lean female pony is an earth pony who is honest. Her coat is green. She has a mane that is yellow, and it reminds you of a pile of shredded paper. Her eyes are gray. Her mark is a cat.

This bulky stallion is an earth pony who is obsessive and selfless. His coat is emerald. He has a long mane. His narrow eyes are violet. His mark is three pots.

This statusesque male pony is an earth pony who is absent-minded. His coat is teal. He has a long, luxurious mane that is black. His large eyes are green. His mark is a sheet of music.

This ungainly male pony is an earth pony who is courageous and hard-working. His coat is orange. He has an extremely long, unstyled mane that is red. His almond-shaped eyes are orange. His mark is an anvil.

This elegant stallion is a unicorn who is scatterbrained. His coat is yellow. He has a long mane that is brown. His slitted eyes are red. His mark is a sun.

This elegant filly is an earth pony who is scatterbrained. Her coat is lemon-yellow. She has a long, luxurious mane. Her eyes are chocolate-colored. Her mark is a knitting needle.

This elegant stallion is a pegasus who is alienated. His coat is gunmetal-gray. He has a long mane that is white and black. His eyes are gold. His mark is a piece of cheese.

This bulky female pony is an earth pony who is withdrawn, unintelligent, and cooperative. Her coat is charcoal-colored. She has an unusually short, elaborately-styled mane. Her eyes are purple. Her mark is a banana peel.

This elegant female pony is a pegasus who is ambitious and witty. Her coat is ebony. She has a mane that reminds you of a comet's trail. Her wide eyes are green. Her mark is three bandages.

This bulky female pony is a unicorn who is smart and mean-spirited. Her coat is purple. She has a mane that is green, and it reminds you of a flowing cape. Her eyes are peach-colored. Her mark is a gate.

This lean male pony is a pegasus who is mysterious, smart, and altruistic. His coat is olive-green. He has a mane that is violet, and it reminds you of a flame. His large eyes are smoke-gray. His mark is a deck of cards.

This pudgy male pony is an earth pony who is arrogant, wise, and gentle. His coat is teal. He has an unstyled mane. His eyes are cream-colored. His mark is a knot.

This gangly female pony is a pegasus who is self-aggrandizing. Her coat is orange. She has a mane that is black, and it reminds you of a shark's fin. Her eyes are violet. Her mark is a butterfly.

This bulky stallion is a pegasus who is biased, incoherent, and mean-spirited. His coat is indigo. He has an unusually short, wavy mane that is yellow. His hooded eyes are gray. His mark is a mirror.

This lean male pony is an earth pony who is fashionable, ignorant, and humble. His coat is apricot-colored. He has a short, elaborately-styled mane that is black. His eyes are black. His mark is a staff.

This stubby-legged male pony is an earth pony who is down-to-earth, unintelligent, and humble. His coat is red. He has a long mane that is yellow. His deep-set eyes are amethyst. His mark is a slug.

This small male pony is an earth pony who is uncultured and unethical. His coat is yellow. He has a mane that is red, and it reminds you of a shark's fin. His droopy eyes are rust-colored. His mark is two earthworms.

This statusesque colt is an earth pony who is confident, incoherent, and nihlistic. His coat is aquamarine. He has an unusually short mane. His eyes are yellow. His mark is four ankhs.

This leanly-built colt is an earth pony who is withdrawn, smart, and boastful. His coat is brown. He has a mane that reminds you of a drifting cloud. His slitted eyes are vermillion. His mark is three scooters.

This bulky female pony is a unicorn who is slow-witted and selfless. Her coat is coffee-colored. She has a mane that is red and orange, and it reminds you of a porcupine's quills. Her eyes are yellow. Her mark is a swimming pool.

This long-legged male pony is a pegasus who is obedient. His coat is yellow and black. He has a short, wavy mane that is green. His eyes are green. His mark is a chandelier.

This long-legged filly is an earth pony who is playful and cunning. Her coat is chocolate-colored. She has a mane that is gray, and it reminds you of a puffy dandelion. Her large eyes are tangerine-colored. Her mark is a tree and a mandolin.

This bulky colt is a unicorn who is obedient, smart, and manipulative. His coat is blue. He has a short, spiky mane that is gray. His eyes are yellow. His mark is a basket of laundry and a disc.

This bulky colt is a unicorn who is fashionable, wise, and dishonorable. His coat is ivory. He has a curly mane that is gray and brown. His eyes are orange. His mark is a starburst.

This stubby-legged stallion is an earth pony who is unprincipled. His coat is ash-gray. He has a curly mane. His eyes are cobalt-blue. His mark is a candy.

This long-legged female pony is an earth pony who is inquisitive and smooth-talking. Her coat is white. She has a mane that reminds you of a burning fire. Her almond-shaped eyes are brown. Her mark is a balloon.

This elegant filly is an earth pony who is illogical and humble. Her coat is chestnut. She has a mane that reminds you of a flowing stream. Her eyes are red. Her mark is a harp.

This gangly filly is a unicorn who is organized and educated. Her coat is apricot-colored. She has a mane that reminds you of a flower's petals. Her eyes are green. Her mark is a satchel.

This elegant female pony is an earth pony who is boring and nihlistic. Her coat is chestnut. She has a mane that reminds you of a gush of water. Her eyes are purple. Her mark is a disc.

This statusesque female pony is an earth pony who is fashionable, clever, and kind. Her coat is brown. She has a mane that reminds you of a flame. Her eyes are purple. Her mark is a harp.

This stubby-legged filly is a unicorn who is comitted and unreliable. Her coat is white and red. She has a mane that is yellow, and it reminds you of a comet's trail. Her round eyes are red. Her mark is three scythes.

This large filly is a pegasus who is laid-back, unintelligent, and humble. Her coat is midnight black. She has a mane that is green, and it reminds you of the petals of a flower. Her eyes are ash-gray. Her mark is a bean.

This stubby-legged female pony is a pegasus who is focused and gentle. Her coat is ebony. She has a mane that is blue, and it reminds you of the rays of the sun. Her almond-shaped eyes are white. Her mark is two hatchets.

This small filly is an earth pony who is unintelligent. Her coat is yellow with brown patches. She has a mane that is orange, and it reminds you of a rocky outcropping. Her eyes are brown. Her mark is three hatchets.

This pudgy female pony is an earth pony who is bouncy, air-headed, and gentle. Her coat is white. She has an unstyled mane that is black and red. Her hooded eyes are slate-gray. Her mark is a mop.

This small filly is an earth pony who is playful and altruistic. Her coat is blue. She has a luxurious mane that is violet and gray. Her eyes are lavender. Her mark is a globe.

This pudgy female pony is an earth pony who is loyal. Her coat is mauve. She has a mane that reminds you of a comet's trail. Her narrow eyes are mauve. Her mark is a flask.

This large female pony is an earth pony who is arrogant and caring. Her coat is green. She has a long mane. Her eyes are brown. Her mark is a fang and a bowl.

This large filly is a pegasus who is unintelligent and caring. Her coat is gray. She has a luxurious mane. Her eyes are beige. Her mark is a ruby.

This ungainly colt is a pegasus who is pragmatic, studious, and envious. His coat is sand-colored. He has a mane that is black and blue, and it reminds you of a tangled bush. His narrow eyes are sand-colored. His mark is a lasso.

This leanly-built male pony is an earth pony who is loyal and unreliable. His coat is red. He has a mane that is yellow and orange, and it reminds you of a comet's trail. His eyes are tangerine-colored. His mark is three ingots.

This long-legged colt is an earth pony who is charmismatic and absent-minded. His coat is black. He has a long, unstyled mane that is white. His eyes are peach-colored. His mark is two pillows.

This gangly colt is an earth pony who is laid-back, studious, and honest. His coat is blue. He has a mane that is red, and it reminds you of a flame. His eyes are teal. His mark is a lime.

This ungainly female pony is a unicorn who is incoherent and gentle. Her coat is blue. She has a mane that is black and yellow, and it reminds you of a drifting cloud. Her eyes are white. Her mark is an ear of corn.

This lean male pony is a unicorn who is romantic and manipulative. His coat is black. He has a short mane that is orange and black. His hooded eyes are white. His mark is an explosion.

This long-legged female pony is a unicorn who is focused and self-aggrandizing. Her coat is chocolate-colored. She has a mane that is red, and it reminds you of a pile of shredded paper. Her eyes are coffee-colored. Her mark is a chart.

This elegant stallion is an earth pony who is pragmatic and scatterbrained. His coat is brick-red. He has an unstyled mane that is yellow. His beady eyes are chocolate-colored. His mark is a zodiac sign.

This muscular female pony is an earth pony who is neat, focused, and egotistical. Her coat is black. She has a mane that is red, and it reminds you of a cascading waterfall. Her round eyes are lemon-yellow. Her mark is a cookie.

This pudgy male pony is a unicorn who is mystical and hard-working. His coat is black. He has an unusually short, straight mane that is brown. His eyes are plum-colored. His mark is three lotus flowers.

This large male pony is an earth pony who is paranoid. His coat is yellow. He has a mane that is white, and it reminds you of a comet's trail. His deep-set eyes are green. His mark is three brushes.

This long-legged male pony is an earth pony who is ambitious, studious, and hypocritical. His coat is yellow and green. He has a mane that is white, and it reminds you of the petals of a flower. His almond-shaped eyes are gray. His mark is a pumpkin.

This muscular female pony is a pegasus who is caring. Her coat is green. She has a mane that is white and gray, and it reminds you of a tangled bush. Her slanted eyes are red. Her mark is a caduceus.

This stubby-legged female pony is an earth pony who is private. Her coat is blue. She has a short, spiky mane that is brown. Her round eyes are amber. Her mark is three socks.

This pudgy stallion is a pegasus who is cheerful and ignorant. His coat is white. He has a mane that reminds you of an overused mop. His eyes are burgandy. His mark is a sun.

This long-legged filly is a pegasus who is fun-loving, educated, and hard-working. Her coat is gray. She has a mane that is green, and it reminds you of a flame. Her eyes are chalk-white. Her mark is three bisctuits.

This stubby-legged female pony is an earth pony who is impolite, smooth-talking, and cooperative. Her coat is silver. She has a sloppily-styled mane that is purple and black. Her eyes are magenta. Her mark is a tornado.

This bulky male pony is an earth pony who is brave. His coat is gray. He has an extremely long mane that is orange and green. His eyes are blood-red. His mark is two oars.

This pudgy filly is an earth pony who is inquisitive, air-headed, and heroic. Her coat is white. She has a mane that is brown, and it reminds you of an elaborate sculpture. Her eyes are orange. Her mark is a tarot card.

This leanly-built colt is an earth pony who is fashionable, illogical, and cruel. His coat is gray. He has an extremely long, luxurious mane that is violet. His almond-shaped eyes are sand-colored. His mark is three watermelons.

This elegant filly is a unicorn who is impractical and honest. Her coat is gray. She has a mane that is orange, and it reminds you of a comet's trail. Her large eyes are orange. Her mark is a doctor's bag.

This lean stallion is an earth pony who is moral. His coat is blue with brown patches. He has a mane that is gray, and it reminds you of a pile of shredded paper. His hooded eyes are chestnut. His mark is a wave.

This pudgy female pony is an earth pony who is hypocritical. Her coat is orange and violet. She has a short mane that is green. Her beady eyes are yellow. Her mark is a bandage.

This large male pony is a unicorn who is nice. His coat is purple shading into black. He has a short mane that is yellow. His eyes are blood-red. His mark is a bird.

This pudgy stallion is a unicorn who is slow-witted and concieted. His coat is lavender. He has a mane that is red, and it reminds you of a flame. His slitted eyes are purple. His mark is a chevron.

This muscular stallion is a pegasus who is poised and smart. His coat is coffee-colored. He has a mane that is orange, and it reminds you of a drifting cloud. His hooded eyes are soot-black. His mark is three a parasol.

This leanly-built female pony is an earth pony who is ignorant. Her coat is yellow. She has a luxurious mane that is white. Her deep-set eyes are blue. Her mark is a biscuit.

This lean female pony is an earth pony who is philosophical. Her coat is violet with orange spots. She has a curly mane that is purple. Her slitted eyes are orange. Her mark is a dumbbell.

This statusesque filly is an earth pony who is uncultured, unintelligent, and lazy. Her coat is blood-red. She has an elaborately-styled mane that is brown. Her eyes are violet. Her mark is three bisctuits.

This small male pony is an earth pony who is uneducated. His coat is yellow. He has an unusually short, curly mane. His eyes are gray. His mark is two cans.

This muscular colt is an earth pony who is dishonest. His coat is sapphire. He has a mane that is white and purple, and it reminds you of a trailing ribbon. His hooded eyes are chestnut. His mark is a scoreboard.

This small male pony is a pegasus who is cooperative. His coat is green. He has a mane that reminds you of a flowing stream. His eyes are violet. His mark is a pie.

This small female pony is a pegasus who is trusting. Her coat is red. She has a mane that is brown, and it reminds you of a tangled bush. Her eyes are vermillion. Her mark is a pan.

This muscular female pony is an earth pony who is contemplative and mean-spirited. Her coat is red with white spots. She has an unusually short, elaborately-styled mane that is red. Her droopy eyes are slate-gray. Her mark is a bar of soap.

This large female pony is an earth pony who is selfless. Her coat is apple-green. She has a mane that is orange and white, and it reminds you of a waterfall. Her beady eyes are silver. Her mark is a bottle of shampoo.

This large female pony is a pegasus who is withdrawn, unwise, and honest. Her coat is gold. She has a curly mane that is orange and purple. Her beady eyes are jet black. Her mark is a quill.

This elegant colt is an earth pony who is witty and selfless. His coat is alabaster. He has a mane that is blue and gray, and it reminds you of a drifting cloud. His eyes are gray. His mark is four mouths.

This ungainly male pony is a unicorn who is classy, cunning, and unethical. His coat is pine-green. He has a mane that is violet, and it reminds you of a cascading waterfall. His eyes are lavender. His mark is four wolves.

This gangly female pony is an earth pony who is composed and gluttonous. Her coat is plum-colored. She has a straight mane that is orange. Her slanted eyes are black. Her mark is two teeth.

This pudgy female pony is an earth pony who is air-headed and mean-spirited. Her coat is red. She has a sloppily-styled mane that is blue. Her eyes are brick-red. Her mark is a mop.

This large male pony is an earth pony who is clever and humble. His coat is amber. He has a mane that is blue, and it reminds you of a flame. His round eyes are moss green. His mark is a palm tree.

This muscular male pony is an earth pony who is clever and ethical. His coat is crimson. He has a mane that reminds you of a plume of smoke. His eyes are vermillion. His mark is a feather.

This statusesque female pony is an earth pony who is scatterbrained and dishonest. Her coat is amber. She has a mane that is green, and it reminds you of a porcupine's quills. Her eyes are ebony. Her mark is a bunch of letters.

This statusesque female pony is an earth pony who is witty. Her coat is blue shading into black. She has an unusually short mane that is yellow. Her hooded eyes are slate-gray. Her mark is two bones.

This small filly is an earth pony who is uninquisitive. Her coat is chestnut. She has an extremely long mane that is blue. Her eyes are chalk-white. Her mark is three poker chips.

This lean filly is an earth pony who is stressed, clever, and reliable. Her coat is blue. She has a mane that is red and gray, and it reminds you of a flame. Her eyes are ash-gray. Her mark is a mop.

This long-legged colt is a pegasus who is boring and concieted. His coat is gray. He has an unusually short mane that is yellow. His droopy eyes are amber. His mark is a bag of golf clubs.

This leanly-built colt is a unicorn who is boring. His coat is green. He has an unusually short, wavy mane that is black. His slanted eyes are blue. His mark is a fishing pole.

This muscular filly is an earth pony who is neurotic and honest. Her coat is coffee-colored. She has a curly mane that is green. Her eyes are green. Her mark is a knife and fork.

This lean female pony is an earth pony who is generous. Her coat is yellow. She has a mane that is gray, and it reminds you of a burning fire. Her deep-set eyes are night-black. Her mark is three crutches.

This long-legged female pony is a pegasus who is unintelligent and industrious. Her coat is white. She has a mane that is gray, and it reminds you of a gush of water. Her eyes are red. Her mark is four barber poles.

This elegant female pony is an earth pony who is neurotic, smart, and mean. Her coat is jade-colored. She has a short mane. Her eyes are chocolate-colored. Her mark is two hatchets.

This bulky colt is an earth pony who is unwise and nihlistic. His coat is gold. He has a mane that is blue and brown, and it reminds you of a rocky outcropping. His eyes are black. His mark is a zipper.

This lean stallion is a pegasus who is nurturing, irrational, and nice. His coat is midnight black. He has a mane that is gray, and it reminds you of a puffy dandelion. His eyes are red. His mark is a fork.

This leanly-built female pony is an earth pony who is practical, studious, and manipulative. Her coat is slate-gray. She has a mane that is red, and it reminds you of the petals of a flower. Her narrow eyes are charcoal-colored. Her mark is a fork.

This ungainly male pony is a pegasus who is messy. His coat is blue. He has a mane that is purple, and it reminds you of the rays of the sun. His beady eyes are gunmetal-gray. His mark is four ingots.

This long-legged female pony is an earth pony who is pompous and illogical. Her coat is brown shading into blue. She has an unstyled mane that is brown and black. Her eyes are gold. Her mark is a bubble.

This pudgy male pony is a pegasus who is reliable. His coat is bone-white. He has a sloppily-styled mane that is yellow and gray. His eyes are red. His mark is a bird.

This lean colt is an earth pony who is bitter, slow-witted, and hypocritical. His coat is gray. He has a mane that reminds you of a pile of shredded paper. His wide eyes are ivory. His mark is a zipper.

This stubby-legged male pony is a pegasus who is withdrawn and wise. His coat is emerald. He has a mane that reminds you of an overused mop. His eyes are amber. His mark is a bonfire.

This muscular male pony is an earth pony who is secretive and uneducated. His coat is sapphire. He has a mane that reminds you of a porcupine's quills. His eyes are night-black. His mark is four flying saucers.

This pudgy stallion is an earth pony who is playful and gluttonous. His coat is grass-green. He has a long mane that is gray. His eyes are ebony. His mark is a lathe.

This muscular female pony is an earth pony who is unintelligent and mean-spirited. Her coat is blue. She has a short mane. Her eyes are coffee-colored. Her mark is a brush.

This ungainly filly is an earth pony who is smart and cooperative. Her coat is cobalt-blue. She has a short, elaborately-styled mane that is black. Her slanted eyes are white. Her mark is a cat's-cradle.

This elegant female pony is an earth pony who is comitted. Her coat is beige. She has a mane that reminds you of a plume of smoke. Her large eyes are green. Her mark is four treasure chests.

This gangly filly is a unicorn who is slow-witted and vicious. Her coat is chestnut. She has a mane that is white and orange, and it reminds you of a wave of water. Her large eyes are slate-gray. Her mark is three a parasol.

This elegant colt is an earth pony who is nihlistic. His coat is red with violet spots. He has a long mane. His eyes are purple. His mark is two spades.

This elegant female pony is an earth pony who is unwise and gentle. Her coat is lemon-yellow. She has a mane that is green, and it reminds you of a flowing stream. Her eyes are brown. Her mark is a set of crosshairs.

This gangly male pony is an earth pony who is unintelligent and unethical. His coat is orange. He has a mane that is brown, and it reminds you of a flowing stream. His wide eyes are blue. His mark is four pairs of wings.

This elegant stallion is a unicorn who is cultured and ignorant. His coat is gold. He has a mane that is gray and orange, and it reminds you of a cascading waterfall. His eyes are sky-blue. His mark is three yin-yangs.

This small female pony is a unicorn who is cynical, contemplative, and humble. Her coat is royal purple. She has a mane that reminds you of a burning fire. Her eyes are chocolate-colored. Her mark is the zodiac.

This ungainly female pony is an earth pony who is eccentric and industrious. Her coat is moss green. She has a wavy mane that is gray. Her hooded eyes are beige. Her mark is a clover and a ship.

This ungainly female pony is a unicorn who is serene and philosophical. Her coat is gold. She has a straight mane. Her almond-shaped eyes are amethyst. Her mark is two flags.

This leanly-built male pony is a unicorn who is misguided and smart. His coat is sand-colored. He has a mane that is orange and white, and it reminds you of a cascading waterfall. His eyes are amber. His mark is a circle.

This muscular female pony is a pegasus who is smart. Her coat is lemon-yellow. She has a sloppily-styled mane that is white and red. Her hooded eyes are rose-red. Her mark is three rings.

This ungainly colt is an earth pony who is classy and selfless. His coat is blue. He has a long, wavy mane. His eyes are green. His mark is three spreadsheets.

This stubby-legged female pony is a pegasus who is incoherent. Her coat is brown. She has a short, luxurious mane that is white and orange. Her beady eyes are amber. Her mark is two lions.

This stubby-legged female pony is a pegasus who is classy and heroic. Her coat is orange shading into red. She has a short, wavy mane that is violet and orange. Her narrow eyes are apple-green. Her mark is three bones.

This large female pony is an earth pony who is fashionable and uneducated. Her coat is violet. She has a long, wavy mane that is white. Her eyes are olive-green. Her mark is a lime and an egg.

This large filly is an earth pony who is impractical. Her coat is apricot-colored. She has a short, wavy mane that is gray. Her eyes are smoke-gray. Her mark is a bomb.

This leanly-built colt is an earth pony who is mystical and honest. His coat is white with gray spots. He has a straight mane that is white. His hooded eyes are white. His mark is a bell.

This large female pony is a unicorn who is sarcastic and studious. Her coat is chestnut. She has an extremely long mane that is white. Her eyes are yellow. Her mark is a ringed planet.

This ungainly colt is a pegasus who is honest. His coat is blood-red. He has a mane that is orange, and it reminds you of a gush of water. His eyes are amber. His mark is a triangle and a pile of ash.

This pudgy colt is an earth pony who is worried and witty. His coat is black. He has a mane that is gray, and it reminds you of an overused mop. His large eyes are red. His mark is a drum.

This statusesque female pony is an earth pony who is practical, bookish, and unreliable. Her coat is rust-colored. She has a luxurious mane. Her droopy eyes are black. Her mark is a nest.

This statusesque female pony is an earth pony who is mean. Her coat is gray. She has a wavy mane that is red. Her slanted eyes are apricot-colored. Her mark is a carrot.

This ungainly filly is a pegasus who is incoherent and honest. Her coat is green. She has a long, unstyled mane that is white. Her eyes are yellow. Her mark is three brooms.

This stubby-legged female pony is a unicorn who is bold and wise. Her coat is lemon-yellow. She has a long, unstyled mane that is black. Her wide eyes are amber. Her mark is a pillow.

This muscular colt is an earth pony who is unwise and gentle. His coat is black. He has an extremely long mane that is brown and gray. His eyes are gold. His mark is three mousetraps.

This small female pony is an earth pony who is impractical, focused, and nice. Her coat is gray. She has a mane that is orange, and it reminds you of a rocky outcropping. Her large eyes are amber. Her mark is a bear.

This bulky colt is a pegasus who is organized, absent-minded, and humble. His coat is orange. He has a long, straight mane that is white. His wide eyes are black. His mark is three coins.

This bulky female pony is an earth pony who is unpredictable and vicious. Her coat is orange with green spots. She has a mane that is violet, and it reminds you of a cascading waterfall. Her slanted eyes are white. Her mark is a wolf. 
"""

reg = r"This (.*?) (male pony|female pony|colt|filly|stallion) is (.*?) who is (.*?)\. (His|Her) coat is (.*?)\. (He|She) has (a|an) (.*?)mane( that (is (.*?))?(, and it )?(reminds you of (.*?))?)?\. (His|Her) (.*?)eyes are (.*?)\. (His|Her) mark is (.*?)\."
cutie_reg = r"((a|an|two|three|four) )?(.*?)(s)?$"

##l = lines.split('\n')[53]
##r = re.search(reg,l)
##print r.groups()
adjectives = []
adjectives2 = []
coat_colors = []
mane_type = []
mane_color = []
mane_remind = []
eye_type = []
eye_color = []
cutie_mark = []
for i,x in enumerate(lines.split('\n')):
    r = re.search(reg,x)
    if r:
##        print r.groups()
        adjectives.append(r.group(1))
        temp = str(r.group(4))
        temp = temp.replace(', and ','|')
        temp = temp.replace(', ','|')
        temp = temp.replace(' and ','|')
        adjectives2 += temp.split('|')
        coat_colors.append(r.group(6))
        mane_type += r.group(9).replace(', ','|').split('|')
        if r.group(12):
            mane_color.append(r.group(12))
        if r.group(15):
            mane_remind.append(r.group(15))
        eye_type.append(r.group(17))
        eye_color.append(r.group(18))
        temp = str(r.group(20))
        temp = temp.replace(', and ','|')
        temp = temp.replace(', ','|')
        temp = temp.replace(' and ','|')
##        print repr(temp)
##        print repr(re.search(cutie_reg, temp))
##        print repr(re.search(cutie_reg, temp).groups())
        cutie_mark += [re.search(cutie_reg, x).group(3) for x in temp.split('|')]

cutie_mark_adds = "lantern|thunderbolt|smiling sun|leaky bucket|horseshoe|ladybug|crab|cog|gear|spring"
cutie_mark += cutie_mark_adds.split("|")

replace_all(adjectives2,"charmismatic","charismatic")
replace_all(adjectives2,"comitted","committed")

replace_all(cutie_mark,"wolve","wolf")
replace_all(cutie_mark,"sheet of music","musical note|")
replace_all(cutie_mark,"bunch of letter","letter pile")
replace_all(cutie_mark,"pairs of wing","feathery wing")
replace_all(cutie_mark,"bar of soap","soap bar")
replace_all(cutie_mark,"wisp of smoke","smoke wisp")
replace_all(cutie_mark,"bottle of shampoo","shampoo bottle")
replace_all(cutie_mark,"pieces of sushi","sushi roll")
replace_all(cutie_mark,"slice of pie","pie slice")
replace_all(cutie_mark,"bisctuit","biscuit")
replace_all(cutie_mark,"basket of laundry","laundry basket")
replace_all(cutie_mark,"piece of sushi","sushi roll")
replace_all(cutie_mark,"brushe","brush")
replace_all(cutie_mark,"ruby","gem")

cutie_mark = remove_all(cutie_mark,"ear of corn")
cutie_mark = remove_all(cutie_mark,"the zodiac")
cutie_mark = remove_all(cutie_mark,"set of crosshair")
cutie_mark = remove_all(cutie_mark,"bag of golf club")
cutie_mark = remove_all(cutie_mark,"teeth")


print "Adjectives: {0}".format("|".join(set(adjectives)))
print "Adjectives2: {0}".format("|".join(set(adjectives2)))
print "Coat colors: {0}".format("|".join(set(coat_colors)))
print "Mane types: {0}".format("|".join(set(mane_type)))
print "Mane colors: {0}".format("|".join(set(mane_color)))
print "Mane reminds: {0}".format("|".join(set(mane_remind)))
print "Eye types: {0}".format("|".join(set(eye_type)))
print "Eye colors: {0}".format("|".join(set(eye_color)))
print "Cutie marks: {0}".format("|".join(set(cutie_mark)))

##temp = 'mysterious, smart, and altruistic'
##temp = temp.replace(', and ','|')
##temp = temp.replace(', ','|')
##temp = temp.replace(' and ','|')
##print temp.split('|')
