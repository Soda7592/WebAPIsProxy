from mitmproxy import http
from mitmproxy import ctx
import os
import json

class main:
    def __init__(self):
        self.num = 0
        self.httpRequestlist = []
        self.domainName = None
        self.jsonDict = ""
        self.loadFiles()
        

    def loadFiles(self) :
        try: 
            with open('httpRequest.txt', 'r') as f:
                self.httpRequestlist = f.readlines()
            if os.path.exists("ApiInfo.json") :
                self.jsonDict = json.load("ApiInfo.json")
            else :
                with open('ApiInfo.json', 'w') as api :
                    pass
        except FileExistsError as err:
            ctx.log.info(FileExistsError)

    def load(self, loader) :
        loader.add_option(name="domain", typespec=str, default="", help="Specify a target domain name.")

    def request(self, flow):
        self.domainName = ctx.options.domain
        request = flow.request
        if self.domainName in request.url :
            url = str(request.url)
            httpPostString =  url[url.find('.tw')+3:]
            # apisData = self.writeIntoTxt
            if httpPostString.find('?') != -1 :
                httpPostString = httpPostString[:httpPostString.find('?')]
            try :
                with open('httpRequest.txt', 'a') as f:
                    if request.method == "POST" :
                        content = request.content.decode('utf-8')
                        postARG = request.get_text().split('&')
                        if len(postARG) and (httpPostString not in self.httpRequestlist) :
                            self.httpRequestlist.append(httpPostString)
                            if len(postARG[0]) != 0 :    
                                f.write(httpPostString + '(' + request.method + ')' +   '\n')
                                # apisData['ApiEndpointName'] = httpPostString
                                argDict = {}
                                for i in postARG :
                                        arg = i[:i.find('=')]
                                        val = i[i.find('=')+1:]
                                        argDict[arg] = val
                                        f.write(arg + ':' + val + '\n')
                                        # apisData['Arguments'] = argDict
                                        self.jsonDict[httpPostString] = argDict
                                        json.dump(json.loads(self.jsonDict), 'ApiInfo.json')
                                        # with open('ApiInfo.json', 'a') as js :
                                        #     js.write(json.dumps(apisData) + '\n')
                        if len(content) != 0 and (httpPostString not in self.httpRequestlist) :
                            f.write(httpPostString + '(' + request.method + ')' +   '\n')
                            self.httpRequestlist.append(httpPostString)
                            f.write(content + '\n')
                    elif request.method == "GET" :
                        getARG = list(request.query.keys())
                        getVAL = list(request.query.values())
                        if len(getARG) and (httpPostString not in self.httpRequestlist):
                            self.httpRequestlist.append(httpPostString)
                            f.write(httpPostString + '(' + request.method + ')' +   '\n')
                            for i in range(len(getARG)) :
                                arg = getARG[i]
                                val = getVAL[i]
                                f.write(arg + ":" + val + '\n')
            except FileExistsError as err:
                ctx.log.info(FileExistsError) 

    def response(self, flow):
        response = flow.response
        info = ctx.log.info