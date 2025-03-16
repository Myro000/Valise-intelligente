import cv2

cap = cv2.VideoCapture(0)
if not cap.isOpened():
    print("Erreur : Impossible d'ouvrir la caméra.")
else:
    print("Caméra ouverte avec succès.")
    while True:
        ret, frame = cap.read()
        if not ret:
            print("Erreur : Impossible de lire l'image.")
            break
        cv2.imshow("Test Camera", frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):  # Quitter avec 'q'
            break

    cap.release()
    cv2.destroyAllWindows()
