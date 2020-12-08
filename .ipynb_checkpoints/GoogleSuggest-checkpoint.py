import argparse
import requests
import urllib.parse

#search Google Suggest Class
class GoogleSuggestClass:
    def __init__(self):
        self.base_url = 'https://www.google.co.jp/complete/search?'\
                        'hl=ja&output=toolbar&ie=utf-8&oe=utf-8&'\
                        'client=firefox&q='
        
        #loading word list
        word_dat = open('table.dat','r')
        word_list = []
        for word in word_dat:
            word = word.rstrip()
            word_list.append(word)
            
        self.chrs  = [str(i) for i in word_list]
    
    
    #get and print search result
    def get_suggest(self, query: str) -> list:
        buf = requests.get(self.base_url + urllib.parse.quote_plus(query)).json()
        suggests = [ph for ph in buf[1]]
        print("Search Result: [{0}]".format(query, len(suggests)))
        for ph in suggests:
            print(" ", ph)

        return suggests
    
    #call get_result function with keyword & word_list
    def get_suggest_keyword(self, query: str) -> list:
        # only keyword
        ret = self.get_suggest(query)

        # keyword + space
        ret.extend(self.get_suggest(query + ' '))

        # keypwrd + initial word
        for ch in self.chrs:
            ret.extend(self.get_suggest(query + ' ' + ch))
            
        # unique
        return self.get_uniq(ret)

    
    # eliminate duplication
    def get_uniq(self, arr: list) -> list:
        uniq_ret = []
        for x in arr:
            if x not in uniq_ret:
                uniq_ret.append(x)
        return uniq_ret
