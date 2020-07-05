# encoding=utf-8
inEnEdge = {}
outEnEdge = {}
inEdge = {}
outEdge = {}
types = {}
with open('/home/lx/IdeaProject/gAnswer/data/pkubase/triple.txt', 'r') as f:
    i = 1
    for line in f:
        try:
            tri = line.split(' ')

            if tri[1] == '48' and tri[2].strip().strip() != '-1':
                if tri[0] in types:
                    types[tri[0]].add(tri[2].strip())
                else:
                    types[tri[0]] = set()
                    types[tri[0]].add(tri[2].strip())
            else:
                if tri[0] in outEdge:
                    outEdge[tri[0]].add(tri[1])
                else:
                    outEdge[tri[0]] = set()
                    outEdge[tri[0]].add(tri[1])

                if tri[2].strip() != '-1':
                    if tri[0] in outEnEdge:
                        if tri[2].strip() in outEnEdge[tri[0]]:
                            outEnEdge[tri[0]][tri[2].strip()].add(tri[1])
                        else:
                            outEnEdge[tri[0]][tri[2].strip()] = set()
                            outEnEdge[tri[0]][tri[2].strip()].add(tri[1])
                    else:
                        outEnEdge[tri[0]] = {}
                        outEnEdge[tri[0]][tri[2].strip()] = set()
                        outEnEdge[tri[0]][tri[2].strip()].add(tri[1])

                    if tri[2].strip() in inEdge:
                        inEdge[tri[2].strip()].add(tri[1])
                    else:
                        inEdge[tri[2].strip()] = set()
                        inEdge[tri[2].strip()].add(tri[1])
                    if tri[2].strip() in inEnEdge:
                        if tri[0] in inEnEdge[tri[2].strip()]:
                            inEnEdge[tri[2].strip()][tri[0]].add(tri[1])
                        else:
                            inEnEdge[tri[2].strip()][tri[0]] = set()
                            inEnEdge[tri[2].strip()][tri[0]].add(tri[1])
                    else:
                        inEnEdge[tri[2].strip()] = {}
                        inEnEdge[tri[2].strip()][tri[0]] = set()
                        inEnEdge[tri[2].strip()][tri[0]].add(tri[1])
            # if i % 10000 == 0:
            #     print(i)
            i += 1
        except:
            continue
print(len(inEnEdge))
print(len(outEnEdge))
print(len(inEdge))
print(len(outEdge))
print(len(types))
wr = open('/home/lx/IdeaProject/gAnswer/data/pkubase/fragments/pkubase_entity_fragment.txt', 'w')
with open("/home/lx/IdeaProject/gAnswer/data/pkubase/fragments/id_mappings/pkubase_entity_id.txt", "r") as f:  # here we should iterate every entitiy
    for line in f:
        i = int(line.split("\t")[1])
        # if i % 10000 == 0:
        #     print(i)
        eid = "%d" % i
        ret = ""
        tmp = ""
        if eid in inEnEdge:
            tmp = ""
            for k in inEnEdge[eid].keys():
                tmp += k
                tmp += ':'
                for item in inEnEdge[eid][k]:
                    if item == '-1':
                        continue
                    tmp += item + ';'
                tmp += ','
        ret += tmp
        tmp = ""
        ret += '|'

        if eid in outEnEdge:
            tmp = ""
            for k in outEnEdge[eid].keys():
                tmp += k
                tmp += ':'
                for item in outEnEdge[eid][k]:
                    if item == '-1':
                        continue
                    tmp += item + ';'
                tmp += ','
        ret += tmp
        tmp = ""
        ret += '|'

        if eid in inEdge:
            tmp = ""
            for item in inEdge[eid]:
                if item == '-1':
                    continue
                tmp += item + ','
        ret += tmp
        tmp = ""
        ret += '|'

        if eid in outEdge:
            tmp = ""
            for item in outEdge[eid]:
                if item == '-1':
                    continue
                tmp += item + ','
        ret += tmp
        tmp = ""
        ret += '|'

        if eid in types:
            tmp = ""
            for item in types[eid]:
                if item == '-1':
                    continue
                tmp += item + ','
        ret += tmp
        tmp = ""
        wr.write("%s\t%s" % (eid, ret))
        wr.write('\n')
wr.close()
