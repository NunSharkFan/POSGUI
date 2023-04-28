import flet as ft

appName = "Nun Shark"

def main(page: ft.Page):
    page.title = appName

    userInfo = ft.TextField(label="Username")
    passInfo = ft.TextField(label="Password", password=True, can_reveal_password=True)
    error_prompt = ft.Text("Username or Password is Incorrect", visible=False)

    def user_auth(_):
        if userInfo.value == "ABC" and passInfo.value == "123":
            page.go("/main")
        else:
            error_prompt.visible=True
            userInfo.value = ""
            passwordInfo.value = ""
        page.update()

    def route_change(route):
        page.views.clear()
        if page.route == "/auth":
            page.title = "AUTH"
            page.views.append(
                ft.View(
                    "/auth",
                    [ft.Column(controls=[   ft.Container(content=ft.Text(appName), alignment= ft.alignment.center),
                                            userInfo,
                                            passInfo,
                                            ft.FloatingActionButton(text="LOGIN", on_click=user_auth)], expand= True),
                                            error_prompt]
                )
            )
        elif page.route == "/main":
            page.title = "MAIN"
            page.views.append(
                ft.View(
                    "/main",
                    [ft.IconButton(ft.icons.DARK_MODE_OUTLINED, on_click=lambda _: page.go("/store"))]
                )
            )
        if page.route == "/store":
            page.title = "STORE"
            page.views.append(
                ft.View(
                    "/store",
                    [ft.IconButton(ft.icons.CHECK, on_click=lambda _: page.go("/auth"))]
                )
            )


        page.update()


    page.route = "/auth"
    page.on_route_change = route_change
    page.go(page.route)

ft.app(target=main)
