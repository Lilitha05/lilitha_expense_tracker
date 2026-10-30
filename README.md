**Expense Tracker (Flet Capstone)**

A simple personal expense tracker built with Flet. It records what you spend, groups it by category, and keeps your data between sessions.

Features
Home view: shows the total spent, a per-category breakdown, and a form to add a new expense (title, amount, category).
History view: lists every expense, newest first, with a delete button on each one.
Persistent data: expenses are saved to expenses.json and reloaded when the app starts.
Consistent theme: both views share one colour theme (teal seed colour) and a bottom navigation bar.
Input validation: an expense needs a title and an amount greater than 0.

**How to use**
On Home, type a title, enter an amount, pick a category, and click Add expense.
The total and category breakdown update straight away.
Open History to see every expense. Click the bin icon to delete one.
Close and reopen the app. Your expenses are still there.

**Requirements**
Python 3.10 or newer
Flet 1.0 or newer (ElevatedButton is handled for older Flet versions too)

**How to run**
*Open a terminal in the project folder.*
*Install the dependency:*
   pip install -r requirements.txt
*Start the app:*
   flet run main.py

If the desktop window doesn't open, run it in the browser instead:

   flet run --web main.py
   **:)**
