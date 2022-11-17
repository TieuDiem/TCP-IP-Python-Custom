
__all__ =[]
__doc__ ="""

Custom TCP/TP send and receive numpy array
- Size of buffer = (Width, Height) of screen shoot
{MODE} 
{Send_String}
        data_header[0,0:1] = MODE_SEND.STRING.value
        data_header[0,1:2] = Width of Image
        data_header[0,2:3] = Height of Image
        data_header[0,3:4] = len_str_data
        
        data_send = concat (data_header,data_convert_string_to_numpy)

{Send_Image}

        data_header[0,0:1] = MODE_SEND.IMAGE.value
        data_header[0,1:2] = Width of Image
        data_header[0,2:3] = Height of Image
        data_header[0,3:4] = Shappe of Image

        if Color Image: 
            data_send = concat (data_header,color_numpy_image)
        if Gray Image:
            data_send = concat (data_header,gray_numpy_image)

{Send_String_Image}
        data_str_header[0,0:1] = MODE_SEND.STRING.value
        data_str_header[0,1:2] = Width of Image
        data_str_header[0,2:3] = Height of Image
        data_str_header[0,3:4] = len_str_data

        data_img_header[0,0:1] = MODE_SEND.IMAGE.value
        data_img_header[0,1:2] = Width of Image
        data_img_header[0,2:3] = Height of Image
        data_img_header[0,3:4] = Shappe of Image

        data_send =concat(data_img_header,numpy_image)
        data_send =concat(data_str_header,data_send)

"""

from server.lib import *
from function import *

MODE_DATE_SENT  = MODE_SEND.STRING_IMAGE 

def create_server()->None:
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((HOST, PORT))
    server.listen(1)
    client, addr = server.accept()
    data = client.recv(100) 
    strData = data.decode("utf8")
    print(f'Data receive from client: {strData}')  
    while(True):
        if  strData !="START_CONNECTION":
            continue

        _ =input(f'Enter any key to sent data: ')
        data_send =None
        if MODE_DATE_SENT == MODE_SEND.IMAGE:
            isColor = False
            data_send,height_buffer,width_buffer,shape=captureScreen(isColor)

            data_header =np.zeros((1,width_buffer),dtype=np.float32)

            data_header[0,0:1] = MODE_SEND.IMAGE.value
            data_header[0,1:2] = width_buffer
            data_header[0,2:3] = height_buffer
            data_header[0,3:4] = shape
            if isColor:
                data_sent_split = cv2.split(data_send)

                data_send  =np.concatenate((data_sent_split[0],data_sent_split[1]),axis=0)
                data_send  =np.concatenate((data_send,data_sent_split[2]),axis=0)
                data_send  =np.concatenate((data_header,data_send),axis=0)
            else:
                data_send  =np.concatenate((data_header,data_send),axis=0)

        elif MODE_DATE_SENT == MODE_SEND.STRING:
            _,height_buffer,width_buffer,_=captureScreen(False)
            string_sent     =   "This is send string mode"
            bytes_sent      =   convert_string_to_bytes(string_sent)
            data_numpy, len_str_data    = convert_bytes_to_numpy(bytes_sent,(height_buffer,width_buffer))

            data_header =np.zeros((1,width_buffer),dtype=np.float32)
            data_header[0,0:1] = MODE_SEND.STRING.value
            data_header[0,1:2] = width_buffer
            data_header[0,2:3] = height_buffer
            data_header[0,3:4] = len_str_data

            data_send  =np.concatenate((data_header,data_numpy),axis=0)

        elif MODE_DATE_SENT == MODE_SEND.STRING_IMAGE:
            isColor =False
            data_send,height_buffer,width_buffer,shape=captureScreen(isColor)

            string_sent     =   "This Vayne Mai"
            bytes_sent      = convert_string_to_bytes(string_sent)
            data_numpy, len_str_data    = convert_bytes_to_numpy(bytes_sent,(height_buffer,width_buffer))
            
            data_str_header = np.zeros((1,width_buffer),dtype=np.float32)
            data_str_header[0,1:2] = width_buffer
            data_str_header[0,2:3] = height_buffer
            data = np.array(np.frombuffer(bytes_sent, dtype=np.uint8))
            data_str_header[0,3:4] = len(data)
            for i,item in enumerate(data):
                data_str_header [0:1,i+4:i+5]=item

            data_header =np.zeros((1,width_buffer),dtype=np.float32)
            data_header[0,0:1] = MODE_SEND.STRING_IMAGE.value
            data_header[0,1:2] = width_buffer
            data_header[0,2:3] = height_buffer
            data_header[0,3:4] = shape
            if isColor:
                data_sent_split = cv2.split(data_send)

                data_send  =np.concatenate((data_sent_split[0],data_sent_split[1]),axis=0)
                data_send  =np.concatenate((data_send,data_sent_split[2]),axis=0)
                data_send  =np.concatenate((data_str_header,data_send),axis=0)
                data_send  =np.concatenate((data_header,data_send),axis=0)             
            else:
                data_send  =np.concatenate((data_str_header,data_send),axis=0)
                data_send  =np.concatenate((data_header,data_send),axis=0)
        
        client.send(data_send)


if __name__ =="__main__":
    create_server()