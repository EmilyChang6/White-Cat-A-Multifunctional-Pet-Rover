# 多功能寵物自走車 - 白貓 Project   
<img src="https://github.com/EmilyChang6/White-Cat-A-Multifunctional-Pet-Rover/blob/main/%E7%99%BD%E8%B2%93.PNG" width="600"/>      
本專案以 Raspberry Pi 為核心，建立一套嵌入式系統應用，並將其連接至 Ubidots 平台。

## 主要分為三大功能 (以語音調控)： 
### A. 鬧鐘模式  
 (1) 選擇模式 1   
 (2) 輸入年/月/日   
 (3) 輸入完成按下 Enter 後，螢幕上會顯示距離使用者設定的時間還有多久  
 (4) 當設定的時間到時，鬧鐘響起且 Led 燈閃爍  
 (5) 使用者需透過手靠近光敏電阻，降低亮度才能關閉鬧鐘

### B. 互動模式  
 (1) 選擇模式 2  
 (2) 使用者可自由說一些指令，以下有三種互動：  
  * 「Go Away」：自走車利用超聲波測距避障礙物  
  * 「Come Here」：自走車轉圈  
  * 「Set Up」：回到初始選擇模式   
   
 ### C. 小夜燈模式  
   透過光敏電阻偵測數值 (當光線變暗時，小夜燈將會開啟)
