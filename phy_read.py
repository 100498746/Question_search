import jsonlines
import json

data_file = './static/all_exr.txt'
class PhyReader(object):
    def __init__(self, path):
        self.path = path



    def phy_reader(self):
        results = {}
        with jsonlines.open(self.path, 'r') as freader:
            for line in freader:
                pid = list(line.keys())[0]
                # print(pid)
                question = line[pid]
                results[pid] = question
        freader.close()
        return results

