import os
import time
from ibm_watson import VisualRecognitionV3
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator

'''
DeprecationWarning: watson-developer-cloud moved to ibm-watson. 
To get updates, use the new package.
'''
class Image2Word():
    ''' For main program '''
    def _get_dirname_from_localtime(self):
        # year, month, day, hour, minute, second
        return "_".join([str(time.localtime()[i]) for i in range(0,6)])
    
    def img2word_singleImg(self, img_path, folder_name=None):
        self.setting_API()
        # Option(1): show result only
        #self.get_recog_words(img_path) # type: dict
        
        # Option(2): show result and save json file
        #self._save_json(img_path, folder_name)
        
        # Option(3): return texture for perparing csv data
        recog_words = self.get_recog_words(img_path)
        '''recog_words = self.get_recog_words(img_path).get("texture") # type: dict'''
        return recog_words
        
    def img2word_multipImgs(self, dir_path):
        folder_name = self._get_dirname_from_localtime()
        # If choose Option (3):
        textures_list = list()
        
        for f in os.listdir(dir_path):
            img_path = f"{dir_path}/{f}"
            # If choose Option (1)/(2):
            #self.img2word_singleImg(img_path, folder_name)
            
            # If choose Option (3): 
            # // Instead of print info for each img recong., each result info would collected to textures_list, and then print out the textures_list
            textures = self.img2word_singleImg(img_path, folder_name)
            textures_list.append(textures)
        
        # If choose Option (3):
        print("textures_list:")
        print(textures_list)
    
    def setting_API(self): 
        self.API_key = "5p6k57Ul0eleYgJKvgnE_39uIHI4brPd0_ON9W3UC22D"
        self.API_version = "2018-03-19"
        #self.service_url = "https://api.eu-de.visual-recognition.watson.cloud.ibm.com"
        self.service_url = "https://api.us-south.visual-recognition.watson.cloud.ibm.com/instances/0dfd12f6-c530-4ba5-b702-ec407e215885"  
        
        self.visual_recognition = VisualRecognitionV3(
            version = self.API_version,
            authenticator = IAMAuthenticator(self.API_key)
        )
        self.visual_recognition.set_service_url(self.service_url)
        
    def get_recog_words(self, img_path):
        # Prepare dict for result (json file)
        recog_words = dict()
        recog_words.setdefault("texture", list())
        recog_words.setdefault("color", list())
        
        # Read image
        #img_path = "./res/test/cloth_3.jpg" # for main program
        with open(img_path, "rb") as fp:
            classes = self.visual_recognition.classify(
                images_file=fp,
                threshold="0.6").get_result()
        
        # Extract words by API's classifier,
        # and then split into different features ('texture' & 'color')
        info = [dict_ele["class"] for dict_ele in classes["images"][0]["classifiers"][0]["classes"]]
        info = [word for word in info if word != "clothing" and word != "garment"]
        #print("info:", ", ".join(info), "\n")
        
        for word in info:
            if "color" not in word:
                recog_words["texture"].append(word)
            else:
                recog_words["color"].append(word)
        return recog_words
"""
if __name__ == "__main__":
    img2word = Image2Word()
    img2word.setting_API()
    img_path = "../res/lativ-test"  # PermissionError
    recog_words = img2word.get_recog_words(img_path)
    #print(recog_words)
"""