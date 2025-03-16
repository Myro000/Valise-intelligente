import cv2
from ultralytics import YOLO
import numpy as np

# Charger le modèle YOLOv8 Nano
model = YOLO("../models/yolov8n.pt")  # Chemin correct pour accéder au modèle

# Initialisation de la capture vidéo
cap = cv2.VideoCapture(0)  #
if not cap.isOpened():
    print("Erreur : Impossible d'ouvrir la caméra.")
else:
    print("Caméra ouverte avec succès.")

# Variables de suivi
last_color_hue = None  # Teinte de la dernière personne suivie (initialement aucune)
person_tracked = False  # Indicateur de suivi de la personne
person_id = None  # Identifiant de la personne suivie
user_x1, user_x2 = None, None  # Coordonnées utilisateur
threshold_hue_diff = 10  # Seuil de différence de teinte pour décider si on change de personne suivie

def get_user_position(user_x1, user_x2, frame_width):
    if user_x1 is None or user_x2 is None:
        return None  # Aucune personne détectée
    x_centre = (user_x1 + user_x2) // 2
    if x_centre < frame_width // 3:
        return "gauche"
    elif x_centre > 2 * (frame_width // 3):
        return "droite"
    else:
        return "centre"

while True:
    ret, frame = cap.read()
    if not ret:
        print("Erreur : Impossible de lire l'image.")
        break

    frame_width = frame.shape[1]


    # Exécuter la détection avec YOLO
    results = model(frame)
    detections = results[0].boxes.data  # Récupérer les boîtes englobantes

    # Liste des personnes détectées
    persons = []
    for det in detections:
        x1, y1, x2, y2, conf, cls = det.tolist()
        if conf > 0.5 and cls == 0:  # Si c'est une personne (classe 0)
            persons.append((x1, y1, x2, y2, conf, cls))

    if len(persons) > 0:
        # Si aucune personne n'est suivie actuellement
        if not person_tracked:
            # Trouver la première personne et commencer à la suivre
            for person in persons:
                x1, y1, x2, y2, conf, cls = person

                # Extraire la région d'intérêt (ROI) pour chaque personne
                roi = frame[int(y1):int(y2), int(x1):int(x2)]  # Extraire la ROI

                # Calculer la couleur dominante de la ROI
                hsv_roi = cv2.cvtColor(roi, cv2.COLOR_BGR2HSV)  # Convertir en HSV
                hist = cv2.calcHist([hsv_roi], [0], None, [256], [0, 256])  # Histogramme pour la teinte
                dominant_hue = np.argmax(hist)  # Teinte dominante de la ROI

                # Enregistrer cette teinte comme la teinte de l'utilisateur
                last_color_hue = dominant_hue
                user_x1, user_x2 = x1, x2
                person_id = "utilisateur"  # Identifier la personne comme l'utilisateur
                print(f"Utilisateur détecté ! ID : {person_id}, Teinte : {last_color_hue}")

                # Marquer la personne comme suivie
                person_tracked = True
                break  # Arrêter la boucle, car on a déjà trouvé et suivi une personne

        # Si la personne est suivie, mettre à jour la teinte de la ROI
        else:
            # Comparer chaque personne détectée à la teinte de l'utilisateur
            user_found = False
            for person in persons:
                x1, y1, x2, y2, conf, cls = person
                roi = frame[int(y1):int(y2), int(x1):int(x2)]  # Extraire la ROI
                hsv_roi = cv2.cvtColor(roi, cv2.COLOR_BGR2HSV)  # Convertir en HSV
                hist = cv2.calcHist([hsv_roi], [0], None, [256], [0, 256])  # Histogramme pour la teinte
                dominant_hue = np.argmax(hist)  # Teinte dominante de la ROI

                # Si la teinte de la personne est proche de la teinte de l'utilisateur
                if abs(dominant_hue - last_color_hue) < threshold_hue_diff:
                    user_found = True
                    person_id = "utilisateur"  # L'identifiant de l'utilisateur est mis à jour
                    last_color_hue = dominant_hue  # Mise à jour de la teinte
                    user_x1, user_x2 = x1, x2

                    # Affichage visuel
                    cv2.rectangle(frame, (int(x1), int(y1)), (int(x2), int(y2)), (0, 255, 0),2)  # Dessiner Bboxes
                    cv2.putText(frame, f"Utilisateur ID: {person_id}, Teinte: {last_color_hue}",(int(x1), int(y1) - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
                    print(f"Suivi de l'utilisateur (ID: {person_id}) avec teinte mise à jour : {last_color_hue}")
                    break  # On arrête dès qu'on a trouvé l'utilisateur et mis à jour sa teinte

            if not user_found:
                print("Utilisateur perdu, recherche d'une nouvelle personne avec une teinte similaire.")

    else:
        # Si aucune personne n'est détectée
        print("Aucune personne détectée.")

    # Afficher l'image avec les détections
    cv2.imshow("Human Tracking", frame)

    # Quitter avec la touche 'q'
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Libération des ressources
cap.release() #Libère la caméra
cv2.destroyAllWindows() #Ferme toutes les fenêtres (pour la visualisation)
