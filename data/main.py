import json
import numpy as np
import os
import unicodedata
import pickle
import sys
import time
from bs4 import BeautifulSoup

from utilities import Utilities

mode = sys.argv[1] # {expand, html_parser}

##############################################################

FILES = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h']
PIECES = {'p': 0, 'n': 1, 'b': 2, 'r': 3, 'q': 4, 'k': 5}

def pprint(cells):
    for i in range(8):
        print(cells[i*8:(i+1)*8])
    print()

'''
- Input:
    - saved_links.p
- Go through the links
- Parse the html to see parginator
- Output
    - extra_pages.p : count of number of pages - in same order as in saved_links.p
'''
def expander_main():
    utils = Utilities()
    data_path = "./saved_files/"
    src = data_path + "saved_links.p"
    destination_path = data_path + "expanded_links.p"
    saved_links = pickle.load( open(src,"r") )
    counts = []
    for i, link in enumerate(saved_links):
        print("i,link = ",i, link)
        num = 0
        #if i<2: continue
        #if i>3: break
        try:
            file = "saved"+str(i)+".html"
            html_doc = open(data_path + file,"r").read()
            soup = utils.getSoupFromHTML(html_doc)
            paginator = utils.getTableOfClass(soup, 'paginator')
            print("len(paginator) = ",len(paginator))
            if len(paginator)>0:
                paginator = paginator[0] # If it occurs, it occurs twice - and both seem to be identical
                txt = utils.soupToText(paginator).lower()
                if txt.count("next")>0:
                    txt = txt.replace("pages:","").strip()
                    for j,c in enumerate(txt):
                        if c>='1' and c<='9': # assuming <=9 extra pages
                            num+=1
                        else:
                            break
            print("num = ",num)
        except:
            print("----ERROR:")
        counts.append(num)
    print("len(counts) = ",len(counts))
    print("sum(counts) = ",sum(counts))
    pickle.dump(counts, open("extra_pages.p","w"))
            


            


##############################################################
class DataCollector:

    def __init__(self):
        self._utils = Utilities()
        self._data_path = "./saved_files/"
        self._destination_path = "./outputs/"
        print("------")

    def _getList(self):
        files = os.listdir(self._data_path)
        files = [f for f in files if f.count("html")>0]
        return files

    # Return the bitboard index for a given cell. h1->0, a8->63, etc.
    def _numberizeCell(self, cell):
        col = cell[0]
        row = cell[1]
        return (8-int(row))* 8 + FILES.index(col)
        

    def _getBoardValues(self, soup):
        board_info = soup.findAll("div")[0]['data-chess-diagram']
        
        return board_info.split('|||')


    def _getBitboardFromFEN(self, fen):
        board, turn_color, castling , ep = fen.split()
        castling_rights = set(castling)
        cells = []
        for row in board.split('/'):
            for c in row:
                try:
                    c = int(c)
                    cells.extend(['.']*c)
                except:
                    cells.append(c)

        bb = np.zeros((2, 6, 64), dtype=np.uint8)
        for color in range(2):
            for piece in range(6):
                for square in range(64):
                    if cells[square] is not '.':
                        if (color == 0) == (cells[square].isupper()):
                            if PIECES[cells[square].lower()] == piece+1:
                                bb[color][piece][square] = 1

        info = np.zeros(5, dtype=np.uint8)
        info[0] = 'K' in castling_rights
        info[1] = 'k' in castling_rights
        info[2] = 'Q' in castling_rights
        info[3] = 'q' in castling_rights
        info[4] = turn_color == 'w'

        bb = bb.flatten()
        bb = np.concatenate((bb, info))

        return bb
                                

    def _getPrevBitboard(self, bb, move):
        start = self._numberizeCell(move[5:7])
        end = self._numberizeCell(move[7:9])

        prev_bb = bb.copy()

        for board_start_index in range(0, 64*12, 64):
            if bb[board_start_index + end]:
                prev_bb[board_start_index + end] = 0
                prev_bb[board_start_index + start] = 1
                break

        return prev_bb




    def getData(self):
        all_files = self._getList()
        fw = open("_files.txt","w")
        for file in all_files:
            try:
                print("file = ",file)
                html_doc = open(self._data_path + file,"r").read()
                soup = BeautifulSoup(html_doc, "html.parser")
                results = soup.findAll("table",{"class":"dialog"})
                results2 = [ result for result in results[0].findAll("tr") if
                        len(result.findAll("td", recursive=False))==2 and
                        str(result).find("data-chess-diagram") > 0] #based on observation
                
                all_steps_info = []
                boards = None
                for index,result in enumerate(results2):
                    if index%2==1:
                        continue #fix for repetitions
                    td_res = result.findAll("td", recursive=False)
                    td = td_res[0] ## move+board

                    ##--- Extract moves
                    txt =  td.get_text()
                    txt = unicodedata.normalize('NFKD', txt).encode('ascii','ignore')

                    # moves = txt[:txt.find("<!--")].strip()
                    moves = txt.strip()
                    
                    ##--- Extract board elements
                    fen, move = self._getBoardValues(result)
                    bb = self._getBitboardFromFEN(fen)
                    prev_bb = self._getPrevBitboard(bb, move)
                    
                    ##--- Get the comment
                    td = td_res[1] ## Comment
                    comment = self._utils.soupToText(td)
                    print(comment)
                    
                    ##--- Add to data structure
                    current_boards = np.stack((prev_bb, bb))
                    if boards is not None:
                        boards = np.concatenate((boards, current_boards), axis=0)
                    else:
                        boards = current_boards

                    current_step_info = [moves, comment]
                    all_steps_info.append(current_step_info)
                pickle.dump( all_steps_info, open(self._destination_path +
                    file.replace(".html",".obj"), "wb") )
                np.save(open(self._destination_path + file.replace("html",
                    "bb"), "wb"), boards)
            except Exception as ex:
                print(ex)
                fw.write(file)
                fw.write("\n")
        fw.close()
        #print "=========================================================="

##############################################################

if mode=="html_parser":
    data_collector = DataCollector()
    data_collector.getData()
elif mode=="expand":
    expander_main()
else:
    print("Wrong option")
