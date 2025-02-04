from ultralyticsplus import YOLO, render_result

#_______________________________________________________________________________________________________

            # --------------------------------------------------
            # ----------------- FONCTIONS MODELE ---------------
            # --------------------------------------------------

# Fonction pour charger le modèle
def load_model(conf=0.25, max=1000):
    # load model
    model = YOLO('best.pt')

    # set model parameters
    model.overrides['conf'] = conf # 0.25  # NMS confidence threshold
    model.overrides['iou'] = 0.45  # NMS IoU threshold
    model.overrides['agnostic_nms'] = False  # NMS class-agnostic
    model.overrides['max_det'] = max # 1000  # maximum number of detections per image
    
    return model
