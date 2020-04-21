import os, json, re, datetime
from bs4 import BeautifulSoup
from shutil import copyfile

article_list = os.listdir('./result')
gallery_list = os.listdir('./result')
comment_list = os.listdir('./result')
file_list = os.listdir('./images')

def get_valid_folder_name(name):
    return name.replace('/','.').replace('?', '.').replace('<','[').replace('>',']').replace('"',"'").replace(':','-').replace('*',' ').replace('|',' ').strip()

def function(filename, topic):
    with open('./result/' + filename, "r") as f:
        line = f.readline()
        item_seq = list(map(lambda x: int(x), line[1:-1].split(',')))
        for item in item_seq:
            with open('./result/' + topic + '_view_' + str(item) + ".txt", "r") as f:
                line = f.readline()
                data = json.loads(line)
                category = ""
                if topic == "article":
                    category = data['category'][6:].strip()
                elif topic == "gallery":
                    category = data['category'][7:].strip()
                else:
                    print("error: unknown topic!")
                    return
                    
                category = get_valid_folder_name(category)
                
                subject = get_valid_folder_name(data['subject'])
                subject = '[' + data['registerAt'].replace(':', '.') + '] ' + subject
                
                if data['username']:
                    subject = subject + ' (' + str(data['username']) + ')'
                
                file_path = os.path.join(topic, category, subject)
                os.makedirs(file_path, exist_ok = True)

                files = [file for file in file_list if file.startswith(str(data['articleNo']))]
                comment = 'comment_' + str(data['articleNo']) + '.txt'

                for file in files:
                    copyfile('./images/' + file, os.path.join(file_path, file))

                with open(os.path.join(file_path, "page.html"), "w") as f:
                    html = data['contents']
                    soup = BeautifulSoup(html, 'html.parser')

                    for img in soup.find_all('img'):
                        img_url = img['src'][8:-4]
                        
                        for img_file in files:
                            if img_url in img_file:
                                img['src'] = './' + img_file
                                break
                    f.write(str(soup))
                
                with open('./result/'+comment, "r") as fr:
                    line = fr.readline()
                    data_list = json.loads(line)
                    valid_comments = []
                    if data_list:
                        for data in data_list:
                            is_ok = True
                            for i in valid_comments:
                                if i == data:
                                    is_ok = False
                                    break
                            if is_ok:
                                valid_comments.append(data)

                        with open (os.path.join(file_path, "comment.txt"), "w") as fw:
                            for data in valid_comments:
                                fw.write(data['username'] + ' (' + data['registerAt'] + ')\n')
                                fw.write(data['contents'] + '\n\n')

articles = [article for article in article_list if article.startswith("article_list_")]
for article in articles[:]:
    function(article, 'article')

galleries = [gallery for gallery in gallery_list if gallery.startswith("gallery_list_")]
for gallery in galleries[:]:
    function(gallery, 'gallery')