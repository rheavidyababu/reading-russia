from lib2to3.pgen2 import token
import nltk
import re
import pandas as pd
import matplotlib.pyplot as plt
nltk.download("punkt")
from nltk.probability import FreqDist
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from collections import Counter
from wordcloud import WordCloud

def organize(filename):
    titles = []
    descriptions = []
    genres = []
    with open(filename, 'r', encoding="utf-8") as file:
        for i, line in enumerate(file):
            if i%4 == 1:
                descriptions.append(line.strip('\n'))
            elif i%4 == 2:
                genres.append(line.strip('\n'))
            elif i%4 == 0:
                ttle = line.strip('\n')
                if "10 " in ttle:
                    titles.append(ttle[3:])
                else: 
                    titles.append(ttle[2:])
    file.close()
    return titles, descriptions, genres

def parse(category):
    large_string = ""
    for obj in category:
        lowerfile = obj.lower()
        organized_file = re.sub(r'[^\w\s]','',lowerfile)
        large_string += organized_file + " "
    tokens = word_tokenize(large_string)
    filtered_words = [word for word in tokens if not word in stopwords.words()]
    return filtered_words

def freq_finder(filtered_words, file_names):
    c = Counter(filtered_words)
    y = [val for word, val in c.most_common(15)]
    x = [word for word, count in c.most_common(15)]
    plt.bar(x, y, color='crimson')
    plt.title("Term Frequencies in " + file_names + " Data")
    plt.ylabel("Frequency")
    plt.yscale("linear") # optionally set a log scale for the y-axis
    plt.xticks(rotation=45)
    for i, (word, val) in enumerate(c.most_common(15)):
        plt.text(i, val, f' {val} ', rotation=0,
             ha='center', va='top', color='white')
    plt.xlim(-0.6, len(x)-0.4) # optionally set tighter x lims
    plt.tight_layout() # change the whitespace such that all labels fit nicely
    plt.show()

def generate_wordcloud(text, files_names):
    textstr = ""
    for word in text:
        textstr += word + " "
    wordcloud = WordCloud().generate(textstr)
    plt.imshow(wordcloud)
    plt.axis("off")
    plt.title("Term Frequencies in \n" + files_names + " Data")
    plt.show()


def titles_chart(titles1, titles2, files_names):
    combined = [t for t in titles1]
    for i in titles2:
        if i not in titles1:
            combined += [i]
    print(combined)
    pos = list(range(len(combined)))
    one_num = []
    two_num = []
    for t in combined:
        if t in titles1:
            val_one = 10-titles1.index(t)
            one_num += [val_one]
            if t in titles2:
                val_two = 10-titles2.index(t)
                two_num += [val_one+val_two]
            else:
                two_num += [0]
        else:
            one_num += [0]
            if t in titles2:
                val_two = 10-titles2.index(t)
                two_num += [val_two]
            else:
                two_num += [0]
    plt.bar(pos, two_num, color='pink')
    plt.bar(pos, one_num, color='red')
    plt.xticks(ticks=pos, labels=combined, rotation=75)
    plt.ylabel('Combined Ranking')
    plt.title("Titles Popularity in " + files_names + " Data")
    plt.yscale("linear") # optionally set a log scale for the y-axis
    plt.xlim(-0.6, len(combined)-0.4) # optionally set tighter x lims
    plt.tight_layout() # change the whitespace such that all labels fit nicely
    plt.legend(['First Week', 'Second Week'], loc='upper left')
    plt.show()

def create_files(c,t,n):
    files_list = []
    for country in c:
        for type_ in t:
            for num in n:
                file_name = country +" "+ type_ +" "+ num +".txt"
                files_list.append(file_name)
    return files_list

if __name__ == '__main__':
    country_names = ["russia", "ukraine", "usa"]
    type_names = ["movies", "shows"]
    numbers = [str(n) for n in range(7, 11)]
    files_list = create_files(country_names, type_names, numbers)
    print(files_list)
    for f_index in range(0, len(files_list), 2):
        g = organize(files_list[f_index])
        title1, desc1, genre1 = g
        desc1 = parse(desc1)
        genre1 = parse(genre1)
        g = organize(files_list[f_index+1])
        title2, desc2, genre2 = g
        desc2 = parse(desc1)
        genre2 = parse(genre1)
        titles = title1 + title2
        desc =  desc1 + desc2
        genre = genre1 + genre2
        if "7" in files_list[f_index]:
            names = files_list[f_index][:-6].upper() + " BEFORE INVASION -"
        else:            
            names = files_list[f_index][:-6].upper() + " AFTER INVASION -"
        generate_wordcloud(desc, names +" DESCRIPTIONS")
        freq_finder(genre, names+" GENRE")
        titles_chart(title1, title2, names)
        
