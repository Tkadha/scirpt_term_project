from tkinter import *
from tkinter import ttk
from baseball import BaseBall
from soccer import Soccer
from tennis import Tennis

class MainGUI():
    def __init__(self):
        self.All_list=BaseBall.baseball_lists+Soccer.soccer_lists+Tennis.tennis_lists
        self.All_list=sorted(self.All_list,key=lambda x:x[0])

        self.window = Tk()
        self.window.title("Sport Finder")
        self.window.geometry("800x800")

        # 검색창과 검색 버튼을 위한 프레임 생성 및 배치
        self.search_frame = Frame(self.window)
        self.search_frame.place(x=0, y=0, width=400, height=400)

        # 검색창과 검색 버튼 설정
        self.search_var = StringVar()
        self.search_entry = Entry(self.search_frame, textvariable=self.search_var, width=25)
        self.search_entry.place(x=0, y=0, width=300, height=25)

        self.search_button = Button(self.search_frame, text='검색', command=self.search)
        self.search_button.place(x=300, y=0, width=50, height=25)

        ##
        # 탭 컨트롤 생성 및 배치
        self.tab_control = ttk.Notebook(self.window)
        self.tab_control.place(x=0, y=28, width=320, height=150)

        ##
        # 검색 결과 탭 생성
        self.results_tab = Frame(self.tab_control)
        self.tab_control.add(self.results_tab, text='검색 결과')

        # 선택된 정보를 표시할 캔버스 (검색창 오른쪽)
        self.info_canvas = Canvas(self.search_frame, width=300, height=250, bg='white')
        self.info_canvas.place(x=400, y=50, width=300, height=250)

        # 검색 결과 및 선택 정보를 담을 컨테이너 프레임
        self.container_frame = Frame(self.window)
        self.container_frame.place(x=0, y=56, width=320, height=250)

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
        self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        self.canvas.configure(yscrollcommand=self.scrollbar.set)

        self.canvas.place(x=0, y=0, width=300, height=250)
        self.scrollbar.place(x=300, y=0, width=20, height=250)

        # 선택된 정보를 표시할 프레임 (컨테이너 프레임 내부)
        # self.selection_frame = Frame(self.container_frame, width=250)
        # self.selection_frame.grid(row=0, column=2, sticky="nsew")

        ##
        # 선택된 정보를 표시할 탭 생성
        self.selection_tab = Frame(self.tab_control)
        self.tab_control.add(self.selection_tab, text='즐겨 찾기')

        ##
        # 선택된 정보를 표시할 프레임 (선택 탭 내부)
        self.selection_frame = Frame(self.selection_tab, width=250)
        self.selection_frame.grid(row=0, column=0, sticky="nsew")

        # 검색 결과 목록 초기화
        self.search_results = []
        self.window.mainloop()

    def search(self):
        query = self.search_var.get()

        results=list()
        for info in self.All_list:
            if query in info[1]:
                results.append(info[0])

        self.update_results(results)

    def update_results(self, results):
        # 기존 검색 결과 삭제
        for widget in self.scrollable_frame.winfo_children():
            widget.destroy()

        # 새로운 검색 결과 표시, 최대 10개
        for result in results:
            label = Label(self.scrollable_frame, text=result)
            label.pack(anchor='w')

    def show_selection(self, selection):
        # 선택된 정보 표시
        for widget in self.selection_frame.winfo_children():
            widget.destroy()

        Label(self.selection_frame, text=selection).pack()


MainGUI()