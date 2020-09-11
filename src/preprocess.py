import numpy as np
import cv2
import json
import os
import torch
import tqdm 


IMAGE_DIR="/home/aycaburcu/Masaüstü/Ford_Otosan_Intern/data/images"
#image klasörünün yolu değişkene atandı 
MASK_DIR="/home/aycaburcu/Masaüstü/Ford_Otosan_Intern/data/masks"
#masks klasörünün yolu değişkene atandı
batch_images=[]#boş liste oluşturuldu
image_path=[]#boş liste oluşturuldu
for name in os.listdir(IMAGE_DIR):
    image_path.append(os.path.join(IMAGE_DIR,name))
#IMAGE_DIR yolundaki klasörün içindeki dosyaların isimleri bir listeye kaydedildi 

mask_path=[]#boş bir liste oluşturuldu
for name in os.listdir(MASK_DIR):
    mask_path.append(os.path.join(MASK_DIR,name))
#MASK_DIR yolundaki klasörün içindeki dosyaların isimleri bir yoluyla birleştirilerek bir listeye kaydedildi

output_shape=[300,300]

def tensorize_image(image_path,output_shape):#2 parametreli fonksiyon oluşturuldu
    for image in tqdm.tqdm(image_path):#for döngüsü ile image_path listesinin içindeki elemanlara tek tek ulaşıldı
        img=cv2.imread(image)#image değişkenine atanmış dosya yolundaki,dosya okundu
        res=cv2.resize(img,tuple(output_shape))#image'a resize işlemi uygulandı 
        batch_images.append(res)#resize değiştirilmiş resimler listeye kaydedildi
    
    tensor_image = torch.as_tensor(batch_images)#yukarıda oluşturulan liste torch tensor'e çevrildi
    
    return tensor_image# tensor geri döndürüldü başka biryerde kullanmak için


batch_masks=[]#boş liste oluşturuldu

def tensorize_mask(mask_path,output_shape):#iki parametreye sahip function oluşturuldu
    
    for mask in tqdm.tqdm(mask_path):#mask_path listesinin elemanlarına tek tek ulaşıldı
        mask=cv2.imread(mask,0)#dosyalar okundu 
        #buradaki bir değişiklik (HXW) okundu 
        #mask = cv2.cvtColor(mask, cv2.COLOR_BGR2GRAY)    
        res_mask = cv2.resize(mask, tuple(output_shape))#image'in resize değiştirildi
       
        
       #one hot encode 
        n_classes=2#iki class olucak 1 ve 0 lardan oluşan 
        one_hot = np.zeros((300, 300, n_classes))#bir 0 lardan oluşan 300,300,2 lik numpy oluşturuldu
        for i, unique_value in enumerate(np.unique(res_mask)):
            #np.unique Bir dizinin benzersiz öğelerin indislerini verir 
            #benzersiz olan değerlerin bulup yerine 1 yazacaktır 
            one_hot[:, :, i][res_mask==unique_value] = 1
        batch_masks.append(one_hot)#her image'in one hot encode çevrilmiş hali listeye kaydedilir 
    
    tensor_mask=torch.as_tensor(batch_masks)#batch_masks torch tensore çevrildi
    
    return tensor_mask#tensor geri döndürüldü tekrar kullanım için 


tensorize_image(image_path,output_shape)#fonksiyon çağrıldı

tensorize_mask(mask_path,output_shape)#function çağrıldı 


