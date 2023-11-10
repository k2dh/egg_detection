from ultralytics import YOLO
import cv2
from ensemble_boxes import * 
from ultralytics.utils.plotting import Annotator, colors, save_one_box
from copy import deepcopy
import numpy as np
from .apps import EggsConfig


def imgplot(img, pred_boxes, names):
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
        for d in (reversed(pred_boxes)):
            box = np.array(d[2])
            c, conf, id = int(d[0]), float(d[1]), None
            name = ('' if id is None else f'id:{id} ') + names[c]
            label = (f'{name} {conf:.2f}' if conf else name)
            # print(d.squeeze())
            annotator.box_label(box.squeeze(), label, color=colors(c, True))

    return annotator.result()

def IoU(box1, box2):
    # intersection_over_union
    # box = (x1, y1, x2, y2)
    # box1_area = (box1[2] - box1[0] + 1) * (box1[3] - box1[1] + 1)
    # box2_area = (box2[2] - box2[0] + 1) * (box2[3] - box2[1] + 1)
    box1_area = (box1[2] - box1[0]) * (box1[3] - box1[1])
    box2_area = (box2[2] - box2[0]) * (box2[3] - box2[1])

    # obtain x1, y1, x2, y2 of the intersection
    x1 = max(box1[0], box2[0])
    y1 = max(box1[1], box2[1])
    x2 = min(box1[2], box2[2])
    y2 = min(box1[3], box2[3])

    # compute the width and height of the intersection
    # w = max(0, x2 - x1 + 1)
    # h = max(0, y2 - y1 + 1)
    w = max(0, x2 - x1)
    h = max(0, y2 - y1)

    inter = w * h
    iou = inter / (box1_area + box2_area - inter)
    # print(inter, box1_area + box2_area - inter)

    return iou

def clsrm(bboxes, iou_threshold):
    # bbox: [class, score, [x1, y2, x2, y2], .... ]

    # bboxes = [box for box in bboxes if box[1] > threshold]
    bboxes = sorted(bboxes, key=lambda x: x[1], reverse=True)
    bboxes_after_nmn = []

    while bboxes:
        chosen_box = bboxes.pop(0)

        # bboxes = [box for box in bboxes if box[0] != chosen_box[0] \
        #           or IoU(chosen_box[2], box[2]) < iou_threshold]
        current_bboxes = []
        for box in bboxes:
            if IoU(chosen_box[2], box[2]) > iou_threshold:
                pass
            else:
                current_bboxes.append(box)
        bboxes = current_bboxes

        bboxes_after_nmn.append(chosen_box)

    return bboxes_after_nmn

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
        
        if len(boxes_list[0]) or len(boxes_list[1]) or len(boxes_list[2]):
            # #NMS
            # boxes, scores, labels = nms(deepcopy(boxes_list), deepcopy(scores_list),labels_list, weights=weights, iou_thr=iou_thr)
            # boxes = xyntoxy(boxes, orig_shape)
            # nested = clsrm(list(zip(labels, scores, boxes)),iou_threshold=iou_thr)
            # nms_i = imgplot(img=img, pred_boxes=nested, names=names)
            # cv2.imwrite(f"./result/test_{i}_nms.jpg",nms_i)
            # # print(boxes)
            # # print(scores)
            # # print(labels)
        
            # #SOFT_NMS
            # s_boxes, s_scores, s_labels = soft_nms(deepcopy(boxes_list), deepcopy(scores_list), labels_list, weights=weights, iou_thr=iou_thr, sigma=sigma, thresh=skip_box_thr)
            # s_boxes = xyntoxy(s_boxes, orig_shape)
            # nested = clsrm(list(zip(s_labels, s_scores, s_boxes)),iou_threshold=iou_thr)
            # soft_nms_i = imgplot(img, nested, names)
            # cv2.imwrite(f"./result/test_{i}_snms.jpg",soft_nms_i)

            # #Non_maximum_weighted
            # n_boxes, n_scores, n_labels = non_maximum_weighted(deepcopy(boxes_list), deepcopy(scores_list), labels_list, weights=weights, iou_thr=iou_thr, skip_box_thr=skip_box_thr)
            # n_boxes = xyntoxy(n_boxes, orig_shape)
            # nested = clsrm(list(zip(n_labels, n_scores, n_boxes)),iou_threshold=iou_thr)
            # non_mw_i = imgplot(img, nested, names) 
            # cv2.imwrite(f"./result/test_{i}_nmw.jpg",non_mw_i)

            #Weighted_boxes_fusion
            w_boxes, w_scores, w_labels = weighted_boxes_fusion(deepcopy(boxes_list), deepcopy(scores_list), labels_list, weights=weights, iou_thr=iou_thr, skip_box_thr=skip_box_thr)
            w_boxes = xyntoxy(w_boxes, orig_shape)
            nested = clsrm(list(zip(w_labels, w_scores, w_boxes)),iou_threshold=iou_thr)
            wbf_i = imgplot(img, nested, names)
            # cv2.imwrite(f"./result/test_{i}_wbf.jpg",wbf_i)
            return wbf_i
    

        