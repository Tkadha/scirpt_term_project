from tkinter import *
from tkinter import ttk
from baseball import BaseBall
from soccer import Soccer
from tennis import Tennis
from PIL import Image, ImageTk
import requests
from io import BytesIO
import spam
import teller
import threading
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
class MainGUI():
    def __init__(self):
        self.All_list = BaseBall.baseball_lists + Soccer.soccer_lists + Tennis.tennis_lists
        self.All_list = sorted(self.All_list, key=lambda x: x[0])

        self.window = Tk()
        self.window.title("Sport Finder")
        self.window.geometry("800x800")  # 창 크기를 늘립니다.
        self.window.configure(bg='ivory')

        # Create the tab control
        self.tab_control = ttk.Notebook(self.window)
        self.tab_control.place(x=10, y=10, width=780, height=780)  # Adjust the size and position as needed

        # First tab with all the existing content
        self.first_tab = Frame(self.tab_control)
        self.first_tab.configure(bg='ivory')
        self.tab_control.add(self.first_tab, text='스포츠 파인더')

        # Second tab which is an empty frame
        self.second_tab = Frame(self.tab_control)
        self.second_tab.configure(bg='ivory')
        self.tab_control.add(self.second_tab, text='길찾기')

        # Move the existing content to the first tab
        self.setup_first_tab()
        self.setup_second_tab()
        self.bot = teller.SportFinderBot()
        self.bot_thread_flag = threading.Event()
        # 텔레그램 실행 버튼 생성
        self.telegram_button_img = PhotoImage(file="image/telegram.png")
        self.telegram_button = Button(self.first_tab, image=self.telegram_button_img, command=self.telegram)
        self.telegram_button.place(x=625, y=270, width=50, height=50)

        # Gmail 실행 버튼 생성
        self.email_button_img = PhotoImage(file="image/gmail.png")
        self.email_button = Button(self.first_tab, image=self.email_button_img, command=self.send_email)
        self.email_button.place(x=512.5, y=270, width=50, height=50)

        self.window.mainloop()

    def setup_second_tab(self):
        # Frame for inputting start and end locations
        directions_frame = Frame(self.second_tab)
        directions_frame.place(x=10, y=10, width=350, height=100)

        # Labels and entry widgets for start and end locations
        Label(directions_frame, text="출발지: ").grid(row=0, column=0, padx=5, pady=5)
        self.start_var = StringVar()
        Entry(directions_frame, textvariable=self.start_var, width=30).grid(row=0, column=1, padx=5, pady=5)

        Label(directions_frame, text="도착지: ").grid(row=1, column=0, padx=5, pady=5)
        self.end_var = StringVar()
        Entry(directions_frame, textvariable=self.end_var, width=30).grid(row=1, column=1, padx=5, pady=5)

        # Button to find directions
        find_directions_button = Button(directions_frame, text="길 찾기", command=self.find_directions)
        find_directions_button.grid(row=2, columnspan=2, padx=5, pady=5)

        # Text widget to display directions
        self.directions_text = Text(self.second_tab, wrap=WORD, width=50, height=20)
        self.directions_text.place(x=10, y=120)

    def setup_first_tab(self):
        # 검색창과 검색 버튼을 위한 프레임 생성 및 배치
        self.search_frame = Frame(self.first_tab)
        self.search_frame.configure(bg='ivory')
        self.search_frame.place(x=10, y=10, width=400, height=50)

        # 검색창과 검색 버튼 설정
        self.search_list = list()
        self.select_info = []
        self.search_var = StringVar()
        self.search_entry = Entry(self.search_frame, textvariable=self.search_var, width=30)
        self.search_entry.grid(row=0, column=0, padx=5, pady=5)

        self.search_button = Button(self.search_frame, text='검색', command=self.search)
        self.search_button.grid(row=0, column=1, padx=5, pady=5)

        # 선택된 정보를 표시할 캔버스 (검색창 오른쪽)
        self.text_widget = Text(self.first_tab, width=40, height=16, state="disabled")
        self.text_widget.place(x=400, y=50)

        # 검색 결과 및 선택 정보를 담을 컨테이너 프레임
        self.container_frame = Frame(self.first_tab)
        self.container_frame.configure(bg='ivory')
        self.container_frame.place(x=10, y=70, width=320, height=250)

        # 검색 결과 프레임과 스크롤바 설정 (컨테이너 프레임 내부)
        self.results_frame = Frame(self.container_frame)
        self.results_frame.place(x=0, y=0, width=320, height=250)

        self.canvas = Canvas(self.results_frame, bg='white', width=300, height=225, scrollregion=(0, 0, 300, 225))
        self.scrollbar = Scrollbar(self.results_frame, orient='vertical', command=self.canvas.yview)
        self.scrollable_frame = Frame(self.canvas)

        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: self.canvas.configure(
                scrollregion=self.canvas.bbox("all")
            )
        )
        self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        self.canvas.configure(yscrollcommand=self.scrollbar.set)

        self.canvas.place(x=0, y=0, width=300, height=250)
        self.scrollbar.place(x=300, y=0, width=20, height=250)

        # 즐겨찾기 추가 버튼 생성
        self.add_favorites_button_img = PhotoImage(file="image/star.png")
        self.add_favorites_button = Button(self.first_tab, image=self.add_favorites_button_img,
                                           command=self.add_to_favorites)
        self.add_favorites_button.place(x=400, y=270, width=50, height=50)

        # 네이버 맵을 표시할 라벨
        self.map_label = Label(self.first_tab)
        self.map_label.configure(bg='ivory')
        self.map_label.place(x=400, y=400, width=300, height=300)

        # 검색 결과 목록 초기화
        self.search_results = []

        self.graph_canvas = Canvas(self.first_tab, bg='white', width=300, height=200)
        self.graph_canvas.place(x=10, y=400, width=300, height=300)

        # 탭 컨트롤 생성 및 배치
        self.sub_tab_control = ttk.Notebook(self.first_tab)
        self.sub_tab_control.place(x=10, y=50, width=320, height=20)

        # 검색 결과 탭 생성
        self.results_tab = Frame(self.sub_tab_control)
        self.sub_tab_control.add(self.results_tab, text='검색 결과')

        # 선택된 정보를 표시할 탭 생성
        self.selection_tab = Frame(self.sub_tab_control)
        self.sub_tab_control.add(self.selection_tab, text='즐겨 찾기')

        # 선택된 정보를 표시할 프레임 (선택 탭 내부)
        self.selection_frame = Frame(self.selection_tab, width=250)
        self.selection_frame.grid(row=0, column=0, sticky="nsew")

        # 즐겨찾기 목록 초기화
        self.favorites = []

        # Event binding
        self.sub_tab_control.bind("<<NotebookTabChanged>>", self.on_tab_selected)

    def send_email(self):
        sender_email = "seanseol05@gmail.com"
        sender_password = "wppt owjf mggb ifdr"
        receiver_email = "seanseol05@gmail.com"
        subject = "Sport Finder 즐겨찾기"
        body = "즐겨찾기 목록:\n\n" + "\n".join(
            [f"{item[0]} - {item[1]} - {item[2]} - {item[3]} - {item[4]} - {item[5]} - {item[6]}" for item in
             self.favorites])

        msg = MIMEMultipart()

        msg['From'] = sender_email
        msg['To'] = receiver_email
        msg['Subject'] = subject

        msg.attach(MIMEText(body, 'plain'))

        try:
            server = smtplib.SMTP('smtp.gmail.com', 587)
            server.starttls()
            server.login(sender_email, sender_password)
            text = msg.as_string()
            server.sendmail(sender_email, receiver_email, text)
            server.quit()

            print("이메일이 성공적으로 발송되었습니다.")
        except Exception as e:
            print(f"이메일 발송에 실패하였습니다: {str(e)}")
    def telegram(self):
        self.bot_thread_flag.set()
        threading.Thread(target=self.run_bot).start()

    def run_bot(self):
        self.bot.run()
        self.bot_thread_flag.clear()

    def on_tab_selected(self, event):
        selected_tab = event.widget.tab(event.widget.select(), "text")
        if selected_tab == '즐겨 찾기':
            self.update_favorites()
            self.canvas.yview_moveto(0)
        if selected_tab == '검색 결과':
            self.update_results(self.search_list)
            self.canvas.yview_moveto(0)

    def add_to_favorites(self):
        # 선택된 정보를 즐겨찾기에 추가
        if self.select_info not in self.favorites:
            self.favorites.append(self.select_info)
            self.bot.add_bookmark(self.select_info)
            return
        else:
            for i, favorite in enumerate(self.favorites):
                if favorite[0] == self.select_info[0]:
                    del self.favorites[i]
                    self.bot.erase_bookmark(self.select_info)
                    self.update_favorites()
                    break

    def update_favorites(self):
        # 즐겨찾기 목록 업데이트
        for widget in self.scrollable_frame.winfo_children():
            widget.destroy()
        if not self.favorites:
            return
        for favorite in self.favorites:
            label = Label(self.scrollable_frame, text=favorite[0] + "\t\t\t\t\t")
            label.bind("<Button-1>", lambda event, result=favorite[0]: self.show_selection(result))
            label.pack(anchor='w')

    def search(self):
        query = self.search_var.get()

        results = list()
        for info in self.All_list:
            if query in info[1]:
                results.append(info[0])

        self.search_list = results
        self.sub_tab_control.select(self.results_tab)
        self.update_results(results)
        self.update_graph(results)

    def update_results(self, results):
        # 기존 검색 결과 삭제
        for widget in self.scrollable_frame.winfo_children():
            widget.destroy()

        # 새로운 검색 결과 표시, 최대 10개
        for res in results:
            label = Label(self.scrollable_frame, text=res + "\t\t\t\t\t")
            label.bind("<Button-1>", lambda event, result=res: self.show_selection(result))
            label.pack(anchor='w')

    def show_selection(self, selection):
        # 선택된 정보 표시
        for info in self.All_list:
            if selection == info[0]:
                self.select_info = info
                self.text_widget.config(state="normal")
                self.text_widget.delete("1.0", "end")
                self.text_widget.insert("1.0", "시설명: " + info[0] + "\n" +
                                        "지역: " + info[1] + "\n" +
                                        "면적: " + info[2] + "\n" +
                                        "바닥 재질: " + info[3] + "\n" +
                                        "주소: " + info[6] + "\n" +
                                        "위도: " + info[4] + "\n" +
                                        "경도: " + info[5] + "\n")
                self.text_widget.config(state="disabled")

                # 구글 맵을 표시
                latitude = info[4]
                longitude = info[5]
                map_url = f"https://maps.googleapis.com/maps/api/staticmap?center={latitude},{longitude}&zoom=15&size=400x400&key=AIzaSyCzFgc9OGnXckq1-JNhSCVGo9zIq1kSWcE"

                if info[4] and info[5]:
                    marker_url = f"&markers=color:red%7C{latitude},{longitude}"
                map_url += marker_url

                self.show_map(map_url)

        for widget in self.selection_frame.winfo_children():
            widget.destroy()

        Label(self.selection_frame, text=selection).pack()

    def show_map(self, map_url):
        response = requests.get(map_url)
        img_data = response.content
        img = Image.open(BytesIO(img_data))
        img = img.resize((400, 400), Image.Resampling.LANCZOS)
        photo = ImageTk.PhotoImage(img)
        self.map_label.config(image=photo)
        self.map_label.image = photo

    def update_graph(self, results):
        # 축구장, 야구장, 테니스장 개수 계산
        soccer_count = 0
        baseball_count = 0
        tennis_count = 0

        for result in results:
            for info in Soccer.soccer_lists:
                if result == info[0]:
                    soccer_count += 1
            for info in BaseBall.baseball_lists:
                if result == info[0]:
                    baseball_count += 1
            for info in Tennis.tennis_lists:
                if result == info[0]:
                    tennis_count += 1

        # 캔버스 초기화
        self.graph_canvas.delete("all")

        # 막대 그래프 그리기
        total = soccer_count + baseball_count + tennis_count
        if total == 0:
            return

        max_height = 250
        bar_width = 50

        soccer_height = spam.barlen(soccer_count, total)
        baseball_height = spam.barlen(baseball_count, total)
        tennis_height = spam.barlen(tennis_count, total)

        self.graph_canvas.create_rectangle(40, max_height - soccer_height, 40 + bar_width, max_height, fill='green')
        self.graph_canvas.create_rectangle(110, max_height - baseball_height, 110 + bar_width, max_height, fill='orange')
        self.graph_canvas.create_rectangle(180, max_height - tennis_height, 180 + bar_width, max_height, fill='blue')

        self.graph_canvas.create_text(40 + bar_width / 2, max_height - soccer_height - 10,
                                      text=str(soccer_count), anchor='s')
        self.graph_canvas.create_text(110 + bar_width / 2, max_height - baseball_height - 10,
                                      text=str(baseball_count), anchor='s')
        self.graph_canvas.create_text(180 + bar_width / 2, max_height - tennis_height - 10,
                                      text=str(tennis_count), anchor='s')

        self.graph_canvas.create_text(40 + bar_width / 2, max_height + 10, text='축구장', anchor='n')
        self.graph_canvas.create_text(110 + bar_width / 2, max_height + 10, text='야구장', anchor='n')
        self.graph_canvas.create_text(180 + bar_width / 2, max_height + 10, text='테니스장', anchor='n')

    def on_closing(self):
        if self.bot_thread_flag.is_set():
            self.bot_thread_flag.clear()
            self.bot.running = False
            self.window.destroy()
        else:
            self.window.destroy()

    def get_coordinates(self, address):
        client_id = 'gxp3zxbpf6'
        client_secret = 'NOYVE8v4pDKxnF2rnisXhTgrkClON8ZEfQi0GSUG'

        url = f"https://naveropenapi.apigw.ntruss.com/map-geocode/v2/geocode?query={address}"
        headers = {
            "X-NCP-APIGW-API-KEY-ID": client_id,
            "X-NCP-APIGW-API-KEY": client_secret
        }
        response = requests.get(url, headers=headers)
        result = response.json()
        if "addresses" in result and len(result["addresses"]) > 0:
            return result["addresses"][0]["x"], result["addresses"][0]["y"]
        else:
            return None, None

    def find_directions(self):
        start_location = self.start_var.get()
        end_location = self.end_var.get()

        # 출발지와 도착지의 좌표를 얻기
        start_x, start_y = self.get_coordinates(start_location)
        end_x, end_y = self.get_coordinates(end_location)

        if start_x is None or end_x is None:
            self.directions_text.config(state="normal")
            self.directions_text.delete("1.0", "end")
            self.directions_text.insert("end", "경로를 찾을 수 없습니다. 출발지 또는 도착지 주소를 확인하세요.\n")
            self.directions_text.config(state="disabled")
            return

        # 네이버 지도 API 키 설정
        client_id = 'gxp3zxbpf6'
        client_secret = 'NOYVE8v4pDKxnF2rnisXhTgrkClON8ZEfQi0GSUG'

        # 경로 검색
        url = f"https://naveropenapi.apigw.ntruss.com/map-direction-15/v1/driving?start={start_x},{start_y}&goal={end_x},{end_y}&option=trafast"
        headers = {
            "X-NCP-APIGW-API-KEY-ID": client_id,
            "X-NCP-APIGW-API-KEY": client_secret
        }

        response = requests.get(url, headers=headers)
        directions_result = response.json()

        if "route" in directions_result:
            route = directions_result['route']['trafast'][0]
            steps = route['guide']
            self.directions_text.config(state="normal")
            self.directions_text.delete("1.0", "end")
            for step in steps:
                self.directions_text.insert("end", step['instructions'] + "\n")
            self.directions_text.config(state="disabled")
        else:
            self.directions_text.config(state="normal")
            self.directions_text.delete("1.0", "end")
            self.directions_text.insert("end", "경로를 찾을 수 없습니다.\n")
            self.directions_text.insert("end", f"출발지: {start_location}\n")
            self.directions_text.insert("end", f"도착지: {end_location}\n")
            self.directions_text.insert("end", "API 응답: {}\n".format(directions_result))
            self.directions_text.config(state="disabled")

MainGUI()
