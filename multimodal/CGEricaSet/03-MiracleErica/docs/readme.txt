Unity Version 2020.3.33f1

起動時にコマンドライン引数に-selectrobot robotnameで自動でロボットを選ぶ
MiracleHuman.exe -selectrobot Erica

！注意！'='の間にスペースを入れてはならない
<通信方式>
本アプリがTCPサーバ（ port : 21000）で非同期通信を行う
コマンドのフッターは改行コード
文字コードはutf-8

<送信コマンド>
x,y,zで視線，顔，体を向ける座標を指定する
ロボットの正面方向がz軸，右がx軸，上がy軸の左手座標系でロボットの腰の下が原点，単位はメートル，translateSpeed(移動速度)は[m/sec]
priorityはfloatでデフォルトは0
反射的に視線を向ける場合とゆっくりトラッキングする場合とでpriorityを変えると吉

EyeController={"id": "EyeController","motionTowardObject": "","targetMotionMode": 2,"targetPoint": {"x": 0.0,"y": 1.2,"z": 1.5},"translateSpeed": 2.0,"translateTime": -1,"targetRotation": {"x":0.0,"y": 0.0,"z": 0.0},"rotateSpeed": 270,"rotateTime": -1,"keepTime": 0,"mode": 2,"gazeTracking": true,"priority": 0,"isBezierCurvePoint": false,"fingerData": []}\n
HeadController={"id": "HeadController","motionTowardObject": "","targetMotionMode": 2,"targetPoint": {"x": 0.0,"y": 1.2,"z": 1.5},"translateSpeed": 1.5,"translateTime": -1,"targetRotation": {"x":0.0,"y": 0.0,"z": 0.0},"rotateSpeed": 270,"rotateTime": -1,"keepTime": 0,"mode": 2,"gazeTracking": true,"priority": 0,"isBezierCurvePoint": false,"fingerData": []}\n
BodyController={"id": "BodyController","motionTowardObject": "","targetMotionMode": 2,"targetPoint": {"x": 0.0,"y": 1.2,"z": 1.5},"translateSpeed": 1.0,"translateTime": -1,"targetRotation": {"x":0.0,"y": 0.0,"z": 0.0},"rotateSpeed": 270,"rotateTime": -1,"keepTime": 0,"mode": 2,"gazeTracking": true,"priority": 0,"isBezierCurvePoint": false,"fingerData": []}\n

//ミニマル
EyeController={"id": "EyeController","motionTowardObject": "","targetMotionMode": 2,"targetPoint": {"x": 0.0,"y": 1.2,"z": 1.5},"translateSpeed": 2.0}\n
HeadController={"id": "HeadController","motionTowardObject": "","targetMotionMode": 2,"targetPoint": {"x": 0.0,"y": 1.2,"z": 1.5},"translateSpeed": 2.0}\n
BodyController={"id": "BodyController","motionTowardObject": "","targetMotionMode": 2,"targetPoint": {"x": 0.0,"y": 1.2,"z": 1.5},"translateSpeed": 2.0}\n

//見続けるには"tracking": true
set command=HeadController={"id": "HeadController","motionTowardObject": "monitor","tracking": true, "targetMotionMode": 2,"targetPoint": {"x":0,"y": 0,"z": 0},"translateSpeed": 2.0}\n


//左手をみつづける
//Enumは0スタート, From Object = 0, Toward Object = 1, On Object = 2
EyeController={"id": "EyeController","motionTowardObject": "LeftHand","targetMotionMode": 2,"tracking": true,"targetPoint": {"x": 0,"y": 0,"z": 0},"translateSpeed": 2.0,"translateTime": -1,"targetRotation": {"x": 0.0,"y": 0.0,"z": 0.0},"rotateSpeed": 270,"rotateTime": -1,"keepTime": 0,"mode": 2,"gazeTracking": true,"priority": 0,"isBezierCurvePoint": false,"fingerData": []}\n

//体の右前
EyeController={"id": "EyeController","motionTowardObject": "Spine","targetMotionMode": 2,"tracking": true,"targetPoint": {"x": 1,"y": 1,"z": 1},"translateSpeed": 2.0,"translateTime": -1,"targetRotation": {"x": 0.0,"y": 0.0,"z": 0.0},"rotateSpeed": 270,"rotateTime": -1,"keepTime": 0,"mode": 2,"gazeTracking": true,"priority": 0,"isBezierCurvePoint": false,"fingerData": []}


※Attractivenessの要素も追加できる
顔，体を向ける度合いを指定する(対象からそらす：-1.0~+1.0：対象に向ける)
BodyController={"attractiveness":0.5}\n
HeadController={"attractiveness":-0.5}\n

フルコマンド: transitionSpeedは変化速度[/sec]，transitionDurationは変化時間[msec]どちらかを指定すると線形でその時間かけて変化する，急激な変化を避けられる
{"attractiveness":-0.5, "transitionSpeed":0.1, "transitionDuration":5000}\n
BodyController={"attractiveness":1.0, "transitionDuration":5000}\n
HeadController={"attractiveness":-1.0, "transitionSpeed":1.0}\n


RightHandController={"id": "RightHandControllerDicrectControl","motionTowardObject": "","targetMotionMode": 2,"targetPoint": {"x": 0.25,"y": 0.8,"z": 0.5},"translateSpeed": 0.3,"translateTime": -1,"targetRotation": {"x": -90.0,"y": 0.0,"z": 0.0},"rotateSpeed": 270,"rotateTime": -1,"keepTime": 0,"mode": 2,"gazeTracking": true,"priority": 0,"isBezierCurvePoint": false,"fingerData": []}\n
LeftHandController={"id": "LeftHandControllerDicrectControl","motionTowardObject": "","targetMotionMode": 2,"targetPoint": {"x": -0.25,"y": 0.8,"z": 0.5},"translateSpeed": 0.3,"translateTime": -1,"targetRotation": {"x": -90.0,"y": 0.0,"z": 0.0},"rotateSpeed": 270,"rotateTime": -1,"keepTime": 0,"mode": 2,"gazeTracking": true,"priority": 0,"isBezierCurvePoint": false,"fingerData": []}\n
※指指定したいならば"fingerData": [{"motionPartName": "LeftIndexFinger","targetAngle": 0,"springValue": 10},{"motionPartName": "LeftFingers","targetAngle": 0,"springValue": 10}]

[指のみの動き]
part=Left/RightFingers, Left/RightIndexFinger, Left/RightSum
angle = 0~90, 90degs -> grasp
grasp={"motionPartName":"RightFingers", "targetAngle":90, "springValue":5}

[視線]
gazeavert={"pitch_degree":0.0, "yaw_degree":0.0, "speed":2.0}\n
float scale is degree, change automatically EyeController position, pitch_degree > 0 downward, <0 upward
gazeavert={"pitch_degree":10.0, "yaw_degree":10.0, "speed":2.0}

[サッケード]
サッケードを自動でするかしないか
saccade=true/false\n

[ジェスチャ]
playmotion=motionID\n
playmotion=motionA;...;motionB;\n
動きの速度をスケーリングするオプション，0.1（ゆっくり）~10.0（早い）
playmotion=motionA/0.1;...;motionB/10.0;\n

appendmotion=motionID\n
appendmotion=motionA;...;motionB;\n
※appendできるのは絶対動作のみ
getmotions\n -> motionid;motionid;.....;\n

指令後遅延してジェスチャを発動させる
delaytmotion={json};{json}...;{json};
delaymotion={"id":"greeting", "delay":5000, "speedScale":1.0};{"id":"righthandbeat", "delay":100}
delay=0でその瞬間でジェスチャを行う[msec]，speedScaleは速度のスケールで指定しないと1.0

ジェスチャにオフセットをかける
playoptionalmotion={json};{json}...;{json};
playoptionalmotion={"id":"right_hand_you", "delay":0, "speedScale":1.0, "translationOffset":{"x":0.5,"y":0.5,"z":0}, "rotationOffset":{"x":0.0,"y":0.0,"z":0.0}};


[未定義動作生成]
playthismotion={motion json}\n
appendthismotion={motion json}\n
・targetMotionMode: FromObject(0), FromRobot(1), OnObject(2), Beat(3), FromRobotHead(4), FromRobotSpine(5), MimicOnHead(6), MimicOnBody(7)
・mode: Lerp(0), Slerp(1)

(right palm up body controller)
targetMotionMode
playthismotion={"id":"right_hand_palmup_tmp","priority":0,"isRelative":false,"isGloablCoordinates":true,"motionPartName":"RightHandController","thoughSafetyStopoverPoint":false,"motionData":[{"id":"right_hand_palmup_tmp","motionTowardObject":"BodyController","targetMotionMode":1,"targetPoint":{"x":0,"y":0,"z":0.5},"translateSpeed":-1,"translateTime":850,"targetRotation":{"x":0,"y":90,"z":-90},"rotateSpeed":-1,"rotateTime":850,"keepTime":0,"mode":2,"gazeTracking":true,"priority":0,"tracking":true,"fingerData":[{"motionPartName":"RightIndexFinger","targetAngle":0,"springValue":10},{"motionPartName":"RightFingers","targetAngle":0,"springValue":10}]}]}

[未定義手動作生成]
playthishandmotion={handmotion json}\n
appendthishandmotion={handmotion json}\n

・transitionCoordinate: OnGlobal(0)世界座標系, OnRobot(1)SpringMan座標系, OnObject(2), FromObject(3), FromRobotHead(4), FromRobotSpine(5)
・rotationCoordinate: PalmNaturalUpward(0)//回転座標系で手のひらを上Y+方向, PalmNaturalDownward(1)//回転座標系で手のひらを下Y-方向, PalmNaturalSide(2)//回転座標系で手のひらを水平体の中心方向, PalmNaturalToward(3)//手のひらを対象方向Z+, PalmUpward(4)//回転座標系で手のひらを上Y+方向, PalmDownward(5)//回転座標系で手のひらを下Y-方向, PalmSide(6)//回転座標系で手のひらを水平体の中心方向, PalmToward(7)//手のひらを対象方向Z+
・motionDirectionTowardObject: motionTowardObjectは座標を決めるためで，もしその位置から別の対象に手を向ける場合にはこれで対象を指定する

(left hand shake body controller)
playthishandmotion={"id":"left_hand_palmside_tmp","priority":0,"isRelative":false,"isGloablCoordinates":true,"motionPartName":"LeftHandController","thoughSafetyStopoverPoint":false,"motionHandData":[{"id":"left_hand_palmside_tmp","motionTowardObject":"BodyController","transitionCoordinate": 5,"targetPoint":{"x":0,"y":0,"z":0.5}, "targetPosOnObject": {"x": 0,"y": 0,"z": 0},"translateSpeed":-1,"translateTime":850,"rotationCoordinate": 7,"targetRotation":{"x":0,"y":0,"z":0},"keepTime":0,"priority":0,"tracking":true,"fingerData":[{"motionPartName":"LeftIndexFinger","targetAngle":0,"springValue":10},{"motionPartName":"LeftFingers","targetAngle":0,"springValue":10}]}]}



K2BodyのObjectを使う場合（MimicGestureを作る場合）
TargetHuman/SubTargetHuman+Head/Spine/RightHand/LeftHand

[ターゲットHumanのIDの設定]
targethuman=4\n
subtargethuman=2\n

[マニュアルでロール姿勢を変えるコマンド，これを送れば自動でEmotion2Poseは止まる]
rollpose={"degree":float, "direction":"left/right", "samedirection":true/false, "rollspeed":float}\n
rollpose={"degree":5.0, "direction":"left", "samedirection":true, "rollspeed":20.0}\n
rollspeedを指定しないとデフォルトの速度になる[deg/sec]

[Emotion2Poseを再開・停止]
modulecontrol={"moduleName":"Emotion2Pose", "permit": true/false}\n

[Central pattern generator]
cpg={"scale":float>=0, "frequency":float>=0}\n
cpg={"scale":5, "frequency":2}\n

[内部状態の設定]
arousal=float\n
valence=float\n

[角度指定]
sethingejoint={"part":"objectname", "angle":double}\n
setconfigjoint={"part":"objectname", "angle":{"x":-1.0,"y":-0.5,"z":3.5}}\n

[モジュールのONOFF]
modulecontrol={"moduleName":"name", "permit": true/false}\n
ex;
modulecontrol={"moduleName":"Emotion2Pose", "permit": true/false}\n

[オブジェクトの追加削除]
位置・回転はGlobal
createobject={"id":"name", "scale":{"x":-1.0,"y":-0.5,"z":3.5}, "position":{"x":1.0,"y":0.5,"z":3.5}, "rotation":{"x":0,"y":0,"z":0}, "color":{"r":255,"g":255,"b":255,"a":255}, \"isLookTarget\":true, \"isPointingTarget\":true}
deleteobject={"id":"name"}
objectはCube一個で，isLookTarget=trueにすると人が見ているものの判定に含まれる，isPointingTarget=trueにすると人が指差しているものの判定に含まれる

[カメラ位置の変更]Motionと同じパラメータだけど使えないパラメータは指定しないこと
camera={"id": "Main Camera","motionTowardObject": "","targetMotionMode": 2,"targetPoint": {"x": 0.0,"y": 1.2,"z": 1.5},"translateSpeed": 1.0,"translateTime": -1,"targetRotation": {"x":0.0,"y": 0.0,"z": 0.0},"rotateSpeed": 270,"rotateTime": -1,"keepTime": 0,"mode": 2,"}\n
camera={"id": "Main Camera","motionTowardObject": "","targetMotionMode": 2,"targetPoint": {"x": 1.0,"y": 1.2,"z": 1.5},"translateTime": 1000, "targetRotation": {"x":0.0,"y": -135.0,"z": 0.0},"rotateTime": 1000}\n


<受信コマンド>
値が変わったときのみデータが送られてくる
[Kinectの情報と組み合わせたときのみ]
 [ユーザの視線情報]
　ロボットに対しての視線情報
　　HumanLookingTowardRobot={\"x\":" +float+",\"y\":" + float + ",\"z\":" + float+ ",\"layer2_x\":" + float + ",\"layer2_y\":" + float + ",\"layer2_z\":" + float+ "}\n");
　　HumanNotLookingTowardRobot
　その他ものに対しての視線情報
　　HumanLookingTowardObject={\"x\":" + float + ",\"y\":" + float + ",\"z\":" + float + ",\"layer2_x\":" + float + ",\"layer2_y\":" + float + ",\"layer2_z\":" + float + ",\"objectname\":" + "\""+string+ "\"" + "}\n"
　　HumanNotLookingTowardObject
　ユニークIDがついている人が見ている情報(見ていないとnone)
　	UniquePeopleGazeObject={\"uniquepeoplegazeobject\":[{"hid":4, "lookat":"SpringMan"}, {"hid":2, "lookat":"unique:4"}, {"hid":3, "lookat":"none"}]}
　ユニークIDがついている人が指差している情報(指していないとnone)
　	UniquePeoplePointObject={\"uniquepeoplepointobject\":[{"hid":4, "pointat":"SpringMan", "stable":true}, {"hid":2, "pointat":"unique:4", "stable":false}, {"hid":2, "pointat":"none"}]}
　	
　ロボットユーザの視線状態
　　EyeContactState=MUTUALGAZE/ROBOTLOOKSHUMAN/HUMANLOOKSROBOT/NONE
 [ユーザの動きに基づく危険状態検出]
　mainユーザが顔や手を近づけてきた状態
　　DangerousState=HUMANHEAD2ROBOTHEAD/HUMANRIGHTHAND2ROBOTHEAD/HUMANLEFTHAND2ROBOTHEAD/HUMANRIGHTHAND2ROBOTRIGHTHAND/HUMANRIGHTHAND2ROBOTLEFTHAND/HUMANLEFTHAND2ROBOTRIGHTHAND/HUMANLEFTHAND2ROBOTLEFTHAND/NONE 
　　
　　
<How to make gesture>
オブジェクトからの相対でジェスチャーを作る場合
向きは標準状態での向きをしていする
位置は2種類ありオブジェクトのローカル座標系での位置とオブジェクトからみた顔の向き（Look）をZ方向とした座標系


[State Streamer, remoto controllerとは別のポート]
State Streamer = {json}

Speaking Motion/Listening Motion=SpeechStart/SpeechEnd/SpeechPause

MentalState=arousal=float
MentalState=valence=float
MentalState=smoothed_arousal=float
MentalState=smoothed_valence=float
(視線を外したタイミングもストリーミング)
GazeAvert={"pitch":float, "yaw":float}


<その他注意点>
GreetingではRollを０にするとしゃきっと動作になる
