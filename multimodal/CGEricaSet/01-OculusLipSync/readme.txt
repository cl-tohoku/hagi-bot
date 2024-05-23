Unity Version 2019.4.16f1
LipSync version 20.0.0

'M'キーを押すとマイクを選択できる / Press the 'M' key to select the microphone.
入力音声に遅延がかかっていそうな場合は再度マイク選択すると解決する / If there seems to be a delay in the input sound, selecting the microphone again solves the problem.
'Space'キーでマイクをリフレッシュできる / The 'Space' key can be used to refresh the microphone.
Unityアプリを別途起動したときに遅延が生じるのかもしれない / The delay may occur when the Unity application is launched separately.


Streamingサンプル，0~1まで口の形の確率を表すだけ，prosodyInfoも追加 / Streaming samples, only probability of mouth shape from 0~1, also add prosodyInf
{"laughterScore":0.0,"sil":0.0,"PP":0.0,"FF":0.0,"TH":0.0,"DD":0.0,"kk":0.0,"CH":0.0,"SS":0.0,"nn":0.0,"RR":0.0,"aa":1,"E":0.0,"ih":0.0,"oh":0.0,"ou":0.0}
{"laughterScore":0.0,"sil":0.0,"PP":0.0,"FF":0.0,"TH":0.0,"DD":0.0,"kk":0.0,"CH":0.0,"SS":0.0,"nn":0.0,"RR":0.0,"aa":0,"E":0,"ih":1,"oh":0.0,"ou":0.0}
{"laughterScore":0.0,"sil":0.0,"PP":0.0,"FF":0.0,"TH":0.0,"DD":0.0,"kk":0.0,"CH":0.0,"SS":0.0,"nn":0.0,"RR":0.0,"aa":0,"E":0,"ih":0.0,"oh":0.0,"ou":1}
{"laughterScore":0.0,"sil":0.0,"PP":0.0,"FF":0.0,"TH":0.0,"DD":0.0,"kk":0.0,"CH":0.0,"SS":0.0,"nn":0.0,"RR":0.0,"aa":0,"E":1,"ih":0.0,"oh":0.0,"ou":0.0}
{"laughterScore":0.0,"sil":0.0,"PP":0.0,"FF":0.0,"TH":0.0,"DD":0.0,"kk":0.0,"CH":0.0,"SS":0.0,"nn":0.0,"RR":0.0,"aa":0,"E":0,"ih":0.0,"oh":1,"ou":0.0}

{"laughterScore":0.05707126,"sil":0.0001325802,"PP":0.0003985905,"FF":0.0006701589,"TH":6.462601E-05,"DD":0.001136577,"kk":0.003009429,"CH":1.72895E-05,"SS":0.0002111323,"nn":0.003264397,"RR":0.003018536,"aa":0.4687479,"E":0.002089644,"ih":0.0006006912,"oh":0.5164416,"ou":0.0001968694,"prosodyInfo":{"power":25.22232,"f0Hz":732.1289,"intonation":"NOTHING","semitioneDiff":-1,"intonationDuration":119,"speechFeature":"NONE","beat":false,"powerDiffAtBeat":1.997847}}

intonation: RISE, FLAT, FALL, NOTHING
speechFeature: FALLDOWN, RISEUP, NONE


sil～ouは0~1で口の形の推定値 / sil~ou is 0~1 and is an estimate of mouth shape
prosodyInfoは韻律特徴，順にdB, Hz, intonationは以下の4つのラベル（RISE, FLAT, FALL, NOTHING），semitioneDiffはintonation識別区間でのF0semitoneスケールでの変化量，intonationDurationはその区間時間msec，speechFeatureは以下の3つのラベル（FALLDOWN, RISEUP, NONE），beatは音圧ピーク検出，ピーク時の音圧の変化量dB / prosodyInfo is the prosody feature, in order dB, Hz, intonation is the following four labels (RISE, FLAT, FALL, NOTHING), semitioneDiff is the amount of change on the F0semitone scale in the intonation identification interval, and intonationDuration is the interval time in msec, speechFeature is the following three labels (FALLDOWN, RISEUP, NONE), beat is the sound pressure peak detection, and dB is the change in sound pressure at the peak.

---
サーバに
{"laughterScore":0.0,"sil":0.0,"PP":0.0,"FF":0.0,"TH":0.0,"DD":0.0,"kk":0.0,"CH":0.0,"SS":0.0,"nn":0.0,"RR":0.0,"aa":1,"E":0.0,"ih":0.0,"oh":0.0,"ou":0.0}\n
と送信し返すとしゃべり始めるまでその口をする
予備動作とかに利用
注意点，マニュアルで重みを送信したらAudioとの推定結果の和になる．なのでAudioではsil=1と判定されている
GUI上ではsil=1のままだけど，送信結果はそうじゃないから安心して

and send it back to the server, it will talk until it starts talking.
Used for preliminary actions and so on.
Note that if you send the weights manually, they will be the sum of the estimation results with Audio. So in Audio it is judged as sil=1.
In the GUI, sil=1, but not in the transmission result.
---


---
サーバに
r\n
と送信するとマイクをリセットする
実験前とかに送ると安心

Sending r\n to the server resets the microphone
It's safer to send it before an experiment or something.
---