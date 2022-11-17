
from server.lib import *
def captureScreen(isBGR=True)->np.ndarray:
    ImageScreenshot = pyautogui.screenshot()

    if  isBGR:
        image = cv2.cvtColor(np.array(ImageScreenshot), cv2.COLOR_RGB2BGR)
    else:
        image= cv2.cvtColor(np.array(ImageScreenshot), cv2.COLOR_BGR2GRAY)
    if (len(image.shape)==3):
        return  image, image.shape[0],image.shape[1],image.shape[2]
    else:
        return image, image.shape[0],image.shape[1],0
def convert_numpy_to_bytes(numpy_value):
    return numpy_value.tobytes()

def convert_bytes_to_string(bytes_value):
    return bytes_value.decode("utf-8") 

def convert_numpy_to_string(numpy_value):
    return (numpy_value.tobytes()).decode("utf-8")

def convert_string_to_bytes(string_value ):
    return bytes(string_value, 'utf-8')      


def convert_bytes_to_numpy(bytes_value,size):
    data = np.array(np.frombuffer(bytes_value, dtype=np.uint8))
    mask = np.zeros(size, dtype=np.uint8)
    for i,item in enumerate(data):
        mask [0:1,i:i+1]=item
    return mask,len(data)