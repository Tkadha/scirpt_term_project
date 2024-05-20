from tkinter import *


class MainGUI():
    def __init__(self):
        self.window = Tk()
        self.window.title("Sport Finder")
        self.window.geometry("800x800")

        # 검색창과 검색 버튼을 위한 프레임 생성 및 배치
        self.search_frame = Frame(self.window)
        self.search_frame.grid(row=0,column=0,sticky="ew")

        # 검색창과 검색 버튼 설정
        self.search_var = StringVar()
        self.search_entry = Entry(self.search_frame, textvariable=self.search_var, width=50)
        self.search_entry.grid(row=0, column=0, padx=(10, 0), pady=(10, 0))

        self.search_button = Button(self.search_frame, text='검색', command=self.search)
        self.search_button.grid(row=0, column=1, padx=(10, 0), pady=(10, 0))

        # 검색 결과 및 선택 정보를 담을 컨테이너 프레임
        self.container_frame = Frame(self.window)
        self.container_frame.grid(row=1, column=0, sticky="nsew")

        # 검색 결과 프레임과 스크롤바 설정 (컨테이너 프레임 내부)
        self.results_frame = Frame(self.container_frame, width=350, height=300)
        self.container_frame.columnconfigure(0, minsize=10)
        self.results_frame.grid(row=0, column=1, sticky="nw")

        self.canvas = Canvas(self.results_frame, bg='white', width=350, height=300, scrollregion=(0, 0, 350, 300))
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

        self.canvas.grid(row=0, column=0, sticky="nsew")
        self.scrollbar.grid(row=0, column=1, sticky="ns")

        # 선택된 정보를 표시할 프레임 (컨테이너 프레임 내부)
        self.selection_frame = Frame(self.container_frame, width=250)
        self.selection_frame.grid(row=0, column=2, sticky="nsew")

        # 검색 결과 목록 초기화
        self.search_results = []
        self.window.mainloop()

    def search(self):
        query = self.search_var.get()
        print(f"검색: {query}")
        # 검색 로직 구현 필요
        # 예시 결과
        example_results = [f"결과 {i}" for i in range(1, 21)]  # 20개의 가짜 결과

        self.update_results(example_results)

    def update_results(self, results):
        # 기존 검색 결과 삭제
        for widget in self.scrollable_frame.winfo_children():
            widget.destroy()

        # 새로운 검색 결과 표시, 최대 10개
        for result in results[:10]:
            label = Label(self.scrollable_frame, text=result)
            label.pack(anchor='w')

    def show_selection(self, selection):
        # 선택된 정보 표시
        for widget in self.selection_frame.winfo_children():
            widget.destroy()

        Label(self.selection_frame, text=selection).pack()


MainGUI()