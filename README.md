# ptt-crawler

## 程式構想:<br>
首先設定欲爬文之版塊名稱，透過更改(line46)的range來決定<br>
要抓取幾頁的貼文<br>

## 迴圈的設定為:<br>
1. 點擊貼文(line49 to 55)<br>
2. 抓取貼文資料(line57 to 90)<br>
3. 上一頁(line92)<br>
4. 點擊下一篇貼文<br>

## 尚未解決的問題:<br>
-[]文末如果文章網址是綠色的，會中斷執行<br>
![範例](https://cdn.discordapp.com/attachments/679337498908033024/702419410085740675/unknown.png)<br>
-[]無法將公告剔除爬文<br>
-[]無法同時爬取有無非18歲條款的版塊<br>
