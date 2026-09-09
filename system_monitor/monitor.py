import csv
import json
from datetime import datetime
from pathlib import Path
import psutil
from utils.logger import get_logger

logger = get_logger("system_monitor")

class SystemMonitor:
    def __init__(self, thresholds=None):
        self.thresholds = thresholds or {
            "cpu": 85, "memory": 85, "disk": 90
        }

    def snapshot(self):
        vm = psutil.virtual_memory()
        disk = psutil.disk_usage("/")
        net = psutil.net_io_counters()
        data = {
            "timestamp": datetime.now().isoformat(timespec="seconds"),
            "cpu_percent": psutil.cpu_percent(interval=0.5),
            "memory_percent": vm.percent,
            "memory_used_gb": round(vm.used / 1024**3, 2),
            "memory_total_gb": round(vm.total / 1024**3, 2),
            "disk_percent": disk.percent,
            "disk_used_gb": round(disk.used / 1024**3, 2),
            "disk_total_gb": round(disk.total / 1024**3, 2),
            "network_sent_mb": round(net.bytes_sent / 1024**2, 2),
            "network_received_mb": round(net.bytes_recv / 1024**2, 2)
        }
        return data

    def alerts(self, snapshot=None):
        s = snapshot or self.snapshot()
        alerts = []
        if s["cpu_percent"] >= self.thresholds["cpu"]:
            alerts.append(f"CPU usage high: {s['cpu_percent']}%")
        if s["memory_percent"] >= self.thresholds["memory"]:
            alerts.append(f"Memory usage high: {s['memory_percent']}%")
        if s["disk_percent"] >= self.thresholds["disk"]:
            alerts.append(f"Disk usage high: {s['disk_percent']}%")
        return alerts

    def save_report(self, output_path, snapshot=None):
        output = Path(output_path)
        output.parent.mkdir(parents=True, exist_ok=True)
        s = snapshot or self.snapshot()
        if output.suffix.lower() == ".json":
            output.write_text(json.dumps(s, indent=2), encoding="utf-8")
        elif output.suffix.lower() == ".csv":
            with output.open("w", newline="", encoding="utf-8") as f:
                writer = csv.DictWriter(f, fieldnames=s.keys())
                writer.writeheader()
                writer.writerow(s)
        else:
            raise ValueError("Report format must be .json or .csv")
        logger.info("Saved monitor report: %s", output)
        return output
