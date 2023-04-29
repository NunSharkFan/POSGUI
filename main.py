import flet as ft
from functools import reduce
from typing import Callable

appName = "Nun Shark POS System"

class Product:
    def __init__(self, id: str, name: str, price: float, stocks: int, image: str):
        self.id = id
        self.name = name
        self.price = price
        self.stocks = stocks
        self.image = image
    

def main(page: ft.Page):
    page.title = appName
    page.theme_mode = ft.ThemeMode.LIGHT

    def theme_change(_):
        if page.theme_mode == ft.ThemeMode.LIGHT:
            page.theme_mode = ft.ThemeMode.DARK
            themeIcon.icon = ft.icons.DARK_MODE
        else:
            page.theme_mode = ft.ThemeMode.LIGHT
            themeIcon.icon = ft.icons.LIGHT_MODE
        page.update()

    def user_auth(_):
        if userInfo.value == "admin" and passInfo.value == "leafa":
            page.go("/main")

        else:
            page.snack_bar = ft.SnackBar(
                ft.Text('Username or Password is Incorrect!',
                        color = "#ff0000"),
                bgcolor = "#ffcccb")
            page.snack_bar.open = True

        userInfo.focus()
        passInfo.value = ""
        page.update()

    themeIcon = ft.IconButton(icon = ft.icons.LIGHT_MODE,
                              on_click = theme_change)

    userInfo = ft.TextField(icon = ft.icons.PERSON,
                            label = "Username",
                            autofocus = True)
    
    passInfo = ft.TextField(icon = ft.icons.PASSWORD,
                            label = "Password",
                            password = True,
                            can_reveal_password = True)
    
    logInButton = ft.FloatingActionButton(text = "LOGIN",
                                          on_click = user_auth,
                                          expand = True)
    
    def MainMenuCard(name: str,
                     icon,
                     on_click,
                     color=ft.colors.GREEN_ACCENT_700) -> ft.Control:
        return ft.Container(padding=10,
                            width=200,
                            height=200,
                            bgcolor=color,
                            on_click=on_click,
                            content=ft.Column([ft.Icon(icon, size=64),
                                               ft.Text(name)],
                            alignment=ft.MainAxisAlignment.CENTER,
                            horizontal_alignment=ft.CrossAxisAlignment.CENTER))

    
    def route_change(route):
        page.views.clear()
        if page.route == "/auth":
            page.title = "AUTH"
            page.views.append(
                ft.View("/auth",
                        [ft.Column(controls = [ft.Container(content = ft.Text(appName,
                                                                              size=50),
                                                            alignment = ft.alignment.bottom_center,
                                                            height=200),
                                               userInfo,
                                               passInfo,
                                               ft.Container(content = logInButton,
                                                            alignment = ft.alignment.center)])]))

        elif page.route == "/main":
            page.title = "MAIN"
            storeCard = MainMenuCard('New Transaction',
                                     ft.icons.ADD,
                                     lambda e: page.go('/store'))
            historyCard = MainMenuCard('History',
                                       ft.icons.BOOK,
                                       lambda e: page.go('/transactions'))
            authCard = MainMenuCard('Log Out',
                                    ft.icons.LOGOUT,
                                    lambda e: page.go('/auth'))
            page.views.append(
                ft.View("/main",
                        [ft.Container(content = ft.Row(controls = [ft.Text(value = f'Welcome Back, {userInfo.value}!',
                                                                           expand = True),
                                                                   themeIcon]),
                                      bgcolor = ft.colors.BLUE_ACCENT_400),
                         ft.Column(controls = [ft.Row(controls = [storeCard,
                                                                  historyCard,
                                                                  authCard],
                                                      alignment = ft.MainAxisAlignment.CENTER)],
                                   alignment = ft.MainAxisAlignment.SPACE_AROUND,
                                   expand = True)]))
            
        elif page.route == "/store":
            cart = []
            products = []
            vw_product_list = ft.GridView(expand=1,
                                          runs_count=5,
                                          max_extent=300,
                                          spacing=5,
                                          run_spacing=5)
            
            vw_total = ft.Text(f'P {0}',
                               weight = ft.FontWeight.W_900,
                               size = 30)

            with open('products.txt') as f:
                for line in f:
                    id = line[0 : 5]
                    name = line[5 : 20]
                    name.replace(" ", "")
                    name.replace("_", " ")
                    price = float(line[20 : 30])
                    stocks = int(line[30 : 35])
                    image = line[35:]
                    image.replace("\n", "")
                    products.append(id, name, price, stocks, image)
            
            def ItemCard(product: Product, on_click: Callable) -> ft.Control:
                return ft.Container(on_click = lambda _: on_click(),
                                    bgcolor = ft.colors.GREEN_ACCENT_700,
                                    border_radius = 5,
                                    padding = 20,
                                    margin = 2,
                                    content = ft.Column(horizontal_alignment = ft.CrossAxisAlignment.CENTER,
                                                        alignment = ft.MainAxisAlignment.CENTER,
                                                        controls = [ft.Image(src = product.image,
                                                                             width = 150,
                                                                             height = 150),
                                                                    ft.Text(value = product.name,
                                                                            weight = ft.FontWeight.W_900),
                                                                    ft.Text(value = f'x {product.stocks}',
                                                                            weight = ft.FontWeight.W_300),
                                                                    ft.Text(value = f'P {product.price}',
                                                                            weight = ft.FontWeight.W_400)]))

            def on_item_click(product: Product):
                pass

            def show_products() -> ft.GridView:
                cards = map(lambda x: ItemCard(product = x,
                                                      on_click = lambda: on_item_click(product = x)),
                                   products)
                vw_product_list.controls = list(cards)
                return vw_product_list

            page.views.append(
                ft.View(
                    "/store",
                    appbar = ft.AppBar(title = ft.Text('Store'),
                                       leading = ft.IconButton(icon = ft.icons.ARROW_BACK,
                                                               on_click = lambda e: page.go('/main'))),
                    controls = [ft.ResponsiveRow(vertical_alignment = ft.CrossAxisAlignment.STRETCH,
                                                 controls = [ft.Column(col = 9,
                                                                       controls = [show_products()]),
                                                             ft.Column(col = 3,
                                                                       horizontal_alignment = ft.CrossAxisAlignment.STRETCH,
                                                                       controls = [ft.Column(controls = [ft.Text('TOTAL '),
                                                                                                        vw_total,
                                                                                                        ft.FilledButton('CHECKOUT',
                                                                                                                        width = 1000)]),
                                                                                   ft.Text('---------------------------------------------------')])])]))

        elif page.route == "/transactions":
            page.go('/auth')

        page.update()

    def YPRESSENTER(_: ft.KeyboardEvent):
        if _.key == 'Enter' and page.route == '/auth':
            user_auth(_)

    page.on_keyboard_event = YPRESSENTER
    page.route = "/auth"
    page.on_route_change = route_change
    page.go(page.route)

ft.app(target=main)
