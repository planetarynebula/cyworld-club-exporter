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
                
                try:
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
                except:
                    pass

def printProgressBar (iteration, total, prefix = '', suffix = '', decimals = 1, length = 50, fill = '█', printEnd = "\r"):
    """
    Call in a loop to create terminal progress bar
    @params:
        iteration   - Required  : current iteration (Int)
        total       - Required  : total iterations (Int)
        prefix      - Optional  : prefix string (Str)
        suffix      - Optional  : suffix string (Str)
        decimals    - Optional  : positive number of decimals in percent complete (Int)
        length      - Optional  : character length of bar (Int)
        fill        - Optional  : bar fill character (Str)
        printEnd    - Optional  : end character (e.g. "\r", "\r\n") (Str)
    """
    percent = ("{0:." + str(decimals) + "f}").format(100 * (iteration / float(total)))
    filledLength = int(length * iteration // total)
    bar = fill * filledLength + '-' * (length - filledLength)
    print('\r%s |%s| %s%% %s' % (prefix, bar, percent, suffix), end = printEnd)
    # Print New Line on Complete
    if iteration == total: 
        print()

articles = [article for article in article_list if article.startswith("article_list_")]
print('start article...')
tot = len(articles)
cnt = 0
for article in articles[:]:
    function(article, 'article')
    cnt += 1
    printProgressBar(cnt, tot)

galleries = [gallery for gallery in gallery_list if gallery.startswith("gallery_list_")]
print('start gallery...')
tot = len(galleries)
cnt = 0
for gallery in galleries[:]:
    function(gallery, 'gallery')
    cnt += 1
    printProgressBar(cnt, tot)