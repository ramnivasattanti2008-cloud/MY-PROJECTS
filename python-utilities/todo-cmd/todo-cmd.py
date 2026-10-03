#!/usr/bin/env python3
"""
Todo CMD - A powerful CLI todo list manager
Features: Priorities, due dates, categories, completion tracking
Stores tasks in a JSON file with colorama styling
"""

import argparse
import json
import os
import sys
from datetime import datetime, timedelta
from pathlib import Path
from typing import Optional

# Try to import colorama
try:
    from colorama import init, Fore, Style
    init(autoreset=True)
except ImportError:
    class Fore:
        RED = GREEN = YELLOW = CYAN = MAGENTA = WHITE = RESET = BLUE = ''
    class Style:
        BRIGHT = RESET_ALL = DIM = ''

# Configuration
TODO_FILE = Path.home() / ".todo-cmd.json"

# Priority configurations
PRIORITIES = {
    "high": {"symbol": "🔴", "color": Fore.RED, "label": "HIGH"},
    "medium": {"symbol": "🟡", "color": Fore.YELLOW, "label": "MED"},
    "low": {"symbol": "🟢", "color": Fore.GREEN, "label": "LOW"}
}

# Category colors
CATEGORY_COLORS = {
    "work": Fore.BLUE,
    "personal": Fore.MAGENTA,
    "health": Fore.GREEN,
    "learning": Fore.CYAN,
    "finance": Fore.YELLOW,
    "default": Fore.WHITE
}


def load_tasks() -> dict:
    """Load tasks from JSON file or return empty structure."""
    if TODO_FILE.exists():
        try:
            with open(TODO_FILE, 'r', encoding='utf-8') as f:
                return json.load(f)
        except json.JSONDecodeError:
            print(f"{Fore.RED}Error: Corrupted todo file. Starting fresh.{Style.RESET_ALL}")
            return {"tasks": [], "categories": []}
    return {"tasks": [], "categories": []}


def save_tasks(data: dict) -> None:
    """Save tasks to JSON file."""
    with open(TODO_FILE, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)


def generate_id() -> str:
    """Generate a unique task ID."""
    return datetime.now().strftime("%Y%m%d%H%M%S%f")


def add_task(title: str, priority: str, due_date: Optional[str],
             category: str, description: str = "") -> None:
    """Add a new task."""
    tasks_data = load_tasks()

    # Parse due date
    due_dt = None
    if due_date:
        try:
            due_dt = datetime.strptime(due_date, "%Y-%m-%d")
        except ValueError:
            try:
                # Support relative dates like +3days
                if due_date.startswith("+"):
                    days = int(due_date[1:])
                    due_dt = datetime.now() + timedelta(days=days)
                else:
                    print(f"{Fore.RED}Invalid date format. Use YYYY-MM-DD or +Ndays{Style.RESET_ALL}")
                    return
            except ValueError:
                print(f"{Fore.RED}Invalid date format: {due_date}{Style.RESET_ALL}")
                return

    task = {
        "id": generate_id(),
        "title": title,
        "description": description,
        "priority": priority.lower(),
        "category": category.lower() if category else "default",
        "due_date": due_dt.isoformat() if due_dt else None,
        "completed": False,
        "created_at": datetime.now().isoformat(),
        "completed_at": None
    }

    tasks_data["tasks"].insert(0, task)

    # Add category if new
    if category and category.lower() not in tasks_data.get("categories", []):
        tasks_data.setdefault("categories", []).append(category.lower())

    save_tasks(tasks_data)

    print(f"{Fore.GREEN}Task added successfully!{Style.RESET_ALL}")
    print(f"{Fore.CYAN}ID: {task['id']}{Style.RESET_ALL}")
    if task['due_date']:
        print(f"{Fore.YELLOW}Due: {due_dt.strftime('%Y-%m-%d')}{Style.RESET_ALL}")


def list_tasks(priority_filter: str = None, category_filter: str = None,
               show_completed: bool = False, show_pending: bool = False) -> None:
    """List all tasks with optional filters."""
    tasks_data = load_tasks()
    tasks = tasks_data.get("tasks", [])

    # Apply filters
    if priority_filter:
        tasks = [t for t in tasks if t.get("priority") == priority_filter.lower()]

    if category_filter:
        tasks = [t for t in tasks if t.get("category") == category_filter.lower()]

    if show_pending:
        tasks = [t for t in tasks if not t.get("completed")]
    elif not show_completed:
        tasks = [t for t in tasks if not t.get("completed")]

    if not tasks:
        print(f"{Fore.YELLOW}No tasks found.{Style.RESET_ALL}")
        return

    # Sort by priority then due date
    priority_order = {"high": 0, "medium": 1, "low": 2}
    tasks.sort(key=lambda t: (
        priority_order.get(t.get("priority", "medium"), 1),
        t.get("due_date") or "9999"
    ))

    print(f"\n{Fore.CYAN}{'='*70}{Style.RESET_ALL}")
    pending = sum(1 for t in tasks_data.get("tasks", []) if not t.get("completed"))
    print(f"{Fore.WHITE}{Style.BRIGHT}Tasks: {len(tasks)} shown | {pending} pending total{Style.RESET_ALL}")
    print(f"{Fore.CYAN}{'='*70}{Style.RESET_ALL}\n")

    for i, task in enumerate(tasks, 1):
        prio_config = PRIORITIES.get(task.get("priority", "medium"), PRIORITIES["medium"])
        cat_color = CATEGORY_COLORS.get(task.get("category", "default"), CATEGORY_COLORS["default"])

        status = f"{Fore.GREEN}✓{Style.RESET_ALL}" if task.get("completed") else f"{Fore.DIM}○{Style.RESET_ALL}"
        title = task['title']
        if task.get("completed"):
            title = f"{Style.DIM}{title}{Style.RESET_ALL}"

        print(f"{Fore.WHITE}{i}. {status} {prio_config['color']}{prio_config['symbol']} {title}{Style.RESET_ALL}")

        if task.get("description"):
            print(f"   {Fore.DIM}{task['description'][:60]}...{Style.RESET_ALL}")

        meta_parts = []
        meta_parts.append(f"ID: {task['id'][-6:]}")
        if task.get("category"):
            meta_parts.append(f"{cat_color}[{task['category']}]{Style.RESET_ALL}")
        meta_parts.append(f"Priority: {prio_config['color']}{prio_config['label']}{Style.RESET_ALL}")

        if task.get("due_date"):
            due_dt = datetime.fromisoformat(task['due_date'])
            days_left = (due_dt.date() - datetime.now().date()).days

            if task.get("completed"):
                due_str = f"Completed: {due_dt.strftime('%Y-%m-%d')}"
            elif days_left < 0:
                due_str = f"{Fore.RED}Overdue: {due_dt.strftime('%Y-%m-%d')} ({abs(days_left)} days){Style.RESET_ALL}"
            elif days_left == 0:
                due_str = f"{Fore.RED}Due TODAY!{Style.RESET_ALL}"
            elif days_left <= 3:
                due_str = f"{Fore.YELLOW}Due: {due_dt.strftime('%Y-%m-%d')} ({days_left} days){Style.RESET_ALL}"
            else:
                due_str = f"Due: {due_dt.strftime('%Y-%m-%d')}"

            meta_parts.append(due_str)

        print(f"   {Fore.DIM}{' | '.join(meta_parts)}{Style.RESET_ALL}")
        print()


def complete_task(task_id: str) -> None:
    """Mark a task as completed."""
    tasks_data = load_tasks()

    for task in tasks_data["tasks"]:
        if task['id'] == task_id:
            task['completed'] = True
            task['completed_at'] = datetime.now().isoformat()
            save_tasks(tasks_data)
            print(f"{Fore.GREEN}Task completed: {task['title']}{Style.RESET_ALL}")
            return

    print(f"{Fore.RED}Task not found: {task_id}{Style.RESET_ALL}")


def uncomplete_task(task_id: str) -> None:
    """Mark a task as incomplete (undo)."""
    tasks_data = load_tasks()

    for task in tasks_data["tasks"]:
        if task['id'] == task_id:
            task['completed'] = False
            task['completed_at'] = None
            save_tasks(tasks_data)
            print(f"{Fore.CYAN}Task reopened: {task['title']}{Style.RESET_ALL}")
            return

    print(f"{Fore.RED}Task not found: {task_id}{Style.RESET_ALL}")


def delete_task(task_id: str) -> None:
    """Delete a task."""
    tasks_data = load_tasks()

    original_count = len(tasks_data["tasks"])
    tasks_data["tasks"] = [t for t in tasks_data["tasks"] if t['id'] != task_id]

    if len(tasks_data["tasks"]) < original_count:
        save_tasks(tasks_data)
        print(f"{Fore.GREEN}Task deleted successfully!{Style.RESET_ALL}")
    else:
        print(f"{Fore.RED}Task not found: {task_id}{Style.RESET_ALL}")


def clear_completed() -> None:
    """Remove all completed tasks."""
    tasks_data = load_tasks()

    completed = [t for t in tasks_data["tasks"] if t.get("completed")]
    tasks_data["tasks"] = [t for t in tasks_data["tasks"] if not t.get("completed")]

    if completed:
        save_tasks(tasks_data)
        print(f"{Fore.GREEN}Cleared {len(completed)} completed task(s)!{Style.RESET_ALL}")
    else:
        print(f"{Fore.YELLOW}No completed tasks to clear.{Style.RESET_ALL}")


def show_stats() -> None:
    """Show task statistics."""
    tasks_data = load_tasks()
    tasks = tasks_data.get("tasks", [])

    total = len(tasks)
    completed = sum(1 for t in tasks if t.get("completed"))
    pending = total - completed

    by_priority = {"high": 0, "medium": 0, "low": 0}
    for t in tasks:
        if not t.get("completed"):
            by_priority[t.get("priority", "medium")] += 1

    overdue = 0
    due_soon = 0
    for t in tasks:
        if not t.get("completed") and t.get("due_date"):
            due_dt = datetime.fromisoformat(t['due_date'])
            days_left = (due_dt.date() - datetime.now().date()).days
            if days_left < 0:
                overdue += 1
            elif days_left <= 3:
                due_soon += 1

    print(f"\n{Fore.CYAN}{'='*50}{Style.RESET_ALL}")
    print(f"{Fore.WHITE}{Style.BRIGHT}Task Statistics{Style.RESET_ALL}")
    print(f"{Fore.CYAN}{'='*50}{Style.RESET_ALL}")
    print(f"  {Fore.WHITE}Total Tasks:{Style.RESET_ALL} {total}")
    print(f"  {Fore.GREEN}Completed:{Style.RESET_ALL} {completed}")
    print(f"  {Fore.YELLOW}Pending:{Style.RESET_ALL} {pending}")
    print()
    print(f"  {Fore.RED}Overdue:{Style.RESET_ALL} {overdue}")
    print(f"  {Fore.YELLOW}Due Soon (≤3 days):{Style.RESET_ALL} {due_soon}")
    print()
    print(f"  {Fore.RED}High Priority:{Style.RESET_ALL} {by_priority['high']}")
    print(f"  {Fore.YELLOW}Medium Priority:{Style.RESET_ALL} {by_priority['medium']}")
    print(f"  {Fore.GREEN}Low Priority:{Style.RESET_ALL} {by_priority['low']}")
    print()


def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description="Todo CMD - A powerful CLI todo list manager",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  todo-cmd add "Finish report" --priority high --due 2024-12-31 --category work
  todo-cmd add "Read book" --priority low --due +7days --category learning
  todo-cmd list
  todo-cmd list --priority high
  todo-cmd list --category work
  todo-cmd list --pending
  todo-cmd complete 20231015123456789012
  todo-cmd delete 20231015123456789012
  todo-cmd stats
  todo-cmd clear
        """
    )

    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    # Add command
    add_parser = subparsers.add_parser("add", help="Add a new task")
    add_parser.add_argument("title", help="Task title")
    add_parser.add_argument("--description", "-d", default="", help="Task description")
    add_parser.add_argument("--priority", "-p", choices=["high", "medium", "low"],
                           default="medium", help="Task priority")
    add_parser.add_argument("--due", help="Due date (YYYY-MM-DD or +Ndays)")
    add_parser.add_argument("--category", "-c", default="default", help="Task category")

    # List command
    list_parser = subparsers.add_parser("list", help="List tasks")
    list_parser.add_argument("--priority", help="Filter by priority")
    list_parser.add_argument("--category", help="Filter by category")
    list_parser.add_argument("--all", action="store_true", help="Show completed tasks too")
    list_parser.add_argument("--pending", action="store_true", help="Show only pending tasks")

    # Complete command
    complete_parser = subparsers.add_parser("complete", help="Mark task as completed")
    complete_parser.add_argument("id", help="Task ID")

    # Uncomplete command
    uncomplete_parser = subparsers.add_parser("uncomplete", help="Reopen a completed task")
    uncomplete_parser.add_argument("id", help="Task ID")

    # Delete command
    delete_parser = subparsers.add_parser("delete", help="Delete a task")
    delete_parser.add_argument("id", help="Task ID")

    # Clear command
    clear_parser = subparsers.add_parser("clear", help="Clear all completed tasks")

    # Stats command
    stats_parser = subparsers.add_parser("stats", help="Show task statistics")

    args = parser.parse_args()

    if args.command == "add":
        add_task(args.title, args.priority, args.due, args.category, args.description)
    elif args.command == "list":
        list_tasks(args.priority, args.category, args.all, args.pending)
    elif args.command == "complete":
        complete_task(args.id)
    elif args.command == "uncomplete":
        uncomplete_task(args.id)
    elif args.command == "delete":
        delete_task(args.id)
    elif args.command == "clear":
        clear_completed()
    elif args.command == "stats":
        show_stats()
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
