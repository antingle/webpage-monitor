import requests
import os
import logging
import time

#interval to send webpage get request
DELAY_TIME = 15

#change this to the URL you want to monitor
URL_TO_MONITOR = "https://www.apple.com" 

def webpage_was_changed(): 
    """Returns true if the webpage was changed, otherwise false."""
    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36',
    'Pragma': 'no-cache', 'Cache-Control': 'no-cache'}
    response = requests.get(URL_TO_MONITOR, headers=headers)

    # create the previous_content.txt if it doesn't exist
    if not os.path.exists("previous_content.txt"):
        print("hello")
        open("previous_content.txt", 'w+').close()

    filehandle = open("previous_content.txt", 'r')
    previous_response_html = filehandle.read() 
    filehandle.close()

    if previous_response_html == response.text:
        return False
    else:
        filehandle = open("previous_content.txt", 'w')
        filehandle.write(response.text)
        filehandle.close()
        message = URL_TO_MONITOR
        title = "Webpage contents have changed!"
        command = f'''
        osascript -e 'display notification "{message}" with title "{title}"'
        '''
        os.system(command)
        return True

log = logging.getLogger(__name__)
logging.basicConfig(level=os.environ.get("LOGLEVEL", "INFO"), format='%(asctime)s %(message)s')
log.info("Running Website Monitor")
while True:
    if webpage_was_changed():
        log.info("WEBPAGE WAS CHANGED.")
    else:
        log.info("Webpage was not changed.")
    time.sleep(DELAY_TIME)