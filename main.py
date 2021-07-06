# -*- coding: utf-8 -*-
"""
Created on Thu Jul  1 18:01:36 2021

@author: ADMIN
"""

from vnexpress_daily import VnExpewss
from foxnews_daily import Foxnews
from tuoitre_daily import Tuoitre

VnExpewss().main()
Foxnews().main()
Tuoitre().main()
print("Done")