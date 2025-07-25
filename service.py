# service.py
import torch.nn as nn
from torchvision import models
import bentoml
import torch
import torchvision.transforms as T
from PIL import Image
import numpy as np
import cv2

class ResizeWithReplicatePadding:
    def __init__(self, target_size):
        self.target_size = target_size

    def __call__(self, img):
        if not isinstance(img, Image.Image):
            raise TypeError("Input should be a PIL Image")

        w, h = img.size
        scale = self.target_size / max(w, h)
        new_w, new_h = int(w * scale), int(h * scale)
        img = img.resize((new_w, new_h), Image.BILINEAR)

        img_np = np.array(img)
        pad_w = self.target_size - new_w
        pad_h = self.target_size - new_h
        left = pad_w // 2
        right = pad_w - left
        top = pad_h // 2
        bottom = pad_h - top

        img_padded = cv2.copyMakeBorder(img_np, top, bottom, left, right, cv2.BORDER_REPLICATE)
        img_pil = Image.fromarray(img_padded)

        return img_pil

def create_enhanced_resnet(num_classes, pretrained=True):
    if pretrained:
        resnet = models.resnet50(weights='IMAGENET1K_V1')
    else:
        resnet = models.resnet50(weights=None)
    
    # Modify the final classifier with dropout for regularization
    resnet.fc = nn.Sequential(
        nn.Dropout(0.5),
        nn.Linear(resnet.fc.in_features, 512),
        nn.ReLU(),
        nn.Dropout(0.3),
        nn.Linear(512, num_classes)
    )
    
    # Fine-tune more layers for diatom-specific features
    # Unfreeze the last two residual blocks
    for param in resnet.parameters():
        param.requires_grad = False
    
    # Unfreeze layer4 (last residual block) and fc
    for param in resnet.layer4.parameters():
        param.requires_grad = True
    for param in resnet.fc.parameters():
        param.requires_grad = True
    
    return resnet

def predict_image(img,model,transform,device,classes):    
    # This is important! Puts the model in inference mode, which changes the behaviour
    # of certain layers
    img_tensor = transform(img)
    img_tensor = torch.stack([img_tensor])
    img_tensor = img_tensor.to(device)    
    with torch.no_grad():        
        output = model(img_tensor)
        _,preds = torch.max(output,dim=1)
        return classes[preds.item()]

@bentoml.service(
    image=bentoml.images.Image(python_version="3.12"),
)
class MyResNet:    
    def __init__(self) -> None:
        
        self.model_doa = create_enhanced_resnet(2, pretrained=True)
        state_dict_doa = torch.load("doa_diatom_model.pth")
        self.model_doa.load_state_dict(state_dict_doa)
        self.model_doa.eval()
        
        self.model_species = create_enhanced_resnet(4, pretrained=True)
        state_dict_species = torch.load("enhanced_diatom_model_cpu.pth")
        self.model_species.load_state_dict(state_dict_species)
        self.model_species.eval()
        
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        # self.model = create_enhanced_resnet(2,pretrained=True)        
        self.processor = T.Compose([
            ResizeWithReplicatePadding(target_size=224),
            T.ToTensor(),
            T.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225])
        ])        

    @bentoml.api(batchable=False)
    async def classify_doa(self, image: Image.Image) -> str:
        return predict_image(image, self.model_doa, self.processor, self.device, ['alive','dead'])        
    
    @bentoml.api(batchable=False)
    async def classify_species(self, image: Image.Image) -> str:
        return predict_image(image, self.model_species, self.processor, self.device, ['gomphonema','hannea','nitzschia','nocell'])
    
    @bentoml.api(batchable=False)
    async def classify_both(self, image: Image.Image) -> str:
        species = predict_image(image, self.model_species, self.processor, self.device, ['gomphonema','hannea','nitzschia','nocell'])
        if species == 'nocell':
            return f"{species}_dead"
        else:
            doa = predict_image(image, self.model_doa, self.processor, self.device, ['alive','dead'])        
        return f"{species}_{doa}"

