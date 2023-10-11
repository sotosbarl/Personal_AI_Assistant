import cv2
import face_recognition
import pickle

# Function to load and encode a single image
def encode_face(image_path):
    image = cv2.imread(image_path)
    rgb_image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)  # Convert to RGB (face_recognition uses RGB images)
    face_encodings = face_recognition.face_encodings(rgb_image)
    if len(face_encodings) > 0:
        return face_encodings[0]  # Return the first face encoding if face is detected
    else:
        return None
print('kak')

# List of image paths for each known person, change with your picture files
known_people_images = ["maria.jpg", "sotiris.jpg","panos.jpg","panagiota.jpg"]

# Build the known_face_encodings list
known_face_encodings = []
for image_path in known_people_images:
    face_encoding = encode_face(image_path)
    print('image 1 ready')

    if face_encoding is not None:
        known_face_encodings.append(face_encoding)

# List of corresponding names for each known person
#change with the corresponding people in your pictures (this should be the same length as your pictures)
known_face_names = ["Maria", "Sotiris","Panos","Panagiota"]

data = {
    'encodings': known_face_encodings,
    'names': known_face_names
}

with open('known_faces.pkl', 'wb') as f:
    pickle.dump(data, f)

