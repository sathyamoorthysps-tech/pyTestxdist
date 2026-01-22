class LoginPage:
    def __init__(self, page):
        self.page = page
        self.username = "input#ap_email"
        self.password = "input#ap_password"
        self.submit = "input#signInSubmit"

    def open(self):
        self.page.goto("https://www.amazon.in/ap/signin")

    def login(self, user, pwd):
        self.page.fill(self.username, user)
        self.page.fill(self.password, pwd)
        self.page.click(self.submit)
        self.page.wait_for_load_state("networkidle")