import json,sys,os,collections
d=sys.argv[1]; out=sys.argv[2]
labels={}
for f in os.listdir(d):
    if f.endswith('.meta.json'):
        labels[f[:-10]]=json.load(open(os.path.join(d,f),encoding='utf-8')).get('description')
os.makedirs(out,exist_ok=True)
for aid,label in sorted(labels.items(), key=lambda x:x[1]):
    p=os.path.join(d,aid+'.jsonl')
    if not os.path.exists(p) or os.path.getsize(p)<500000: continue
    tools=collections.Counter(); calls={}; lines=[]
    with open(p,encoding='utf-8') as fh:
        for line in fh:
            try: o=json.loads(line)
            except: continue
            msg=o.get('message') or {}; c=msg.get('content'); role=msg.get('role')
            if not isinstance(c,list): continue
            for b in c:
                if not isinstance(b,dict): continue
                t=b.get('type')
                if t=='text' and role=='assistant' and b.get('text','').strip():
                    lines.append('NOTE: '+b['text'].strip())
                elif t=='tool_use':
                    tools[b.get('name')]+=1; calls[b.get('id')]=(b.get('name'),b.get('input'))
                    inp=b.get('input') or {}
                    if b.get('name') in ('Bash','Write','Edit'):
                        lines.append(f"CALL {b.get('name')}: {json.dumps(inp)[:1500]}")
                    if b.get('name') in ('WebFetch','WebSearch'):
                        lines.append(f"CALL {b.get('name')}: {inp.get('url') or inp.get('query')} :: {str(inp.get('prompt',''))[:300]}")
                elif t=='tool_result':
                    name,inp=calls.get(b.get('tool_use_id'),(None,None))
                    if name in ('WebFetch','WebSearch','Bash'):
                        cc=b.get('content'); 
                        if isinstance(cc,list): cc=' '.join(x.get('text','') for x in cc if isinstance(x,dict))
                        cc=str(cc)
                        lim=2500 if name in ('WebFetch','Bash') else 600
                        lines.append(f"RESULT ({name}): {cc[:lim]}")
    fn=os.path.join(out,label.replace(':','_')+'.txt')
    open(fn,'w',encoding='utf-8').write('\n'.join(lines))
    print(label, dict(tools), os.path.getsize(fn))
