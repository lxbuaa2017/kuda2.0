# encoding=utf-8
en2t = {}
with open('/home/lx/IdeaProject/gAnswer/data/pkubase/fragments/pkubase_entity_fragment.txt', 'r') as f:
    for line in f:
        dou = line[:-1].split('\t')
        types = dou[1].replace('|', '#').split('#')[4]
        typeset = types.split(',')
        en2t[dou[0]] = set()
        for t in typeset:
            if len(t) < 6 and t != '-1' and len(t) > 0:
                en2t[dou[0]].add(t)
print("en2t loaded\n")
lisen = {}
for i in range(26):  # iterate every basic type
    lisen['%d' % i] = [set(), set(), set()]

with open('/home/lx/IdeaProject/gAnswer/data/pkubase/triple.txt', 'r') as f:
    i = 1
    for line in f:
        if i % 100000 == 0:
            print(i)
        i += 1
        tri = line.split(' ')
        print(tri)
        if tri[1] != '48':
            for t in en2t[tri[0]]:
                if len(t) <= 5:
                    lisen[t][1].add(tri[1])
                    lisen[t][2].add(tri[0])
            if tri[2].strip() != '-1':
                for t in en2t[tri[2].strip()]:
                    if len(t) <= 5:
                        lisen[t][0].add(tri[1])
                        lisen[t][2].add(tri[2].strip())

with open('/home/lx/IdeaProject/gAnswer/data/pkubase/fragments/pkubase_type_fragment.txt', 'w') as f:
    for k in lisen.keys():
        f.write(k + '\t' + ','.join(lisen[k][0]) + '|' + ','.join(lisen[k][1]) + '|' + ','.join(lisen[k][2]) + '\n')
    print(len(lisen))
