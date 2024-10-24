import asyncio
import data.db_helper as db_helper
import requests
from multiprocessing import Lock
import uniq.uniq_confetti as uniq_confetti
import sys
import time
import json
import random
import re
import os
import imaplib
import email
import traceback
import string
i =0
video_names = asyncio.run(db_helper.get_single_video_to_update())
asyncio.run(uniq_confetti.process_video(video_names, i))