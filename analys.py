text = open("out/text0.txt", encoding='utf-8').read().split("\n")

filtered = []
for sentence in text:
    flag = True
    words = sentence.split(" ")
    for word in words:
        if (word and word[0] in ["ъ", "ы", "ь", "й"]):
            flag = False
            break
        if (word in list("бгдеёзйлмнпртфхцчшщэю")):
            flag = False
            break

    if flag:
        filtered.append(sentence)
open("filtered.txt", 'w', encoding='utf-8').write('\n'.join(filtered))