import os 
name = [
    ('llx2','JP')
]

out_file = f"filelists/llx2.txt"

def process():
    with open(out_file, 'w', encoding="utf-8") as wf:
        for item in name:
            ch_name = item[0]
            ch_lan = item[1]
            path = f"./raw/{ch_name}"
            files = os.listdir(path)
            for f in files:
                if f.endswith(".lab") or f.endswith(".txt"):
                    with open(os.path.join(path,f),'r',encoding='utf-8') as perFile:
                        line = perFile.readline()
                        res = f"./dataset/{ch_name}/{f.split('.')[0]}.wav|{ch_name}|{ch_lan}|{line}"
                        wf.write(f'{res}\n')
                        
                        
if __name__ == '__main__':
    process()