from ultralytics import YOLO
import cv2
from ensemble_boxes import * 
from ultralytics.utils.plotting import Annotator, colors, save_one_box
from copy import deepcopy
import numpy as np
from .apps import EggsConfig


def imgplot(img, pred_boxes, labels, scores, names):
    line_width=None
    font_size=None
    font='Arial.ttf'

    annotator = Annotator(
            deepcopy(img),
            line_width,
            font_size,
            font,
            False, 
            example=names)
    
    if len(pred_boxes):
        for i,d in enumerate(pred_boxes):
            d = np.array(d)
            c, conf, id = int(labels[i]), float(scores[i]), None
            name = ('' if id is None else f'id:{id} ') + names[c]
            label = (f'{name} {conf:.2f}' if conf else name)
            # print(d.squeeze())
            annotator.box_label(d.squeeze(), label, color=colors(c, True))

    return annotator.result()

def xyntoxy(box_list, img_shape):
    new_box_list = []
    for box in box_list:
        x1,y1,x2,y2 = box
        new_box = [x1*img_shape[1],y1*img_shape[0],x2*img_shape[1],y2*img_shape[0]]
        new_box_list.append(new_box)
    return new_box_list
    

def ensembleResult(image):
    iou_thr = 0.5
    skip_box_thr = 0.0001
    sigma = 0.1
    weights = [1,1,3]
    
    model_list = [EggsConfig.sv_model,EggsConfig.kh_model,EggsConfig.dh_model]
    results = []
    names = {}
    for model in model_list:
        result = model.predict(image)
        results.append(result)

    
    for i, (r1,r2,r3) in enumerate(zip(results[0], results[1], results[2])):
        # print(r1)
        # print(r1.boxes)
        names = r1.names
        names[3] = "FS"
        r2.names[3] = "FS"
        r3.names[3] = "FS"
        result = [r1,r2,r3]
        scores_list = []
        labels_list = []
        boxes_list = []
        
        for r in result:
            r_score = r.boxes.conf.cpu().numpy()
            r_cls = r.boxes.cls.cpu().numpy()
            r_bbox = r.boxes.xyxyn.cpu().numpy()

            scores_list.append(r_score)
            labels_list.append(r_cls)
            boxes_list.append(r_bbox)
            
        orig_shape = r1.orig_shape
        img = r1.orig_img
        # r1_o_plot = r1.plot()
        # r2_o_plot = r2.plot()
        # r3_o_plot = r3.plot()

        # cv2.imwrite(f"./result/test_{i}_r1.jpg",r1_o_plot)
        # cv2.imwrite(f"./result/test_{i}_r2.jpg",r2_o_plot)
        # cv2.imwrite(f"./result/test_{i}_r3.jpg",r3_o_plot)

        # print(boxes_list)
        # print(scores_list)
        # print(labels_list)
        if len(boxes_list[0]) or len(boxes_list[1]) or len(boxes_list[2]):
            #NMS
            # boxes, scores, labels = nms(boxes_list, scores_list, labels_list, weights=weights, iou_thr=iou_thr)
            # boxes = xyntoxy(boxes, orig_shape)
            # nms_i = imgplot(img=img,pred_boxes=boxes,labels=labels, scores=scores, names=names)
            # cv2.imwrite(f"./result/test_{i}_nms.jpg",nms_i)
            # print(boxes)
            # print(scores)
            # print(labels)
        
            #SOFT_NMS
            # boxes, scores, labels = soft_nms(boxes_list, scores_list, labels_list, weights=weights, iou_thr=iou_thr, sigma=sigma, thresh=skip_box_thr)
            # boxes = xyntoxy(boxes, orig_shape)
            # soft_nms_i = imgplot(img, boxes,labels,scores, names)
            # cv2.imwrite(f"./result/test_{i}_snms.jpg",soft_nms_i)

            #Non_maximum_weighted
            # boxes, scores, labels = non_maximum_weighted(boxes_list, scores_list, labels_list, weights=weights, iou_thr=iou_thr, skip_box_thr=skip_box_thr)
            # boxes = xyntoxy(boxes, orig_shape)
            # non_mw_i = imgplot(img, boxes, labels, scores, names) 
            # cv2.imwrite(f"./result/test_{i}_nmw.jpg",non_mw_i)

            #Weighted_boxes_fusion
            boxes, scores, labels = weighted_boxes_fusion(boxes_list, scores_list, labels_list, weights=weights, iou_thr=iou_thr, skip_box_thr=skip_box_thr)
            boxes = xyntoxy(boxes, orig_shape)
            wbf_i = imgplot(img, list(reversed(boxes)), list(reversed(labels)), list(reversed(scores)), names)
            # cv2.imwrite(f"./result/test_{i}_wbf.jpg",wbf_i)
            return wbf_i
    

        