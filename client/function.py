
from client.lib import *
def captureScreen(isBGR=True)->np.ndarray:
    ImageScreenshot = pyautogui.screenshot()

    if  isBGR:
        image = cv2.cvtColor(np.array(ImageScreenshot), cv2.COLOR_RGB2BGR)
    else:
        image= cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    return  image, image.shape[0],image.shape[1],image.shape[2]

def convert_numpy_to_bytes(numpy_value):
    return numpy_value.tobytes()

def convert_bytes_to_string(bytes_value):
    return bytes_value.decode("utf-8") 

def convert_numpy_to_string(numpy_value):
    return (numpy_value.tobytes()).decode("utf-8")

def convert_string_to_bytes(string_value ):
    return bytes(string_value, 'utf-8')        


def ExtractData(recv_msg):

    recv_msg_numpy = np.frombuffer(recv_msg,dtype=np.float32)

    mode            = int(recv_msg_numpy[0])
    width_buffer    = int(recv_msg_numpy[1])
    height_buffer   = int(recv_msg_numpy[2])
    shape           = int(recv_msg_numpy[3])

    recv_msg_numpy =recv_msg_numpy.reshape(-1,int(width_buffer))
    data_header = recv_msg_numpy[0:1,0:width_buffer]

    if mode== MODE_SENT.STRING.value:
        str_recrive= recv_msg_numpy[1:height_buffer+1,0:width_buffer].astype(dtype=np.uint8)
        data= str_recrive[0:1,0:int(shape)]       
        str_receive  = convert_numpy_to_string(data)
        return str_receive ,None
        
    elif mode== MODE_SENT.IMAGE.value:
        if shape ==3:
            img_channel_1= recv_msg_numpy[1:height_buffer+1,0:width_buffer].astype(dtype=np.uint8)
            img_channel_2= recv_msg_numpy[height_buffer+1:2*height_buffer+1,0:width_buffer].astype(dtype=np.uint8)
            img_channel_3= recv_msg_numpy[2*height_buffer+1:3*height_buffer+1,0:width_buffer].astype(dtype=np.uint8)

            img_receive  = cv2.merge((img_channel_1,img_channel_2,img_channel_3))
        elif shape==0:
            img_receive= recv_msg_numpy[1:height_buffer+1,0:width_buffer].astype(dtype=np.uint8)
        return None,img_receive

    elif mode== MODE_SENT.STRING_IMAGE.value:

        data_str_header = recv_msg_numpy[1:2,0:width_buffer]
        width_buffer    = int(data_str_header[0:,1:2])
        height_buffer   = int(data_str_header[0:,2:3])
        len_str_data    = int(data_str_header[0:,3:4])
        data= data_str_header[0:1,4:int(len_str_data)+4]  .astype(dtype=np.uint8)
        str_receive  = convert_numpy_to_string(data)

        if shape ==3:
            img_channel_1= recv_msg_numpy[2:height_buffer+2,0:width_buffer].astype(dtype=np.uint8)
            img_channel_2= recv_msg_numpy[height_buffer+2:2*height_buffer+2,0:width_buffer].astype(dtype=np.uint8)
            img_channel_3= recv_msg_numpy[2*height_buffer+2:3*height_buffer+2,0:width_buffer].astype(dtype=np.uint8)

            img_receive  = cv2.merge((img_channel_1,img_channel_2,img_channel_3))
        elif shape==0:
            img_receive= recv_msg_numpy[1:height_buffer+1,0:width_buffer].astype(dtype=np.uint8)

        return str_receive,img_receive
        

    cv2.imwrite("img_receive.png",img_receive)
    print(f'Receive Data Sucessfull ...')