import json
import time
from pathlib import Path
import schedule
from utils.logger import get_logger

logger = get_logger("task_scheduler")

class TaskScheduler:
    def __init__(self, tasks_file="configs/tasks.json"):
        self.tasks_file = Path(tasks_file)
        self.tasks_file.parent.mkdir(parents=True, exist_ok=True)
        self.tasks = self.load_tasks()

    def load_tasks(self):
        if not self.tasks_file.exists():
            return []
        return json.loads(self.tasks_file.read_text(encoding="utf-8"))

    def save_tasks(self):
        self.tasks_file.write_text(json.dumps(self.tasks, indent=2), encoding="utf-8")

    def add_task(self, name, frequency, job):
        task = {"name": name, "frequency": frequency, "job": job}
        self.tasks.append(task)
        self.save_tasks()
        return task

    def register_callable(self, frequency, func):
        # Supported examples: "10 seconds", "every minute", "every day at 09:00".
        if frequency.endswith("seconds"):
            seconds = int(frequency.split()[0])
            schedule.every(seconds).seconds.do(func)
        elif frequency == "every minute":
            schedule.every().minute.do(func)
        elif frequency.startswith("daily "):
            at_time = frequency.split(" ", 1)[1]
            schedule.every().day.at(at_time).do(func)
        else:
            raise ValueError("Unsupported frequency")

    def run_forever(self):
        logger.info("Scheduler started with %d configured tasks", len(self.tasks))
        while True:
            schedule.run_pending()
            time.sleep(1)
