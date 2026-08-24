# 🌐 Network Scanner v1.0

A desktop network scanner built with **Python** and **CustomTkinter** for discovering active devices on a local network.

Network Scanner GUI provides a simple and clean interface for scanning IPv4 network ranges, identifying reachable hosts, resolving hostnames and MAC addresses, and exporting discovered devices for further analysis.

---

## ✨ Features

- 🔎 Scan IPv4 network ranges using CIDR notation
- 🟢 Detect active devices on the local network
- 🌐 Display IP addresses
- 💻 Resolve device hostnames
- 🔗 Retrieve MAC addresses when available
- ⚡ Multithreaded scanning for improved performance
- 📄 Export scan results to CSV
- 🌙 Dark-mode interface
- 🖥️ Cross-platform Python application
- 🧹 Clear scan results directly from the interface

---

## 📸 Preview

> Application screenshot coming soon.

---

## 🛠️ Tech Stack

|     Technology     |            Purpose              |
|--------------------|---------------------------------|
|       Python       |     Core application logic      |
|    CustomTkinter   |       Modern desktop GUI        |
|      ipaddress     |  IPv4 network and CIDR handling |
|       socket       |       Hostname resolution       |
|     subprocess     | System ping and ARP interaction |
| ThreadPoolExecutor |    Concurrent network scanning  |
|         CSV        |      Scan result exporting      |

---

## 🚀 Installation

### 1. Clone the repository

```bash
git clone https://github.com/TW4RDYDEV/network-scanner.git
cd network-scanner
```

### 2. Create a virtual environment

**Windows**

```bash
python -m venv venv
venv\Scripts\activate
```

**Linux / macOS**

```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Run the application

```bash
python app.py
```

---

## 🔍 Usage

Enter the IPv4 network range you want to scan using CIDR notation.

Example:

```text
192.168.1.0/24
```

Click **Start Scan** and the application will check the network for reachable devices.

For each discovered host, the application attempts to display:

- IP address
- Online status
- Hostname
- MAC address

Results can be saved locally using the **Export CSV** button.

---

## 📁 Project Structure

```text
network-scanner/
│
├── app.py
├── scanner.py
├── exporter.py
├── requirements.txt
│
├── assets/
│   └── network-scanner-preview.png
│
├── LICENSE
├── .gitignore
└── README.md
```

### Core Files

**`app.py`**  
Contains the graphical user interface and application event handling.

**`scanner.py`**  
Handles network scanning, ping detection, hostname resolution, MAC address discovery, and multithreading.

**`exporter.py`**  
Handles exporting discovered devices to CSV files.

---

## 🧠 How It Works

The scanner converts the supplied CIDR range into individual host addresses using Python's `ipaddress` module.

Hosts are checked concurrently using a thread pool rather than sequentially, significantly reducing the time required to scan a typical local subnet.

When a host responds, the application attempts to resolve additional information such as its hostname and MAC address using operating-system networking utilities.

The discovered devices are then displayed inside the graphical interface and can optionally be exported to a CSV report.

---

## 🗺️ Roadmap

Future versions may include:

- [ ] Automatic local network detection
- [ ] MAC vendor identification
- [ ] Improved device classification
- [ ] Live scan progress indicator
- [ ] Search and filtering
- [ ] Scan history
- [ ] Device-specific icons
- [ ] Improved responsive UI
- [ ] Additional export formats
- [ ] Standalone Windows executable

---

## ⚠️ Responsible Use

Network Scanner GUI is intended for **educational purposes, network administration, home labs, and networks where the user has authorization to perform scanning**.

Only scan systems and networks that you own or have explicit permission to test.

---

## 🤝 Contributing

Suggestions, improvements, and bug reports are welcome.

If you would like to contribute:

1. Fork the repository
2. Create a new branch
3. Make your changes
4. Commit your changes
5. Open a pull request

---

## 📜 License

This project is released under the **MIT License**.

---

## 👨‍💻 Author

**TW4RDYDEV**

Cybersecurity • Networking • Software Development

---

⭐ If you find this project useful, consider giving the repository a star.
