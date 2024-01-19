#爬ptt內文
import requests
import bs4
import os
def download(url,save_path):  #定義下載圖片函式
    print("正在下載圖片:",url)
    resqonse=requests.get(url)  #發起網絡請求，獲取圖片的二進制內容
    with open(save_path,"wb") as file:  #寫入圖片的二進制內容到文件
        file.write(resqonse.content)
    print("-"*30)  #分隔線
def main():  #主程式
    url="https://www.ptt.cc/bbs/Beauty/M.1698322162.A.AEA.html"  #自行輸入網址
    headers={
        "User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36",
        "cookie":"over18=1"
    }
    response=requests.get(url,headers=headers)  #發起請求，獲取網頁內容
    with open("data.html","w",encoding="utf-8") as f:  #寫入網頁內容到 data.html 文件
        f.write(response.text)  
    soup=bs4.BeautifulSoup(response.text,"html.parser")  #使用 Beautiful Soup 解析網頁內容
    #尋找標題
    spans=soup.find_all("span",class_="article-meta-value")
    print(spans[2].text)
    print("-"*30)
    #創建資料夾
    title=spans[2].text   #輸出第三個span標籤的文字內容
    dir_name=f"image/{title}"  #資料夾名稱是文章標題
    if not os.path.exists(dir_name):  #如果資料夾不存在，建立資料夾；如果存在則跳過
        os.makedirs(dir_name)
    
    #爬網頁中的圖片
    links=soup.find_all("a")  #找出所有的超連結標籤
    allow=["jpg","jpeg","png","gif"]  #允許的副檔名
    x=[]
    for img in links:  
        if img.find_parent(class_="push"):  #將父級元素帶有"push"的連結找出，這代表該連結來自於留言
            x.append(img.text)
    for link in links:
        href=link.get("href")  #取得連結
        if not href:  #如果不是連結就跳過
            continue
        if href in x:  #如果網址來自於留言，則跳過
            continue
        file_name=href.split("/")[-1]  #將網址中/後面的字串定義為名稱
        exception=href.split(".")[-1].lower()  #利用網址中.後面的字串分析出要的副檔名
        if exception in allow:
            print("url:",href)
            print("副檔名:",exception)
            download(href,f"{dir_name}/{file_name}")  #下載圖片並保存到指定目錄
if __name__=="__main__":  #如果主程式執行
    main()  #執行主程式
print("下載完畢")