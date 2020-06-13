import bs4
import json

def ext_to_dict(soup_object,id):
    #find the items
    rod_div  = soup_object.find("div",{"id":id})
    rod_items = rod_div.find_all("div",{"class":"attendance-table-item"})
    
    dic = {}
    already = {}
    for box in rod_items:
        head = box.h3.contents
        services = box.find_all('li')
        km = head[0].strip()
        mao = head[1].contents[0]
        titulo = head[3].contents[0]
        servicos = []
        for s in services:
            servicos.append(s.contents[0].contents[0])
        if titulo in already:
            already[titulo] +=1
            titulo = ' '.join([titulo,str(already[titulo])])
            dic[titulo] = {
            "KM":km,
            "Mao" : mao,
            "Servicos" : servicos
            }
        else:
            already[titulo]=1
            dic[titulo]={
            "KM":km,
            "Mao" : mao,
            "Servicos" : servicos
            }
    return dic


def file_dic(file_input):
    #open
    with open(file_input,encoding='utf-8') as html_file:
        html = html_file.read()

    soup = bs4.BeautifulSoup(html,"html.parser",from_encoding='utf-8')

    rod_id = {}
    for rod in soup.find("div",{ "class":"tabs"}).find_all('a'):
        rod_id[rod.attrs['href'][1:]] = rod.contents[0]

    rod_pontos = {}
    for rod in rod_id:
        rod_pontos[rod_id[rod]] = ext_to_dict(soup,rod)
    
    return rod_pontos

if __name__ == "__main__":
    output = {}
    output['autoban'] = file_dic('HTML/autoBAn.html')
    output['msvia'] = file_dic('HTML/MSVia.html')
    output['novadutra'] = file_dic('HTML/NovaDutra.html')
    output['rodoanel'] = file_dic('HTML/RodoAnel.html')
    output['rodonorte'] = file_dic('HTML/RodoNorte.html')
    output['spvias'] = file_dic('HTML/SPvias.html')
    output['vialagos'] = file_dic('HTML/ViaLagos.html')
    output['viaoeste'] = file_dic('HTML/ViaOeste.html')
    output['viasul'] = file_dic('HTML/ViaSul.html')

    json_object = json.dumps(output, indent = 4,ensure_ascii=False).encode('utf-8').decode('utf-8')
    print(json_object)
    with open("output.json", "w",encoding='utf-8') as outfile: 
        outfile.write(json_object)