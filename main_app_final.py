import pygame
import cv2
import speech_recognition as sr
from gtts import gTTS
from moviepy.editor import VideoFileClip
from bardapi import Bard
import random
import cv2
import face_recognition
import pickle

# Infrom bardapi import Barditialize the recognizer
recognizer = sr.Recognizer()

#Follow instructions on https://github.com/dsdanielpark/Bard-API to install Bard API and find your api.
credentials = '{replace_with_your_bard_api}'
# Create a BardClient object using the GoogleCredentials object.
token = credentials
bard = Bard(token=credentials)

people_seen = []


def speech2text():
    text =''
    with sr.Microphone() as source:
        print("Say something...")
        recognizer.adjust_for_ambient_noise(source)  # Optional: adjust for ambient noise
        audio = recognizer.listen(source)

    try:
        # Convert speech to text
        text = recognizer.recognize_google(audio, language='el')  # Language code for English (en) / greek (el)
        print("You said:", text)
    except sr.UnknownValueError:
        print("Could not understand audio.")
    except sr.RequestError as e:
        print("Error occurred; {0}".format(e))

    return text

def SpeakText(command):

#    Initialize the engine
    tts = gTTS(text=command, lang='en', slow=False)
    random_number = random.randint(1, 10000)

    tts.save("temp%s.mp3" %random_number)

    pygame.mixer.init()
    pygame.mixer.music.load("temp%s.mp3" %random_number)
    pygame.mixer.music.play()




# engine.runAndWait()
class TextBox:
    def __init__(self, x, y, width, height, font, color):
        self.rect = pygame.Rect(x, y, width, height)
        self.font = font
        self.color = color
        self.active = False
        self.text = ""

    def handle_event(self, event):
        text = self.text
        flag = False
        if event.type == pygame.KEYDOWN:

            try:

                text = speech2text()
                #text = input('question')
                Chatgpt(text)
                flag = True



            except sr.RequestError as e:
                print("Could not request results; {0}".format(e))

            except sr.UnknownValueError:
                print("unknown error occurred")

        return  flag, text

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, self.rect, 2)
        text_surface = self.font.render(self.text, True, self.color)
        screen.blit(text_surface, (self.rect.x + 5, self.rect.y + 5))


def resize_video_frame(frame, target_size):
    return pygame.transform.scale(frame, target_size)


def Chatgpt(question):

    # pygame.mixer.music.load(audio_path)
    # question = input("You:")
    # question += "be concise"
    answer = bard.get_answer(question)['content']
    text = answer.replace('*', '')
    SpeakText(text)

def See_person():

    # Capture video from the camera
    cap = cv2.VideoCapture(0)  # Use 0 for the default camera, or specify the camera index if you have multiple cameras

    # Load the known_face_encodings and known_face_names from the file
    with open('known_faces.pkl', 'rb') as f:
        data = pickle.load(f)

    known_face_encodings = data['encodings']
    known_face_names = data['names']
    flag = False

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        # Find face locations and face encodings in the frame
        face_locations = face_recognition.face_locations(frame)
        face_encodings = face_recognition.face_encodings(frame, face_locations)

        # Identify the person in the frame
        for face_encoding in face_encodings:
            # Compare the current face encoding to the known face encodings
            matches = face_recognition.compare_faces(known_face_encodings, face_encoding)

            # Check if there is a match
            name = "Unknown"
            if True in matches:
                match_index = matches.index(True)
                name = known_face_names[match_index]

            # Draw bounding box and label on the frame
            top, right, bottom, left = face_locations[0]
            cv2.rectangle(frame, (left, top), (right, bottom), (0, 255, 0), 2)
            cv2.putText(frame, name, (left, top - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.75, (0, 255, 0), 2)

            if name is not "Unknown":
                flag = True
                break

        if cv2.waitKey(1) & 0xFF == ord('q') or flag:
            break

    # Release the capture and close the window
    flag2 = True
    # SpeakText('Hello'+ name + "what can I do for you today?")
    for person in people_seen:


        if person == name:
            flag2 = False
            break

    if flag2:
        SpeakText('Hello' + name + "what can I do for you today?")
        people_seen.append(name)





def Video():
    font = pygame.font.Font(None, 32)

    text_box = TextBox(200, 200, 400, 40, font, (255, 255, 255))

    VIDEO_WIDTH, VIDEO_HEIGHT = 3840, 2160
    SCREEN_WIDTH, SCREEN_HEIGHT = 920, 540

    # Calculate scaling factors to fit the video inside the screen
    scale_factor = min(SCREEN_WIDTH / VIDEO_WIDTH, SCREEN_HEIGHT / VIDEO_HEIGHT)
    scaled_width, scaled_height = int(VIDEO_WIDTH * scale_factor), int(VIDEO_HEIGHT * scale_factor)
    letterbox_width = SCREEN_WIDTH - scaled_width
    letterbox_height = SCREEN_HEIGHT - scaled_height

    window = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    clock = pygame.time.Clock()
    video = cv2.VideoCapture("animation.mp4")
    video2= cv2.VideoCapture("animation2.mp4")
    # video_clip = VideoFileClip("animation.mp4")
    # first_frame = video_clip.get_frame(2)
    # video_clip.close()
    # image_path = "animation_pic.png" # Replace this with the path to your image file
    # my_image = first_frame
    # my_image = pygame.image.frombuffer(
    #     my_image.tobytes(), my_image.shape[1::-1], "RGB")
    # my_image = resize_video_frame(my_image, (SCREEN_WIDTH, SCREEN_HEIGHT))
    fps = video.get(cv2.CAP_PROP_FPS)
    # window.blit(my_image, (0, 0))
    success, video_image = video.read()
    video_surf = pygame.image.frombuffer(
        video_image.tobytes(), video_image.shape[1::-1], "BGR")

    run = True

    flag = False
    text = ''

    count = 1
    busy = 0

    while run:

        clock.tick(fps)
        count += 1
        busy += 1
        print('busy',busy)



        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

            text,flag = text_box.handle_event(event)


        if count == 10:
            See_person()

        if busy%400 == 0:
            See_person()


        if pygame.mixer.music.get_busy():

            busy = 0

            success, video_image = video.read()
            if not success:
                # If the video reaches its end, rewind back to the beginning
                video.set(cv2.CAP_PROP_POS_FRAMES, 0)
                success, video_image = video.read()

            video_surf = pygame.image.frombuffer(
                video_image.tobytes(), video_image.shape[1::-1], "BGR")

            video_surf = pygame.transform.scale(video_surf, (scaled_width, scaled_height))

            # Create a black surface as the background
            background = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
            background.fill((0, 0, 0))

            # Blit the video frame onto the center of the screen with letterboxing
            window.blit(background, (0, 0))
            window.blit(video_surf, (letterbox_width // 2, letterbox_height // 2))

            # window.blit(video_surf, (0, 0))
            flag = False
        else:

            success, video_image = video2.read()
            if not success:
                # If the video reaches its end, rewind back to the beginning
                video2.set(cv2.CAP_PROP_POS_FRAMES, 0)
                success, video_image = video2.read()

            video_surf = pygame.image.frombuffer(
                video_image.tobytes(), video_image.shape[1::-1], "BGR")

            video_surf = pygame.transform.scale(video_surf, (scaled_width, scaled_height))

            # Create a black surface as the background
            background = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
            background.fill((0, 0, 0))

            # Blit the video frame onto the center of the screen with letterboxing
            window.blit(background, (0, 0))
            window.blit(video_surf, (letterbox_width // 2, letterbox_height // 2))
            flag = False



        pygame.display.flip()

def main():


    Video()

if __name__ == "__main__":
    main()

pygame.quit()
exit()