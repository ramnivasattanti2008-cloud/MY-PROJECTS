# Todo CMD

A powerful command-line todo list manager with priorities, due dates, and categories.

## Features

- **Task priorities**: High, Medium, Low with visual indicators
- **Due dates**: Set specific dates or relative days (+Ndays)
- **Categories**: Organize tasks by type (work, personal, health, etc.)
- **Completion tracking**: Mark tasks complete/incomplete
- **Filtering**: View by priority, category, or status
- **Statistics**: Overview of your task status
- **Clear completed**: Batch remove finished tasks

## Installation

```bash
pip install -r requirements.txt
```

## Usage

### Add a Task
```bash
# Basic task
python todo-cmd.py add "Finish report"

# Full task with all options
python todo-cmd.py add "Finish report" \
  --priority high \
  --due 2024-12-31 \
  --category work \
  --description "Q4 financial report for board"

# Relative due date (7 days from now)
python todo-cmd.py add "Read chapter" --due +7 --category learning
```

### List Tasks
```bash
# Show all pending tasks
python todo-cmd.py list

# Show all tasks including completed
python todo-cmd.py list --all

# Filter by priority
python todo-cmd.py list --priority high

# Filter by category
python todo-cmd.py list --category work

# Show only pending
python todo-cmd.py list --pending
```

### Manage Tasks
```bash
# Mark task complete
python todo-cmd.py complete 20231015123456789012

# Reopen a completed task
python todo-cmd.py uncomplete 20231015123456789012

# Delete a task
python todo-cmd.py delete 20231015123456789012

# Clear all completed tasks
python todo-cmd.py clear
```

### Statistics
```bash
python todo-cmd.py stats
```

## Data Storage

Tasks are stored in `~/.todo-cmd.json` (your home directory).

## Priority Levels

| Priority | Symbol | Color |
|----------|--------|-------|
| High | 🔴 | Red |
| Medium | 🟡 | Yellow |
| Low | 🟢 | Green |

## Due Date Indicators

- **Overdue**: Red with negative days count
- **Due Today**: Flashing red alert
- **Due Soon (≤3 days)**: Yellow
- **Normal**: Default color

## Categories

Default categories (with colors):
- work (Blue)
- personal (Magenta)
- health (Green)
- learning (Cyan)
- finance (Yellow)
- default (White)
