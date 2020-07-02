#encoding=utf-8
en2t = {}
with open('/home/lx/PycharmProjects/kuda2.0/pkubase_entity_fragment.txt','r') as f:
	for line in f:
		dou = line[:-1].split('\t')
		types = dou[1].replace('|','#').split('#')[4]
		typeset = types.split(',')
		en2t[dou[0]] = set()
		for t in typeset:
			if len(t)<6 and t!='-1' and len(t)>0:
				en2t[dou[0]].add(t)
sen = set()
lisen = {}
for i in range(49):#iterate every predicate
	lisen['%d'%i] = set()

with open('/home/lx/PycharmProjects/kuda2.0/triple.txt','r') as f:
	i = 1
	for line in f:
		if i%100000==0:
			print(i)
		tri = line[:-1].split(' ')
		if tri[0]!='-1':
			pre = '['+','.join(en2t[tri[0]])+']'
		else:
			pre = '[]'
		if tri[2].strip()!='-1' and tri[1]!='48':
			print(tri)
			pos = '['+','.join(en2t[tri[2].strip()])+']\n'
			str = pre + '\t' + tri[1] + '\t' + pos
			sen.add(str)
		else:
			lisen[tri[1]].add(tri[0])

for k in lisen.keys():
	str = '['+','.join(lisen[k])+']\t'+k+'\tliteral\n'
	sen.add(str)

with open('/home/lx/PycharmProjects/kuda2.0/pkubase_predicate_fragment.txt','w') as f:
	for item in sen:
		f.write(item)
	print(len(sen))
		
		
