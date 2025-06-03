
# AEGIS - Siemens PLC Interaction Toolkit
<p align="center">
  <img src="AEGIS_logo.png" alt="AEGIS Logo" width="150">
</p>

**AEGIS** is a Python-based toolset designed for interacting with Siemens S7 PLCs using the Snap7 library.  
It offers capabilities such as memory manipulation, OB management, and PLC state control, intended for **Red Teaming**, **industrial network testing**, or **cybersecurity research**.

> ⚠️ **Warning**: This tool is for educational and authorized security testing purposes only. Unauthorized access or use on production systems may be illegal.

---

## 📦 Requirements

- Python 3.7+
- [snap7](https://pypi.org/project/python-snap7/)

```bash
pip install python-snap7
```

---

## 🚀 Usage

```bash
python3 aegis.py -i <PLC_IP> [options]
```

### 🔧 Options

| Option             | Description                                                  |
|--------------------|--------------------------------------------------------------|
| `-i, --interface`  | IP address of the target PLC (mandatory)                     |
| `-c, --connection` | Maintain multiple simultaneous connections                   |
| `-s, --saturation` | Launch a connection saturation attack                        |
| `--stop-start N`   | Stop the PLC, wait `N` seconds, then restart it              |
| `--copy OB_NUM`    | Download and print contents of a specific OB                 |
| `--paste IP OB`    | Upload previously copied OB to a new PLC or location         |
| `-d, --delete OB`  | Simulate deletion of an OB (overwrite with blank data)       |
| `--read ARGS`      | Read memory: `AREA,BYTE,BIT,DATATYPE,[DB_NUMBER]`            |
| `--write ARGS`     | Write memory: `AREA,BYTE,BIT,DATATYPE,VALUE,[DB_NUMBER]`     |
| `--stop`           | Stop the PLC                                                 |
| `--start`          | Start the PLC                                                |
| `-t, --time N`     | Sleep `N` seconds between actions                            |

---

### 🧪 Examples

- Open 10 connections:
  ```bash
  python3 aegis.py -i 192.168.0.10 -c 10
  ```

- Saturate interface:
  ```bash
  python3 aegis.py -i 192.168.0.10 -s
  ```

- Stop then restart PLC after 5 seconds:
  ```bash
  python3 aegis.py -i 192.168.0.10 --stop-start 5
  ```

- Read a bit from peripheral input area:
  ```bash
  python3 aegis.py -i 192.168.0.10 --read Areas.PE,0,0,Bit
  ```

- Write a byte to DB1 at offset 10:
  ```bash
  python3 aegis.py -i 192.168.0.10 --write Areas.DB,10,0,Byte,42,1
  ```

---

## 🛡️ Supported Memory Areas

| Name        | Constant     |
|-------------|--------------|
| DB          | `Areas.DB`   |
| Markers     | `Areas.MK`   |
| Inputs      | `Areas.PE`   |
| Outputs     | `Areas.PA`   |
| Counters    | `Areas.CT`   |
| Timers      | `Areas.TM`   |

---

## ✍️ Notes

- OB deletion is simulated by uploading an empty OB (real deletion is not available in Snap7).
- The script uses direct Snap7 calls and low-level memory access; improper usage **may crash your PLC**.

---

## 👨‍💻 Author

Maxence Lannuzel – for research and red team operations on industrial networks.

---

## 📝 License

MIT License – use with responsibility.