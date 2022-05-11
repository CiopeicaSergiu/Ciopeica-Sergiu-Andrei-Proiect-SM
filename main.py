import speech_recognition as sr
import smtplib
import playsound

class MailSender:
    def __init__(self):
        self.__username = "atacatorul.atacatorul@gmail.com"
        self.__password = "atacatorul21121998"
        self.__server = smtplib.SMTP('smtp.gmail.com', 587)
        self.__sp = SpeechToText()

    def SendMail(self, msg):
        myFormat = f"""From: From Person <{self.__username}>
To: To Person <{self.__username}>
Subject: SMTP e-mail test

""" + msg
        text = self.__sp.RecognizeAudio()
        if text.lower() == "send":
            self.__server.starttls()
            self.__server.login(self.__username, self.__password)
            self.__server.sendmail(self.__username, self.__username, myFormat)
            self.__server.quit()
            print("Mesaj trimis cu succes")
        else:
            print(f'Eroare: {text}')

class SpeechToText:
    def __init__(self):
        self.__mic = sr.Microphone()
        self.__recognizer = sr.Recognizer()

    def __CaptureAudio(self):
        with self.__mic as source:
             playsound.playsound("/home/sergiu/PycharmProjects/TestSMV2/AudioFiles/comanda.mp3")
             self.__recognizer.adjust_for_ambient_noise(source, duration=1)


             audio = self.__recognizer.listen(source)
        return audio

    def RecognizeAudio(self):
        audio = self.__CaptureAudio()
        try:
            return self.__recognizer.recognize_google(audio)
        except sr.RequestError:
            return "Probleme cu api-ul!!"
        except sr.UnknownValueError:
            return "Nu inteleg nimic!"



if __name__ == '__main__':
    m1 = MailSender()
    msg = input("Continutul mesajului: ")
    m1.SendMail(msg)