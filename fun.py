import os
import urllib
import fortune
import time

if "FUN_CONFIG_path_to_fortune" in os.environ: PATH_TO_FORTUNE=os.environ.get("FUN_CONFIG_path_to_fortune")
else: print ("Please set the environment variable FUN_CONFIG_path_to_fortune to contain the full path to the fortune file.\nexiting...");exit(255)
URL_TO_FORTUNE="https://gist.githubusercontent.com/textarcana/676ef78b2912d42dbf355a2f728a0ca1/raw/f50d5792496b551c847cc3deb04959daf7dd2638/devops_borat.dat"

def init():
	#if not exists fortune text - download fortune text	
	if not os.path.isfile(PATH_TO_FORTUNE):
		print("Fortune database not found, downloading from "+URL_TO_FORTUNE+" ...")
		urllib.urlretrieve(URL_TO_FORTUNE,PATH_TO_FORTUNE)
	#if exists fortune text - always generate fortune index
		print ("refreshing the fortune index...")
		fortune.make_fortune_data_file([PATH_TO_FORTUNE])
def get_one():
	return (fortune.get_random_fortune([PATH_TO_FORTUNE]))

