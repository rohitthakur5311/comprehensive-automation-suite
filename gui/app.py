import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from pathlib import Path
import threading

from config import load_config
from file_organizer.organizer import FileOrganizer
from web_scraper.scraper import WebScraper
from system_monitor.monitor import SystemMonitor
from email_automation.mailer import EmailAutomation
from task_scheduler.scheduler import TaskScheduler
from utils.logger import get_logger

logger = get_logger("gui")

class AutomationApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Comprehensive Automation Suite")
        self.geometry("1100x720")
        self.minsize(900, 600)
        self.config_data = load_config()
        self._build()

    def _build(self):
        header = ttk.Frame(self, padding=12)
        header.pack(fill="x")
        ttk.Label(header, text="🤖 Comprehensive Automation Suite",
                  font=("Segoe UI", 18, "bold")).pack(side="left")
        ttk.Button(header, text="System Status", command=self.show_status).pack(side="right")

        notebook = ttk.Notebook(self)
        notebook.pack(fill="both", expand=True, padx=10, pady=8)

        self.dashboard_tab = ttk.Frame(notebook, padding=12)
        self.file_tab = ttk.Frame(notebook, padding=12)
        self.scrape_tab = ttk.Frame(notebook, padding=12)
        self.email_tab = ttk.Frame(notebook, padding=12)
        self.monitor_tab = ttk.Frame(notebook, padding=12)
        self.scheduler_tab = ttk.Frame(notebook, padding=12)
        self.workflow_tab = ttk.Frame(notebook, padding=12)

        for tab, name in [
            (self.dashboard_tab, "Dashboard"), (self.file_tab, "File Organizer"),
            (self.scrape_tab, "Web Scraper"), (self.email_tab, "Email"),
            (self.monitor_tab, "System Monitor"), (self.scheduler_tab, "Scheduler"),
            (self.workflow_tab, "Workflow Designer")
        ]:
            notebook.add(tab, text=name)

        self._dashboard()
        self._file_organizer()
        self._scraper()
        self._email()
        self._monitor()
        self._scheduler()
        self._workflow()

    def _dashboard(self):
        ttk.Label(self.dashboard_tab, text="Integrated automation dashboard",
                  font=("Segoe UI", 16, "bold")).pack(anchor="w")
        self.dashboard_text = tk.Text(self.dashboard_tab, height=24, wrap="word")
        self.dashboard_text.pack(fill="both", expand=True, pady=10)
        self.show_status()

    def show_status(self):
        try:
            monitor = SystemMonitor(self.config_data["system_monitor"])
            s = monitor.snapshot()
            text = (
                "SYSTEM STATUS: ACTIVE\n\n"
                f"CPU Usage: {s['cpu_percent']}%\n"
                f"Memory Usage: {s['memory_percent']}% "
                f"({s['memory_used_gb']}/{s['memory_total_gb']} GB)\n"
                f"Disk Usage: {s['disk_percent']}% "
                f"({s['disk_used_gb']}/{s['disk_total_gb']} GB)\n"
                f"Network Sent: {s['network_sent_mb']} MB\n"
                f"Network Received: {s['network_received_mb']} MB\n"
                f"Alerts: {', '.join(monitor.alerts(s)) or 'None active'}\n"
            )
        except Exception as exc:
            text = f"Status error: {exc}"
        self.dashboard_text.delete("1.0", "end")
        self.dashboard_text.insert("1.0", text)

    def _file_organizer(self):
        ttk.Label(self.file_tab, text="Source folder").grid(row=0, column=0, sticky="w")
        self.file_source = tk.StringVar(value=str(Path.cwd() / "data"))
        ttk.Entry(self.file_tab, textvariable=self.file_source, width=75).grid(row=1, column=0, padx=(0,8), sticky="ew")
        ttk.Button(self.file_tab, text="Browse", command=self._browse_folder).grid(row=1, column=1)
        self.file_dry = tk.BooleanVar(value=True)
        ttk.Checkbutton(self.file_tab, text="Dry run (recommended)", variable=self.file_dry).grid(row=2, column=0, sticky="w", pady=8)
        ttk.Button(self.file_tab, text="Organize", command=self._organize).grid(row=2, column=1)
        self.file_output = tk.Text(self.file_tab, height=24)
        self.file_output.grid(row=3, column=0, columnspan=2, sticky="nsew", pady=8)
        self.file_tab.columnconfigure(0, weight=1)
        self.file_tab.rowconfigure(3, weight=1)

    def _browse_folder(self):
        value = filedialog.askdirectory()
        if value:
            self.file_source.set(value)

    def _organize(self):
        try:
            org = FileOrganizer(self.config_data["file_organizer"]["categories"])
            results = org.organize(self.file_source.get(), dry_run=self.file_dry.get())
            self.file_output.delete("1.0", "end")
            for r in results:
                self.file_output.insert("end", f"{r['file']} -> {r['category']} | duplicate={r['duplicate']}\n")
            self.file_output.insert("end", f"\nProcessed: {len(results)} files")
        except Exception as exc:
            messagebox.showerror("File Organizer", str(exc))

    def _scraper(self):
        ttk.Label(self.scrape_tab, text="Public URL").pack(anchor="w")
        self.url_var = tk.StringVar(value="https://example.com")
        ttk.Entry(self.scrape_tab, textvariable=self.url_var).pack(fill="x", pady=5)
        ttk.Label(self.scrape_tab, text="Optional CSS selector").pack(anchor="w")
        self.selector_var = tk.StringVar(value="h1")
        ttk.Entry(self.scrape_tab, textvariable=self.selector_var).pack(fill="x", pady=5)
        ttk.Button(self.scrape_tab, text="Scrape", command=self._scrape).pack(anchor="w", pady=5)
        self.scrape_output = tk.Text(self.scrape_tab, height=25)
        self.scrape_output.pack(fill="both", expand=True)

    def _scrape(self):
        try:
            cfg = self.config_data["web_scraper"]
            scraper = WebScraper(
                cfg["user_agents"], cfg["proxies"], cfg["delay_seconds"],
                cfg["timeout_seconds"], cfg["respect_robots_txt"]
            )
            result = scraper.scrape(self.url_var.get(), self.selector_var.get() or None)
            self.scrape_output.delete("1.0", "end")
            self.scrape_output.insert("1.0", f"TITLE: {result.title}\n\nTEXT:\n{result.text[:10000]}\n\nLINKS: {len(result.links)}")
        except Exception as exc:
            messagebox.showerror("Web Scraper", str(exc))

    def _email(self):
        ttk.Label(self.email_tab, text="Email Automation (Dry Run by default)",
                  font=("Segoe UI", 14, "bold")).pack(anchor="w")
        self.email_info = tk.Text(self.email_tab, height=15)
        self.email_info.pack(fill="both", expand=True, pady=10)
        self.email_info.insert("1.0",
            "Configure SMTP in .env before sending real mail.\n"
            "Use the CLI for campaigns; the GUI demonstrates configuration and template integration.\n"
            "Never place passwords directly in source code."
        )

    def _monitor(self):
        ttk.Button(self.monitor_tab, text="Refresh Metrics", command=self._refresh_monitor).pack(anchor="w")
        self.monitor_output = tk.Text(self.monitor_tab, height=25)
        self.monitor_output.pack(fill="both", expand=True, pady=8)
        self._refresh_monitor()

    def _refresh_monitor(self):
        try:
            monitor = SystemMonitor(self.config_data["system_monitor"])
            s = monitor.snapshot()
            alerts = monitor.alerts(s)
            self.monitor_output.delete("1.0", "end")
            self.monitor_output.insert("1.0", str(s) + "\n\nAlerts: " + str(alerts or "None"))
        except Exception as exc:
            self.monitor_output.insert("end", str(exc))

    def _scheduler(self):
        ttk.Label(self.scheduler_tab, text="Task Scheduler",
                  font=("Segoe UI", 14, "bold")).pack(anchor="w")
        ttk.Label(self.scheduler_tab, text="Persistent task definitions: configs/tasks.json").pack(anchor="w", pady=5)
        ttk.Button(self.scheduler_tab, text="Open tasks file", command=self._open_tasks).pack(anchor="w")
        self.scheduler_output = tk.Text(self.scheduler_tab, height=20)
        self.scheduler_output.pack(fill="both", expand=True, pady=8)
        self.scheduler_output.insert("1.0", "Examples:\n- every minute\n- 10 seconds\n- daily 09:00\n")

    def _open_tasks(self):
        path = Path(self.config_data["scheduler"]["tasks_file"])
        path.parent.mkdir(exist_ok=True)
        if not path.exists():
            TaskScheduler(str(path)).save_tasks()
        messagebox.showinfo("Tasks", str(path.resolve()))

    def _workflow(self):
        ttk.Label(self.workflow_tab, text="Workflow Designer",
                  font=("Segoe UI", 14, "bold")).pack(anchor="w")
        self.workflow_steps = tk.Listbox(self.workflow_tab, height=12)
        self.workflow_steps.pack(fill="both", expand=True, pady=8)
        row = ttk.Frame(self.workflow_tab)
        row.pack(fill="x")
        ttk.Button(row, text="Add File Organize", command=lambda: self.workflow_steps.insert("end", "file_organize")).pack(side="left", padx=4)
        ttk.Button(row, text="Add Monitor", command=lambda: self.workflow_steps.insert("end", "system_monitor")).pack(side="left", padx=4)
        ttk.Button(row, text="Run Workflow", command=self._run_workflow).pack(side="right", padx=4)

    def _run_workflow(self):
        steps = list(self.workflow_steps.get(0, "end"))
        self.workflow_steps.insert("end", "Workflow complete" if steps else "Add at least one step")
        if "system_monitor" in steps:
            self.show_status()

def run():
    AutomationApp().mainloop()
