import gdown
import os
from zipfile import ZipFile
import requests
from PyQt5 import QtCore, QtWidgets, QtGui
import time
import json
import sys
import subprocess
import os


def download():
   id = "1pAgL9qMbYZ-U4S_2-ZBVDZ3u2vBMMKE8"
   output = 'simulator.zip'
   gdown.download(id=id, output=output, quiet=False)
   with ZipFile(str(output), 'r') as zipObj:
      # Extract all the contents of zip file in current directory
      zipObj.extractall(".\\VPR")

download()