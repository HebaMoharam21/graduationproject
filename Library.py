import models as ml
import torch
import cv2
import os
from torchvision import transforms
import numpy as np
import requests
import classes as cl

def Transform():
    transformm = transforms.Compose([
        transforms.ToTensor(),
        transforms.Resize((32, 32)),
        transforms.Grayscale(num_output_channels=1)
    ])
    return transformm

def predict(cropped_obj, model, transform,classes):
        img_normalized = transform(cropped_obj)
        img_normalized = img_normalized.unsqueeze(0)
        with torch.no_grad():
            model.eval()
            output = model(img_normalized)
            index = output.argmax(dim=1).item()
            class_name = classes[index]
            #plt.imshow(cropped_obj, cmap='gray')
            # plt.title(class_name)
            # plt.show()
            return class_name
        
def predictCroppedAreas(image , binary_image, start_point, end_point, model):
        pred_list = []
        transform = Transform()
        classes = ('Arrow', 'GreaterThan', 'LessThan', 'Or', 'Other', 'UnKnown')
        
        predictions_crops = []
        for i in range(len(start_point) - 1):
            contours, _ = cv2.findContours(binary_image[start_point[i]:end_point[i + 1]], cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
            sorted_ctrs = sorted(contours, key=lambda ctr: cv2.boundingRect(ctr)[0])
            contoured_image = cv2.cvtColor(image[start_point[i]:end_point[i+1]], cv2.COLOR_GRAY2BGR)
            output_dir = "extracted_objectass"
            if not os.path.exists(output_dir):
               os.makedirs(output_dir)
            line_pred = []
            pred = []
            for j,ctr in enumerate(sorted_ctrs):
                x, y, w, h = cv2.boundingRect(ctr)
                y = y + start_point[i]
                obj = image[y:y + h, x:x + w]
                cv2.imwrite(os.path.join(output_dir, f"{i}_object_{j}.png"), obj)
                # cv2.drawContours(contoured_image, contours, -1, (0, 255, 0), 2)
                # cv2.imshow("s",obj)
                # cv2.waitKey(0)
                # cv2.imwrite(os.path.join(output_dir, f"{i}_object_{ctr}.png"), obj)
                try:
                    prediction = predict(obj, model, transform, classes)
                except Exception as e:
                    print(f"Prediction failed: {e}")
                    
                line_pred.append(prediction)
                pred.append((prediction,obj))
                #image_with_rect = cv2.rectangle(image.copy(), (x, y), (x + w, y + h), color=(0, 255, 0), thickness=2)
            pred_list.append(line_pred)
            predictions_crops.append(pred)
            # cv2.drawContours(contoured_image, contours, -1, (0, 255, 0), 2)
            # cv2.imshow("s",contoured_image)
            # cv2.waitKey(0)
        return predictions_crops, pred_list

def segmentandpredict(image_path):
    
    
    model = ml.NetWidth()
    
    #model.load_state_dict(torch.load(r"D:\Users\HP\Downloads\epoch199.pt"))
    model.load_state_dict(torch.load(r"C:\Users\HP.DESKTOP-J622CV6\project\codes\MyCodes\newOM2\epoch193.pt"))
    
    
    image = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
    _, binary_image = cv2.threshold(image, 128, 255, cv2.THRESH_BINARY_INV)
    bin_image = binary_image / 255
    histogram = np.sum(bin_image, 1)
    mask = np.where(histogram > 0, 255, 0)
    start_point = [0]
    end_point = []

    for i in range(1, binary_image.shape[0]):
        if mask[i] == 255 and mask[i - 1] == 0:
            end_point.append(i)
        elif mask[i] == 0 and mask[i - 1] == 255:
            start_point.append(i)
            
    end_point.append(binary_image.shape[0])
    predictions_crops, pred_list = predictCroppedAreas(image,binary_image,start_point,end_point,model)
    return predictions_crops, pred_list


def predictLetters (cropped_obj , model, transform, classes):
        img_normalized=transform(cropped_obj)
        img_normalized=img_normalized.unsqueeze(0)
        with torch.no_grad():
            model.eval()
            output=model(img_normalized)
            index=output.argmax(dim=1).item()
            class_name=classes[index]
            return (class_name)
        

def forParser(predictions_crops,predicted_images):
    
    model2=ml.Net_width()

    classes2 = ('0','1','2','3','4','5','6','7','8','9','A','B','C','D','E','F','G','H','I','J','K','L','M','N','O'
              ,'P','Q','R','S','T','U','V','W','X','Y','Z','a','b','c','d','e','f','g','h','i'
              ,'j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z')
    # model2_url="https://github.com/HebaMoharam21/Graduation-Project/blob/main/epoch699.pt"
    # response = requests.get(model2_url)
    # with open('epoch699.pt', 'wb') as f:
    #     f.write(response.content)
    #model2.load_state_dict(torch.load(r"C:\Users\HP.DESKTOP-J622CV6\project\codes\MyCodes\rate__\epoch699.pt"))
    model2.load_state_dict(torch.load(r"C:\Users\HP.DESKTOP-J622CV6\project\codes\MyCodes\rate__\epoch699.pt"))

    transform = Transform()
    Gram = cl.Grammar('S')

    for l , line in enumerate(predicted_images):
        if 'Arrow' not in line:
           continue
        arrow_index = line.index('Arrow')
        lhs=None
        for i,label in enumerate(line[:arrow_index]):
             if line[i] == "LessThan" : 
                 for j in range(i+1,arrow_index):
                     if line[j] == "Other":
                        letter_prediction = predictLetters(predictions_crops[l][i+1][1], model2,transform,classes2)
                        lhs = cl.NonTerminal(letter_prediction)
                        if lhs not in Gram.get_NonterminalList():
                            Gram.addNonterminal(lhs)
                        break 
        rhs=cl.RHS()
        #RList=[]
        z=0
        for i  in range(arrow_index+1 , len(line)):
            if(z>0):
              z-=1
              continue
            
            if line[i] == "UnKnown":
                continue
            elif line[i] == "LessThan" and line[i + 2] == "GreaterThan":
                if line[i + 1] == "Other":
                    letter_prediction = predictLetters(predictions_crops[l][i+1][1], model2,transform,classes2)
                    nonterm = cl.NonTerminal(letter_prediction)
                    rhs.add(nonterm)
                    if nonterm not in Gram.get_NonterminalList():
                        Gram.addNonterminal(nonterm)
                    z+=2
            elif line[i] == "Other":
                letter_prediction = predictLetters(predictions_crops[l][i][1], model2,transform,classes2)
                term = cl.Terminal(letter_prediction)
                rhs.add(term)
                if term not in Gram.get_TerminalList():
                    Gram.addTerminal(term)
            elif line[i]=='Or':
                prule = cl.ProductionRule(lhs,rhs)
                Gram.addRule(prule)
                prule.print_rule()
                rhs=cl.RHS()
                #print(RList)
                #rhs.add(RList)
                #RList=[]
        prule = cl.ProductionRule(lhs,rhs)
        prule.print_rule()
        Gram.addRule(prule) 
    Gram.print_rules()
    return Gram

def check_image_orientation(image_array):
        height, width = image_array.shape[:2] 
        if height > width:
            return "Vertical"
        else:
            return "Horizontal"
        
def ParseWords (Gram , text):
    parser= cl.Parser(Gram,text)
    parser.Gram = Gram
    parser.text = text
    result = parser.LL1Parse(Gram)
    return result


        






