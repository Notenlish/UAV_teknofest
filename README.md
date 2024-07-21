# UAV_teknofest

Contains the code for Starwing UAV team's 2024 teknofest fighter uav submission

Pathfinding(Dubins Curves)

![pathfinding](./pathfinding.png)

Credits to [Andrew Walker](https://github.com/AndrewWalker/Dubins-Curves) for the C implementation(that I converted to python)

## Project Roadmap:

# AI image detection

Need training data.

`...` [In progress] making a test training data by just placing red objects and recording them. WOOHOO!

# Algorithm

`-` Going to specified location

`+` Getting Video Feed from Jetson

`-` Give to yolov8 model

`-` Process results and determine if it found the person

`-` Moving in an spiral if havent

`-` Sending data to server if it has

[other uav]

`-` Going there and sending the medical supplies

# Software

`-` Making the whole system compatible with MAVProxy

# Testing

`+` Getting data from XPlane 11
`+` Parsing data from XPlane 11
`+` XPlaneConnect functionality
`-` Feeding to the system

# NOTE:

xplaneconnect should be downloaded as a compiled zip, just downlaoding the project source and putting it to plugins dir wont work.

# stuff

https://github.com/adderbyte/GYM_XPLANE_ML/issues/1
https://openreview.net/forum?id=S1lR6YT4nQ
https://forums.x-plane.org/index.php?/forums/topic/171171-machine-learning-gym_xplane-gym-environment-for-xplane/
https://openreview.net/pdf?id=H1mMHwt9X
https://github.com/nasa/XPlaneConnect

# Uçuş Kanıt Video Hazırlık

Bak usta yapmam gereken her şeyi buraya yazıcam.

### PZT 'ye kadar

[+] - UI'ı MAVProxy e taşı

[?] - MAVProxy hareket ettirme motor kontrolü(yaptım bişiler ama yani ucube bişi)

[ ] - Haberleşme menzil testleri(Ubiquiti) -> seed ile packet gönder, packetlerin kaçının bozulduğunu veya kaybolduğunu her iki cihazdan da aynı seed ile rastgele değerler üretip karşılaştırarak bul

[ ] - Haberleşme menzil testleri(telemetri) -> mavproxy nasıl haberleşme yapıyor ona bakmamız lazım

[ ] - UI'da uçağın ve ai uçağın haritada gösterimi

[ ] - Uçağın 1 dk boyunca bağlantı gelmezse başlangıç noktasına geri gelmesi(Uçak havada uçup gitmesin)

### Kalanlar

[ ] - UAV tespit YOLO modeli(dataset ztn olması lazım)

[ ] - XPlane 11 de test et.

[ ] - Rakip takip ve kilitlenme, yol bulma

[ ] - Kamikaze + diğer
