音声認識プログラム GoogleSpeechRecognitionServer
これまではChromeアプリとして実装していましたが，本バージョンでは，ネット上に
サーバーを用意しました．

Chromeブラウザで下記のサイトにアクセスしてください．
https://hil-erica.github.io/GoogleSpeechAPI/speech_recognition.html

アクセスして表示された画面内の「話してみる」ボタンをクリックすると音声認識が開始します．

chrome://settings/content/microphone
にアクセスすれば，使用するマイクを設定できます．

認識結果と取得方法については，下記のサイトを参照してください．
https://hil-erica.github.io/GoogleSpeechAPI/

これまで対話ロボットコンペティションに参加された方で，これまでと同様の方法で（TCP経由で）認識結果を取得したい場合，上記サイトにも記載していますが，
Websocket TCP socket bridge Tool
を使用してください．画面内の　Websocket TCP socket bridge Tool　
をクリックすると，ソフトウェアを含んだアーカイブファイルがダウンロードされます．アーカイブを任意の場所で解凍してください．解凍されたフォルダ内の
Launcher2-TCPServer.bat
を起動してください（Chromeブラウザを起動しているPCと同じPC上で）．次に，ブラウザの画面内のconnectボタンをクリックしてください(アドレス記入欄はws://127.0.0.1:8000のまま）．
上記のLauncher2-TCPServerが，websocket経由で認識結果を取得して，TCP経由で認識結果を出力します（Launcher2-TCPServerが認識結果を転送します）．
この状態でChromeブラウザを起動しているPCの8888ポートにTCPで接続すると，認識結果を取得することができます．
プロトコルについては，上記サイトに記載しています．
readme_Launcher2-TCPServer.txtにも記載しています．





