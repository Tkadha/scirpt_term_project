from tkinter import *
from tkinter import ttk
from baseball import BaseBall
from soccer import Soccer
from tennis import Tennis
from PIL import Image, ImageTk
import requests
from io import BytesIO

class MainGUI():
    def __init__(self):
        self.All_list=BaseBall.baseball_lists+Soccer.soccer_lists+Tennis.tennis_lists
        self.All_list=sorted(self.All_list,key=lambda x:x[0])

        self.window = Tk()
        self.window.title("Sport Finder")
        self.window.geometry("800x800")  # 창 크기를 늘립니다.
        self.window.configure(bg='ivory')

        # 검색창과 검색 버튼을 위한 프레임 생성 및 배치
        self.search_frame = Frame(self.window)
        self.search_frame.configure(bg='ivory')
        self.search_frame.place(x=10, y=0, width=400, height=400)


        # 검색창과 검색 버튼 설정
        self.search_list=list()
        self.select_info=[]
        self.search_var = StringVar()
        self.search_entry = Entry(self.search_frame, textvariable=self.search_var, width=25)
        self.search_entry.place(x=0, y=0, width=300, height=25)

        self.search_button = Button(self.search_frame, text='검색', command=self.search)
        self.search_button.place(x=300, y=0, width=50, height=25)

        # 탭 컨트롤 생성 및 배치
        self.tab_control = ttk.Notebook(self.window)
        self.tab_control.place(x=10, y=28, width=320, height=150)

        # 검색 결과 탭 생성
        self.results_tab = Frame(self.tab_control)
        self.tab_control.add(self.results_tab, text='검색 결과')


        # 선택된 정보를 표시할 캔버스 (검색창 오른쪽)
        self.text_widget = Text(self.window, width=40, height=20, state="disabled")
        self.text_widget.place(x=400, y=30)

        # 검색 결과 및 선택 정보를 담을 컨테이너 프레임
        self.container_frame = Frame(self.window)
        self.container_frame.configure(bg='ivory')
        self.container_frame.place(x=10, y=50, width=320, height=250)

        # 검색 결과 프레임과 스크롤바 설정 (컨테이너 프레임 내부)
        self.results_frame = Frame(self.container_frame)
        self.results_frame.place(x=0, y=0, width=320, height=250)

        self.canvas = Canvas(self.results_frame, bg='white', width=350, height=225, scrollregion=(0, 0, 350, 225))
        self.scrollbar = Scrollbar(self.results_frame, orient='vertical', command=self.canvas.yview)
        self.scrollable_frame = Frame(self.canvas)

        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: self.canvas.configure(
                scrollregion=self.canvas.bbox("all")
            )
        )
        self.canvas.create_window((10, 0), window=self.scrollable_frame, anchor="nw")
        self.canvas.configure(yscrollcommand=self.scrollbar.set)

        self.canvas.place(x=0, y=0, width=300, height=250)
        self.scrollbar.place(x=300, y=0, width=20, height=250)

        # 선택된 정보를 표시할 탭 생성
        self.selection_tab = Frame(self.tab_control)
        self.tab_control.add(self.selection_tab, text='즐겨 찾기')

        # 선택된 정보를 표시할 프레임 (선택 탭 내부)
        self.selection_frame = Frame(self.selection_tab, width=250)
        self.selection_frame.grid(row=0, column=0, sticky="nsew")

        # 즐겨찾기 목록 초기화
        self.favorites = []

        # 즐겨찾기 추가 버튼 생성
        self.add_favorites_button_img = PhotoImage(file="image/star.png")
        self.add_favorites_button = Button(self.window, image=self.add_favorites_button_img,command=self.add_to_favorites)
        self.add_favorites_button.place(x=400, y=300, width=50, height=50)


        # 구글 맵을 표시할 라벨
        self.map_label = Label(self.window)
        self.map_label.configure(bg='ivory')
        self.map_label.place(x=400, y=400, width=300, height=300)

        # 검색 결과 목록 초기화
        self.search_results = []

        self.graph_canvas = Canvas(self.window, bg='white', width=300, height=200)
        self.graph_canvas.place(x=10, y=400, width=300, height=300)

        self.tab_control.bind("<<NotebookTabChanged>>", self.on_tab_selected)

        self.window.mainloop()

    def on_tab_selected(self, event):
        selected_tab = event.widget.tab(event.widget.select(), "text")
        if selected_tab == '즐겨 찾기':
            self.update_favorites()
        if selected_tab == '검색 결과':
            self.update_results(self.search_list)

    def add_to_favorites(self):
        # 선택된 정보를 즐겨찾기에 추가
        if self.select_info not in self.favorites:
            self.favorites.append(self.select_info)
            return
        else:
            for i, favorite in enumerate(self.favorites):
                if favorite[0] == self.select_info[0]:
                    del self.favorites[i]
                    self.update_favorites()
                    break


    def update_favorites(self):
        # 즐겨찾기 목록 업데이트
        for widget in self.scrollable_frame.winfo_children():
            widget.destroy()

        for favorite in self.favorites:
            label = Label(self.scrollable_frame, text=favorite[0]+"\t\t\t\t\t")
            label.bind("<Button-1>", lambda event, result=favorite[0]: self.show_selection(result))
            label.pack(anchor='w')

    def search(self):
        query = self.search_var.get()

        results=list()
        for info in self.All_list:
            if query in info[1]:
                results.append(info[0])

        self.search_list= results
        self.tab_control.select(self.results_tab)
        self.update_results(results)
        self.update_graph(results)
    def update_results(self, results):
        # 기존 검색 결과 삭제
        for widget in self.scrollable_frame.winfo_children():
            widget.destroy()

        # 새로운 검색 결과 표시, 최대 10개
        for res in results:
            label = Label(self.scrollable_frame, text=res+"\t\t\t\t\t")
            label.bind("<Button-1>", lambda event, result=res: self.show_selection(result))
            label.pack(anchor='w')

    def show_selection(self, selection):
        # 선택된 정보 표시
        for info in self.All_list:
            if selection == info[0]:
                self.select_info = info
                self.text_widget.config(state="normal")
                self.text_widget.delete("1.0","end")
                self.text_widget.insert("1.0","시설명: "+info[0]+"\n" +
                                        "지역: "+info[1]+"\n" +
                                        "면적: "+info[2]+"\n" +
                                        "바닥 재질: "+info[3]+"\n" +
                                        "주소: " + info[6] + "\n" +
                                        "위도: "+info[4]+"\n" +
                                        "경도: "+info[5]+"\n")
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
        max_width = 200
        bar_width = 50

        soccer_height = max_height * (soccer_count / total)
        baseball_height = max_height * (baseball_count / total)
        tennis_height = max_height * (tennis_count / total)

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


MainGUI()