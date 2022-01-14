import json
import argparse
import os
import random
import numpy as np
import requests
import logging
import math
import copy
import string
import time

from tqdm import tqdm
from time import time
from flask import Flask, request, jsonify
from flask_cors import CORS
from tornado.wsgi import WSGIContainer
from tornado.httpserver import HTTPServer
from tornado.ioloop import IOLoop
from all_ES import ESphy
from phy_read import PhyReader

logging.basicConfig(format='%(asctime)s - %(levelname)s - %(name)s -   %(message)s', datefmt='%m/%d/%Y %H:%M:%S',
                    level=logging.INFO)
logger = logging.getLogger(__name__)

def run_simcse_demo(port, args):
    app = Flask(__name__, static_folder='./static')
    app.config['JSONIFY_PRETTYPRINT_REGULAR'] = False
    CORS(app)
    sentence_path = os.path.join(args.sentences_dir, args.example_sentences)
    embed = ESphy()
    new_path = './static/all_exr.txt'
    newques = PhyReader(new_path)
    query_path = os.path.join(args.sentences_dir, args.example_query)
    @app.route('/')
    def index():
        return app.send_static_file('index.html')

    @app.route('/api', methods=['GET'])
    def api():
        query = request.args['query']
        top_k = int(request.args['topk'])
        print(query)
        print(top_k)
        # threshold = float(request.args['threshold'])
        start = time()
        results = embed.bm25search(query)
        new_results = newques.phy_reader()
       # results = [['a woman is carrying her baby', '0.5'],["<p>关于摩擦起电，下列说法正确的是（ ）</p>\n\n<p>（A）只有正电荷从一个物体转移到另一个物体</p>\n\n<p>（B）只有电子从一个物体转移到另一个物体</p>\n\n<p>（C）正负电荷同时按相反方向方向转移</p>\n\n<p>（D）以上三种情况都有可能</p>\n",0.6]]
        ret = []
        out = {}
        for sentence, score, pid in results:
            ret.append({"sentence": new_results[pid], "score": score})
            # ret.append({"sentence": sentence, "score": score})
        # ret.append({"sentence": results[0], "score": results[1]})
        span = time() - start
        out['ret'] = ret
        out['time'] = "{:.4f}".format(span)
        return jsonify(out)

    @app.route('/files/<path:path>')
    def static_files(path):
        return app.send_static_file('files/' + path)
        
    @app.route('/get_examples', methods=['GET'])
    def get_examples():
        with open(query_path, 'r') as fp:
            examples = [line.strip() for line in fp.readlines()]
        return jsonify(examples)
    
    addr = args.ip + ":" + args.port
    logger.info(f'Starting Index server at {addr}')
    http_server = HTTPServer(WSGIContainer(app))
    http_server.listen(port)
    IOLoop.instance().start()

if __name__=="__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--model_name_or_path', default=None, type=str)
    parser.add_argument('--device', default='cpu', type=str)
    parser.add_argument('--sentences_dir', default='./static', type=str)
    parser.add_argument('--example_query', default='example_query.txt', type=str)
    parser.add_argument('--example_sentences', default='example_sentence.txt', type=str)
    parser.add_argument('--port', default='5000', type=str)
    parser.add_argument('--ip', default='0.0.0.0')
    parser.add_argument('--load_light', default=False, action='store_true')
    args = parser.parse_args()


    run_simcse_demo(args.port, args)