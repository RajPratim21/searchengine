# -*- coding: utf-8 -*-

import http.client
import  urllib.parse
import  json

# **********************************************
# *** Update or verify the following values. ***
# **********************************************

# Replace the subscriptionKey string value with your valid subscription key.
subscriptionKey = "fccf7cab51064683b06fce205fff50e5"

# Verify the endpoint URI.  At this writing, only one endpoint is used for Bing
# search APIs.  In the future, regional endpoints may be available.  If you
# encounter unexpected authorization errors, double-check this value against
# the endpoint for your Bing search instance in your Azure dashboard.
host = "api.cognitive.microsoft.com"
path = "/bing/v7.0/images/search"
import sys
term = sys.argv[1]

def BingImageSearch(search):

        headers = {'Ocp-Apim-Subscription-Key': subscriptionKey, 'header':'Medium'}
        conn = http.client.HTTPSConnection(host)
        query = urllib.parse.quote(search)
        conn.request("GET", path + "?q=" + query, headers=headers)
        response = conn.getresponse()
        headers = [k + ": " + v for (k, v) in response.getheaders()
                        if k.startswith("BingAPIs-") or k.startswith("X-MSEdge-")]
        return headers, response.read().decode("utf8")

def getImage():
        if len(subscriptionKey) == 32:
                #print('Searching images for: ', term)
                headers, result = BingImageSearch(term)
                res = (json.loads(result))
                for imglist in res['value']:
                        print (imglist['contentUrl'])

getImage()

