import flet as ft
from functools import reduce
from typing import Callable
import os

appName = "Nun Shark POS System"

class Product:
    def __init__(self, id: str, name: str, price: float, stocks: int, image: str):
        self.id = id
        self.name = name
        self.price = price
        self.stocks = stocks
        self.image = image
    
class CartItem:
    def __init__(self, product:Product, quantity: int):
        self.product = product
        self.quantity = quantity

    def subtotal(self):
        return self.product.price * self.quantity

def main(page: ft.Page):
    page.title = appName
    page.theme_mode = ft.ThemeMode.LIGHT

    def theme_change(_):
        if page.theme_mode == ft.ThemeMode.LIGHT:
            page.theme_mode = ft.ThemeMode.DARK
            themeIcon.icon = ft.icons.DARK_MODE_OUTLINED
        else:
            page.theme_mode = ft.ThemeMode.LIGHT
            themeIcon.icon = ft.icons.LIGHT_MODE_OUTLINED
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

    themeIcon = ft.IconButton(icon = ft.icons.LIGHT_MODE_OUTLINED,
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
                        [ft.Column(controls = [ft.Container(content = ft.Row(alignment = ft.MainAxisAlignment.CENTER,
                                                                             controls = [ft.Text(appName,
                                                                                                 size = 50),
                                                                                         themeIcon]),
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
                        appbar = ft.AppBar(title = ft.Row(controls = [ft.Text(value = f'Welcome Back, {userInfo.value}!',
                                                                              expand = True),
                                                                      themeIcon]),
                                           bgcolor = ft.colors.BLUE_ACCENT_400),
                        controls = [ft.Column(controls = [ft.Row(controls = [storeCard,
                                                                             historyCard,
                                                                             authCard],
                                              alignment = ft.MainAxisAlignment.CENTER)],
                        alignment = ft.MainAxisAlignment.CENTER,
                        expand = True)]))
            
        elif page.route == "/store":
            cartView = ft.ListView()
            productsView = ft.ListView()
            products = []
            cart: list(CartItem) = []
            with open('products.txt') as f:
                for line in f:
                    if '*' in line:
                        continue
                    id = line[0:5]
                    name = line[5:20]
                    name = name.replace(" ", "")
                    name = name.replace("_", " ")
                    price = float(line[20:30])
                    stocks = int(line[30:40])
                    image = line[40:].replace("/n", "")
                    products.append(Product(id, name, price, stocks, image))

            def add_to_cart(product: Product):
                for item in cart:
                    if item.product.name == product.name:
                        cart[cart.index(item)].quantity += 1
                        break
                else:
                    cart.append(CartItem(product, 1))

            def remove_from_cart(product: Product):
                cart.remove(product)

            def show_products() -> ft.ListView:
                productsView.controls = list(map(lambda product: ft.Container(bgcolor = ft.colors.GREEN_ACCENT_400,
                                                                              content = ft.Row([ft.Text(product.name,
                                                                                                        expand = True),
                                                                                               ft.IconButton(icon = ft.icons.ADD_SHOPPING_CART,
                                                                                                             on_click = lambda _: add_to_cart(product))])),
                                                 products))
                return productsView
            
            def show_cart():
                cartView.controls = list(map(lambda item: ft.Container(bgcolor = ft.colors.YELLOW_ACCENT_400,
                                                                       ))) # YOU ARE HERE... THIS IS FOR SHOWING THE CART ITEMS BELOW THE TOTAL THINGY BLAH BLAH
                                                                            # WHAT YOU WANTED TO MAKE WAS A ROW WHICH HAS 2 SHIT ON IT, A TEXT WITH THE NAME AND QUANTITY IN CART AND BUTTON FOR EDITING QUANTITY
                                                                            # YOU SHOULD ALSO MAKE A FUNCTION FOR THAT BUTTON THINGY.... AND REMEMBER TO COPY THE FORMAT IN SHOW_PRODUCTS FOR THIS FUNCTION
                                                                            # OH AND REMIND YOURSELF TO RESEARCH HOW WE CAN MAKE THAT SMALL BORDER THINGY IN A DIFFERENT COLOR BECAUSE IDUNNO, THE OTHER ME SCREAMING


            dueTotal = ft.Text(f'P {0}',
                               weight = ft.FontWeight.W_700)
            total = ft.Column(controls = [ft.Text('Total'),
                                          dueTotal,
                                          ft.Text('---------------------------------------------------',
                                                  weight = ft.FontWeight.W_400)])
            page.views.append(
                ft.View(
                    "/store",
                    appbar = ft.AppBar(title = ft.Row(controls = [ft.Text('Store',
                                                                          expand = True),
                                                                  themeIcon]),
                                       leading = ft.IconButton(icon = ft.icons.ARROW_BACK,
                                                               on_click = lambda e: page.go('/main'))),
                    controls = [ft.Row(controls = [ft.Container(content = show_products(), expand = True),
                                                   ft.Column(controls = [total,],
                                                             horizontal_alignment = ft.CrossAxisAlignment.END)])]))

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
