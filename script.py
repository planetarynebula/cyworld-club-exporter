import os, json, re, datetime
from bs4 import BeautifulSoup
from shutil import copyfile

article_list = os.listdir('./result')
gallery_list = os.listdir('./result')
file_list = os.listdir('./images')

articles = [article for article in article_list if article.startswith("article_list_")]
for article in articles:
    with open('./result/'+article, "r") as f:
        line = f.readline()
        item_seq = list(map(lambda x: int(x), line[1:-1].split(',')))
        for item in item_seq:
            with open('./result/article_view_'+str(item)+".txt", "r") as f:
                line = f.readline()
                data = json.loads(line)
                category = data['category'][6:].strip()
                subject = data['subject'].replace('/', '.').replace('?', '.').strip()
                subject = subject + ' (' + data['username'] + '_' + data['registerAt'].replace(':', '.') + ')'

                file_path = os.path.join('article', category, subject)
                os.makedirs(file_path, exist_ok = True)
                
                with open(os.path.join(file_path, "text.txt"), "w") as f:
                    content = BeautifulSoup(data['contents'], "lxml").text
                    content = re.sub(r'P {MARGIN-TOP: ?2px; MARGIN-BOTTOM: ?2px}', '', content)
                    f.write('작성자: ' + data['username'] + '\n')
                    f.write('작성일: ' + data['registerAt'] + '\n\n')
                    f.write(content)
                with open(os.path.join(file_path, "page.html"), "w") as f:
                    f.write(data['contents'])
                
                files = [file for file in file_list if file.startswith(str(data['articleNo']))]
                for file in files:
                    copyfile('./images/'+file, os.path.join(file_path, file))


galleries = [gallery for gallery in gallery_list if gallery.startswith("gallery_list_")]
for gallery in galleries:
    with open('./result/'+gallery, "r") as f:
        line = f.readline()
        item_seq = list(map(lambda x: int(x), line[1:-1].split(',')))
        for item in item_seq:
            with open('./result/gallery_view_'+str(item)+".txt", "r") as f:
                line = f.readline()
                data = json.loads(line)
                category = data['category'][7:].strip()
                subject = data['subject'].replace('/', '.').replace('/', '.').strip()
                subject = subject + ' (' + data['username'] + '_' + data['registerAt'].replace(':', '.') + ')'

                file_path = os.path.join('gallery', category, subject)
                os.makedirs(file_path, exist_ok = True)

                with open(os.path.join(file_path, "text.txt"), "w") as f:
                    content = BeautifulSoup(data['contents'], "lxml").text
                    content = re.sub(r'P {MARGIN-TOP: ?2px; MARGIN-BOTTOM: ?2px}', '', content)
                    f.write('작성자: ' + data['username'] + '\n')
                    f.write('작성일: ' + data['registerAt'] + '\n\n')
                    f.write(content)
                with open(os.path.join(file_path, "page.html"), "w") as f:
                    f.write(data['contents'])
                
                files = [file for file in file_list if file.startswith(str(data['articleNo']))]
                for file in files:
                    copyfile('./images/'+file, os.path.join(file_path, file))
