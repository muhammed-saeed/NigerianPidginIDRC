text = """
1
matheu
Afta six days, Jesus take Pita, James and John (wey bi James broda), go on-top one high mountin. 2
Jesus body kon shange. En face kon dey shine like sun and en dress kon white. 3
At wons Moses and Elijah kon appear dey tok to Jesus. Matiu 17:4
So Pita kon tell Jesus, “Oga God, e good make wi stay here. If yu like, I go build three tent: one for yu, one for Moses and one for Elijah.” 5
As e still dey tok, one brite kloud kon kover dem and one vois kon sey, “Dis na my Pikin wey I love. Make una listin to am!” 6
Wen di disciples hear di vois, dem fear kon fall face groun. 7
But Jesus tosh dem kon sey, “Stand up! Make una nor fear.” 8
Wen dem look up, di only pesin wey dem si, na Jesus. 9
As dem dey kom down from di mountin, Jesus warn dem sey, “Make una nor tell anybody dis vishon wey una si until God go wake Man Pikin from deat.” 10
Di disciples ask am, “Why di law tishas dey tish sey na Elijah go first kom?” 11
Jesus ansa, “Na true sey Elijah go first kom and e go ripair evritin. 12
And I tell una sey, dat Elijah don kom, but pipol nor know am, instead dem do am as dem like. Na so too, God Pikin go sofa for dia hand.” 13
Den di disciples kon know sey e dey tell dem about John di Baptist. 14
Wen Jesus and en disciples meet di pipol, one man kon knee down for Jesus front 15
beg am sey, “Oga God, make yu sorry for my son, bikos e nor well and many times, di sickness dey sofa and trow am inside fire and wota. 16
I bring am kom meet yor disciples, but dem nor fit heal am.” 17
Jesus kon ansa, “Una wey nor get faith and wey nor know wetin to do! How long I go dey with una? How long I go bear with una? Make una bring di boy kom here.” 18
Den Jesus kommand di demon komot from di boy body and at wons, di boy kon well. 19
Wen only di disciples dey with Jesus, dem kon ask am, “Why wi nor fit drive di demon komot from di boy body?” 20
Jesus ansa dem, “Na bikos una faith too small and I tell una true word, ‘If una get faith wey small like mustard seed, una go tell dis mountin, “Make yu move from here go yonda” and e go move and nor-tin go hard una to do.’ 21
Dis kind demon nor go gri komot from pesin body escept na with fasting and prayer.” 22
Wen dem enter Galilee, Jesus kon tell dem, “Somebody go sell Man Pikin give wiked pipol. 23
Dem go kill-am and for di third day, God go wake am up.” But di disciples nor happy, bikos of wetin Jesus tok. 24
Wen Jesus and en disciples rish Kapanaum, di pipol wey dey kollect tax for di temple kom meet Pita, ask am sey, “Yor oga dey pay Temple tax?” 25
Pita ansa, “Yes.” As Pita enter di house, Jesus kon ask am, “Wetin yu tink, Simon? Who dey pay tax give kings for dis world? Na pipol for di kountry or strenjas?” 26
Pita ansa, “Na strenjas dey pay tax.” So Jesus kon tell am, “Den dia own kountry pipol dey free, 27
but make dem nor for kause trobol, make yu go trow hook for river. Di first fish wey yu go katch, wen yu open en mout, yu go si money for inside, den make yu take di money pay di tax for mi and una.”
"""

# Split the text into lines
lines = text.split('\n')

# Add <extra_id_5> at the beginning and <extra_id_0> at the end of each line
formatted_lines = [f'<extra_id_5> {line} <extra_id_0>' for line in lines if line.strip()]

# Write the formatted lines into a new file called "decoding.txt"
with open("/PATH_TO/PLM4MT/data/textFiles/decoding.txt", "w") as file:
    for formatted_line in formatted_lines:
        file.write(formatted_line + '\n')

print("Decoding file created: decoding.txt")
