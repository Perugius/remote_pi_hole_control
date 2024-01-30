# control and show current status of the pi hole from a web app on your computer

import requests
import json
import flet as ft

# 0 = status | 1 = enable | 2 = disable
lookup_action = ["status", "enable", "disable"]

# either control the pihole when action = 1 or 2, or just check current state if action = 0
def pi_hole_control(action):
    url = "http://192.168.1.106/admin/api.php?" + lookup_action[action] + "=300&auth=7d672902bb13cd1f10cae707022df2d90ba4a8c0771686ac73a02b30a0581966"

    try:
        response = requests.get(url)

        if response.status_code == 200:
            data = json.loads(response.text)
            status_value = data["status"]
            return status_value

        else:
            return ("Unable to fetch")
    except:
        return "error"

def main(page: ft.Page):
    page.title = 'pi hole control'

    def button_clicked(e):
        # check current status then swap to other state if button pressed
        b.data = pi_hole_control(0)
        if b.data == "enabled":
            pi_hole_control(2)
        if b.data == "disabled":
            pi_hole_control(1)

    # define text showing current state and button to change state and set alignments
    t = ft.Text(color="white", size=150)
    b = ft.ElevatedButton(text="          SWAP            ", bgcolor="blue", color="black", on_click=button_clicked, data="")
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.add(b, t)

    # loop to keep updating and displaying current pi hole state
    while True:
        current_status = pi_hole_control(0)
        t.value = current_status
        if current_status == "enabled":
            t.color="green"
        elif current_status == "disabled":
            t.color="red"
        page.update()

ft.app(target=main, view=ft.WEB_BROWSER)
