import csv


def export_to_csv(file_path, devices):
    with open(file_path, "w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)

        writer.writerow(["IP Address", "Status", "Hostname", "MAC Address"])

        for device in devices:
            writer.writerow([
                device["ip"],
                device["status"],
                device["hostname"],
                device["mac"]
            ])