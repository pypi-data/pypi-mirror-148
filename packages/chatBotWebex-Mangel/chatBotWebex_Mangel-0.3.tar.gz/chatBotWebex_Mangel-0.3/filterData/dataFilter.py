import os
import json
import re
import logging


class FilterData :

        def getJsonSites():
            with open(os.path.dirname(__file__) + '/SITES_EDGES_BANCOLOMBIA.json', 'r') as archive:
                data = json.load(archive)
                return data


        def filterbySiteType(siteType, data):

            filterdata = [element for element in data if siteType.strip()
                        in element['siteType'].strip()]
            return filterdata


        def filterData(number, data):

            filterList = [element for element in data if re.findall(number + '$', element['siteCode'])
                                                                    or number in element['siteCode']
                                                                    or number in element['siteName']]

            return filterList


        def getDataSite(selection, siteList):
            
            siteList = list()
            site = ""
            count = 1
            
            for element in siteList:
                if count == int(selection):
                    site = element
                count += 1

            return site

