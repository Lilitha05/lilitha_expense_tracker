import flet as ft

from expense import Expense, ExpenseStore

CATEGORIES = ["Food", "Transport", "Bills", "Shopping", "Fun", "Other"]
SEED_COLOR = ft.Colors.TEAL  # one seed colour keeps the theme consistent

# ElevatedButton was renamed to Button in Flet 1.0; support both
AppButton = getattr(ft, "ElevatedButton", None) or ft.Button


def main(page: ft.Page):
    page.title = "Expense Tracker"
    page.theme_mode = ft.ThemeMode.LIGHT
    page.theme = ft.Theme(color_scheme_seed=SEED_COLOR)
    page.padding = 0

    store = ExpenseStore()
    body = ft.Container(expand=True, padding=20)

    def heading(text):
        return ft.Text(text, size=28, weight=ft.FontWeight.BOLD, color=ft.Colors.PRIMARY)

    # ---------------- Home view ----------------
    def home_view():
        title = ft.TextField(label="What did you spend on?")
        amount = ft.TextField(label="Amount (R)", keyboard_type=ft.KeyboardType.NUMBER)
        category = ft.Dropdown(
            label="Category",
            value=CATEGORIES[0],
            options=[ft.dropdown.Option(c) for c in CATEGORIES],
        )
        status = ft.Text("", color=ft.Colors.ERROR)

        def add_click(e):
            try:
                value = float((amount.value or "").replace(",", "."))
            except ValueError:
                value = 0
            if not (title.value or "").strip() or value <= 0:
                status.value = "Enter a title and an amount greater than 0."
                page.update()
                return
            store.add(Expense(title.value.strip(), value, category.value))
            show(0)  # rebuild Home so the totals update

        breakdown = [
            ft.Row(
                [ft.Text(cat), ft.Text(f"R{amt:,.2f}", weight=ft.FontWeight.W_500)],
                alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
            )
            for cat, amt in sorted(store.totals_by_category().items())
        ]

        summary = ft.Card(
            content=ft.Container(
                padding=20,
                content=ft.Column(
                    [
                        ft.Text("Total spent", color=ft.Colors.PRIMARY),
                        ft.Text(f"R{store.total():,.2f}", size=36, weight=ft.FontWeight.BOLD),
                        ft.Divider(),
                        *(breakdown or [ft.Text("No expenses yet.", italic=True)]),
                    ],
                    horizontal_alignment=ft.CrossAxisAlignment.STRETCH,
                ),
            )
        )

        return ft.Column(
            [
                heading("Home"),
                summary,
                ft.Text("Add an expense", size=18, weight=ft.FontWeight.W_500),
                title,
                amount,
                category,
                AppButton("Add expense", icon=ft.Icons.ADD, on_click=add_click),
                status,
            ],
            scroll=ft.ScrollMode.AUTO,
            spacing=15,
        )

    # ---------------- History view ----------------
    def history_view():
        def make_delete(expense_id):
            def delete_click(e):
                store.delete(expense_id)
                show(1)
            return delete_click

        tiles = [
            ft.ListTile(
                leading=ft.Icon(ft.Icons.RECEIPT_LONG, color=ft.Colors.PRIMARY),
                title=ft.Text(e.title),
                subtitle=ft.Text(f"{e.category} - {e.date}"),
                trailing=ft.Row(
                    [
                        ft.Text(f"R{e.amount:,.2f}", weight=ft.FontWeight.BOLD),
                        ft.IconButton(ft.Icons.DELETE_OUTLINE, on_click=make_delete(e.id)),
                    ],
                    tight=True,
                ),
            )
            for e in reversed(store.expenses)  # newest first
        ]

        return ft.Column(
            [
                heading("History"),
                ft.ListView(
                    controls=tiles or [ft.Text("Nothing here yet. Add one on Home.", italic=True)],
                    expand=True,
                ),
            ],
            expand=True,
        )

    # ---------------- Navigation ----------------
    def show(index):
        body.content = home_view() if index == 0 else history_view()
        page.navigation_bar.selected_index = index
        page.update()

    page.navigation_bar = ft.NavigationBar(
        destinations=[
            ft.NavigationBarDestination(icon=ft.Icons.HOME_OUTLINED, selected_icon=ft.Icons.HOME, label="Home"),
            ft.NavigationBarDestination(icon=ft.Icons.HISTORY, label="History"),
        ],
        on_change=lambda e: show(e.control.selected_index),
    )

    page.add(body)
    show(0)




def _run_app():
    run = getattr(ft, "run", None)
    if callable(run):
        run(main)
        return

    app = getattr(ft, "app", None)
    if callable(app):
        app(target=main)
    else:
        raise RuntimeError("Flet app runner is unavailable. Please install a supported flet version.")


if __name__ == "__main__":
    _run_app()
