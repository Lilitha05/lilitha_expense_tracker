"""Expense model (Unit 4) and JSON persistence (Units 4 & 7)."""
import json
import uuid
from datetime import datetime
from pathlib import Path

DATA_FILE = Path(__file__).parent / "expenses.json"


class Expense:
    """A single expense entry."""

    def __init__(self, title, amount, category, date=None, expense_id=None):
        self.id = expense_id or uuid.uuid4().hex
        self.title = title
        self.amount = float(amount)
        self.category = category
        self.date = date or datetime.now().strftime("%Y-%m-%d %H:%M")

    def to_dict(self):
        return {
            "id": self.id,
            "title": self.title,
            "amount": self.amount,
            "category": self.category,
            "date": self.date,
        }

    @classmethod
    def from_dict(cls, data):
        return cls(
            data["title"],
            data["amount"],
            data["category"],
            data.get("date"),
            data.get("id"),
        )

    def __str__(self):
        return f"{self.title} - R{self.amount:,.2f} ({self.category})"


class ExpenseStore:
    """Holds all expenses and saves them to a JSON file."""

    def __init__(self, path=DATA_FILE):
        self.path = Path(path)
        self.expenses = []
        self.load()

    def load(self):
        try:
            with open(self.path, "r", encoding="utf-8") as f:
                self.expenses = [Expense.from_dict(d) for d in json.load(f)]
        except (FileNotFoundError, json.JSONDecodeError, KeyError):
            self.expenses = []

    def save(self):
        with open(self.path, "w", encoding="utf-8") as f:
            json.dump([e.to_dict() for e in self.expenses], f, indent=2)

    def add(self, expense):
        self.expenses.append(expense)
        self.save()

    def delete(self, expense_id):
        self.expenses = [e for e in self.expenses if e.id != expense_id]
        self.save()

    def total(self):
        return sum(e.amount for e in self.expenses)

    def totals_by_category(self):
        totals = {}
        for e in self.expenses:
            totals[e.category] = totals.get(e.category, 0) + e.amount
        return totals
