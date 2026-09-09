import argparse
from pathlib import Path
from config import load_config
from file_organizer.organizer import FileOrganizer
from web_scraper.scraper import WebScraper
from system_monitor.monitor import SystemMonitor
from task_scheduler.scheduler import TaskScheduler

def main():
    cfg = load_config()
    parser = argparse.ArgumentParser(description="Comprehensive Automation Suite CLI")
    sub = parser.add_subparsers(dest="command", required=True)

    p = sub.add_parser("organize")
    p.add_argument("--source", required=True)
    p.add_argument("--dry-run", action="store_true")

    p = sub.add_parser("scrape")
    p.add_argument("--url", required=True)
    p.add_argument("--selector")

    sub.add_parser("monitor")
    sub.add_parser("scheduler")
    args = parser.parse_args()

    if args.command == "organize":
        org = FileOrganizer(cfg["file_organizer"]["categories"])
        results = org.organize(args.source, dry_run=args.dry_run)
        print(f"Processed {len(results)} files")
    elif args.command == "scrape":
        c = cfg["web_scraper"]
        scraper = WebScraper(c["user_agents"], c["proxies"], c["delay_seconds"],
                             c["timeout_seconds"], c["respect_robots_txt"])
        result = scraper.scrape(args.url, args.selector)
        print("TITLE:", result.title)
        print(result.text[:5000])
        print("LINKS:", len(result.links))
    elif args.command == "monitor":
        m = SystemMonitor(cfg["system_monitor"])
        s = m.snapshot()
        print(s)
        print("Alerts:", m.alerts(s) or "None")
    elif args.command == "scheduler":
        s = TaskScheduler(cfg["scheduler"]["tasks_file"])
        print(f"Configured tasks: {len(s.tasks)}")
        print(s.tasks)

if __name__ == "__main__":
    main()
