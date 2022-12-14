import sys
import requests

if __name__ == '__main__':
    if len(sys.argv)!=2:
        print("Invalid argument")
        sys.exit()
    else:
        packageName = sys.argv[1]

dot_code = "digraph D{\n"
packageNames = []

def get_dependency(packageName):
    packageNames.append(packageName)
    try:
        response = requests.get(f'https://pypi.org/pypi/{packageName}/json')
        requires_dist = response.json()['info']['requires_dist']
    except:
        return
    if requires_dist!=None:
        edges = []
        for i in requires_dist:
            if('extra ==' not in i):
                nextName = i.split(' ')[0].split('<')[0].split('>')[0].split('=')[0].split(';')[0]
                if(nextName in edges):
                    continue
                edges.append(nextName)
                global dot_code
                dot_code += f'"{packageName}" -> "{nextName}";\n'
                if(nextName in packageNames):
                    continue
                get_dependency(nextName)
    

get_dependency(packageName)
dot_code += '}'
print(dot_code)