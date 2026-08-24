import threading
import tkinter.filedialog as filedialog
import customtkinter as ctk

from scanner import scan_network
from exporter import export_to_csv


class NetworkScannerApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Network Scanner v1.0- TWARDY.exe")
        self.geometry("950x620")
        self.minsize(900, 580)

        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")

        self.devices = []

        self.create_layout()

    def create_layout(self):
        self.header = ctk.CTkFrame(self, height=90, corner_radius=0)
        self.header.pack(fill="x")

        self.title_label = ctk.CTkLabel(
            self.header,
            text="Network Scanner v1.0 - TWARDY.exe",
            font=("Arial", 28, "bold")
        )
        self.title_label.pack(pady=(18, 0))

        self.subtitle_label = ctk.CTkLabel(
            self.header,
            text="Scan your local network and discover active devices",
            font=("Arial", 14)
        )
        self.subtitle_label.pack(pady=(2, 12))

        self.main_frame = ctk.CTkFrame(self, corner_radius=18)
        self.main_frame.pack(fill="both", expand=True, padx=20, pady=20)

        self.control_frame = ctk.CTkFrame(self.main_frame, corner_radius=14)
        self.control_frame.pack(fill="x", padx=18, pady=18)

        self.range_label = ctk.CTkLabel(
            self.control_frame,
            text="Network Range:",
            font=("Arial", 14, "bold")
        )
        self.range_label.grid(row=0, column=0, padx=(15, 8), pady=15)

        self.range_entry = ctk.CTkEntry(
            self.control_frame,
            width=230,
            placeholder_text="192.168.1.0/24"
        )
        self.range_entry.grid(row=0, column=1, padx=8, pady=15)
        self.range_entry.insert(0, "192.168.1.0/24")

        self.scan_button = ctk.CTkButton(
            self.control_frame,
            text="Start Scan",
            width=130,
            command=self.start_scan_thread
        )
        self.scan_button.grid(row=0, column=2, padx=8, pady=15)

        self.export_button = ctk.CTkButton(
            self.control_frame,
            text="Export CSV",
            width=130,
            command=self.export_results,
            state="disabled"
        )
        self.export_button.grid(row=0, column=3, padx=8, pady=15)

        self.clear_button = ctk.CTkButton(
            self.control_frame,
            text="Clear",
            width=100,
            command=self.clear_results
        )
        self.clear_button.grid(row=0, column=4, padx=8, pady=15)

        self.status_label = ctk.CTkLabel(
            self.control_frame,
            text="Ready",
            font=("Arial", 13)
        )
        self.status_label.grid(row=0, column=5, padx=(20, 15), pady=15, sticky="e")

        self.control_frame.grid_columnconfigure(5, weight=1)

        self.table_frame = ctk.CTkScrollableFrame(self.main_frame, corner_radius=14)
        self.table_frame.pack(fill="both", expand=True, padx=18, pady=(0, 18))

        self.create_table_header()

    def create_table_header(self):
        header_values = ["IP Address", "Status", "Hostname", "MAC Address"]

        for column, value in enumerate(header_values):
            label = ctk.CTkLabel(
                self.table_frame,
                text=value,
                font=("Arial", 14, "bold")
            )
            label.grid(row=0, column=column, padx=12, pady=10, sticky="w")

        for column in range(4):
            self.table_frame.grid_columnconfigure(column, weight=1)

    def start_scan_thread(self):
        network_range = self.range_entry.get().strip()

        if not network_range:
            self.status_label.configure(text="Enter a network range first")
            return

        self.scan_button.configure(state="disabled", text="Scanning...")
        self.export_button.configure(state="disabled")
        self.status_label.configure(text="Scanning network...")
        self.clear_table()

        scan_thread = threading.Thread(
            target=self.run_scan,
            args=(network_range,),
            daemon=True
        )
        scan_thread.start()

    def run_scan(self, network_range):
        try:
            self.devices = scan_network(network_range)

            self.after(0, self.show_results)
        except Exception as error:
            self.after(0, lambda: self.show_error(str(error)))

    def show_results(self):
        if not self.devices:
            self.status_label.configure(text="No active devices found")
        else:
            for index, device in enumerate(self.devices, start=1):
                self.add_device_row(index, device)

            self.status_label.configure(text=f"Found {len(self.devices)} device(s)")
            self.export_button.configure(state="normal")

        self.scan_button.configure(state="normal", text="Start Scan")

    def add_device_row(self, row, device):
        values = [
            device["ip"],
            device["status"],
            device["hostname"],
            device["mac"]
        ]

        for column, value in enumerate(values):
            label = ctk.CTkLabel(
                self.table_frame,
                text=value,
                font=("Arial", 13),
                anchor="w"
            )
            label.grid(row=row, column=column, padx=12, pady=8, sticky="w")

    def show_error(self, message):
        self.status_label.configure(text=message)
        self.scan_button.configure(state="normal", text="Start Scan")

    def clear_table(self):
        for widget in self.table_frame.winfo_children():
            widget.destroy()

        self.create_table_header()

    def clear_results(self):
        self.devices = []
        self.clear_table()
        self.status_label.configure(text="Ready")
        self.export_button.configure(state="disabled")

    def export_results(self):
        if not self.devices:
            self.status_label.configure(text="Nothing to export")
            return

        file_path = filedialog.asksaveasfilename(
            defaultextension=".csv",
            filetypes=[("CSV Files", "*.csv")],
            title="Save scan results"
        )

        if file_path:
            export_to_csv(file_path, self.devices)
            self.status_label.configure(text="Results exported successfully")


if __name__ == "__main__":
    app = NetworkScannerApp()
    app.mainloop()