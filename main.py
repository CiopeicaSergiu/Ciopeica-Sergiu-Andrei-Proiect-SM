import speech_recognition as sr
import smtplib
import playsound
import bluetooth

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
             #playsound.playsound("/home/sergiu/PycharmProjects/TestSMV2/AudioFiles/comanda.mp3")
             print('Pronunta comanda!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!')
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


def connectToDevice(deviceName):
    target_address = None
    stop = False
   
    for i in range(0, 11):
        nearby_devices = bluetooth.discover_devices(duration=10, flush_cache=True)
        print(len(nearby_devices))
        for bdaddr in nearby_devices:
            if deviceName == bluetooth.lookup_name( bdaddr ):
                print('Found')
                target_address = bdaddr
                stop = True
                break
        if stop == True:
            break
        print(f"Retring {i}:.......................")



    return target_address

if __name__ == '__main__':
    
    deviceName = "HC-05"
    target_address = connectToDevice(deviceName)
    #target_address = "00:21:04:08:41:DB"
    if target_address is not None:
        print("found target bluetooth device with address "+target_address)
        port = 1
        sock=bluetooth.BluetoothSocket( bluetooth.RFCOMM )
        sock.connect((target_address, port))
        sock.send("stairs:4")
        m1 = MailSender()
        while True:
            msg = input("Continutul mesajului: ")
            m1.SendMail(msg)
            sock.send(msg)
        sock.close()

    else:
        print("could not find target bluetooth device nearby")

    
