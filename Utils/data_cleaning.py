import csv
import time
import re

def get_hashtags(text):
    sentences = text.split(".")
    words = [word for sentence in sentences for word in sentence.split()]
    all_hashtags = [word[1:] for word in words if word.startswith('#')]
    for tag in all_hashtags:
        text = text.replace("#" + tag, "")
    
    results = []
    for i in range(len(all_hashtags)):
        result = []
        for j in range(len(all_hashtags[i])):
            if not (all_hashtags[i][j] >= 'a' and all_hashtags[i][j] <= 'z') and not (all_hashtags[i][j] >= 'A' and all_hashtags[i][j] <= 'Z'):
                pass
            else:
                result.append(all_hashtags[i][j])
        results.append(''.join(result))
    return (';'.join(results), text)

def get_ats(text):
    sentences = text.split(".")
    words = [word for sentence in sentences for word in sentence.split()]
    all_hashtags = [word[1:] for word in words if word.startswith('@')]
    for tag in all_hashtags:
        text = text.replace("#" + tag, "")
    
    results = []
    for i in range(len(all_hashtags)):
        result = []
        for j in range(len(all_hashtags[i])):
            if not (all_hashtags[i][j] >= 'a' and all_hashtags[i][j] <= 'z') and not (all_hashtags[i][j] >= 'A' and all_hashtags[i][j] <= 'Z'):
                pass
            else:
                result.append(all_hashtags[i][j])
        results.append(''.join(result))
    return (';'.join(results), text)

def get_words(text):

    word_start = False
    start = 0
    result = []
    for index in range(len(text)):
	    char = text[index]
	    if not char.isalpha() and not word_start:
	        continue
	    else:
	        # we are reading a word
	        # update the start index
	        if not word_start:
	            word_start = True
	            start = index
	        # reach the end of a word
	        if not char.isalpha():
	            word_start = False
	            result.append(text[start:index])
    
    if word_start and start != len(text) - 1:
        result.append(text[start:len(text)])
    
    return " ".join(result)


def get_links(text):
    urls = re.findall(r'(https?://\S+)', text)
    for i in range(len(urls)):
        if urls[i][-1] == '.' or urls[i][-1] == '!' or urls[i][-1] == '?':
            urls[i] = urls[i][:len(urls[i]) - 1]
    for url in urls:
        text = text.replace(url, '')
    return (';'.join(urls), text)



start_time = time.time()
line_count = 0
with open('data.csv', encoding = "utf8", errors = "ignore") as csv_file_read:
    with open('text_link_hashtag.csv', "w+", encoding = "utf8", errors = "ignore") as csv_file_write:
        csv_writer = csv.writer(csv_file_write, delimiter=',', quoting=csv.QUOTE_MINIMAL)
        csv_reader = csv.reader(csv_file_read, delimiter=',')
        
        for row in csv_reader:
            #first row is headers, we set up headers for result file as well
            if line_count == 0: 
                csv_writer.writerow(['Text', '@', 'Hyperlinks', 'Hashtags'])
                line_count += 1
                continue
            
            #Text (row[6])
            persons, text = get_ats(row[6])
            hashtags, text = get_hashtags(text)
            hyper_links, text = get_links(text)
            cleaned_text = get_words(text)
            
            data_to_add = [cleaned_text, persons, hyper_links, hashtags]
            csv_writer.writerow(data_to_add)
            line_count +=1

print("It takes", str(time.time() - start_time), "second to process", str(line_count), "lines")