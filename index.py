import tkinter as tk
from tkinter import ttk, messagebox
import ipaddress

class IPCalculatorGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("IP Calculator - Network Tools")
        self.root.geometry("500x650")
        self.root.resizable(False, False)
        
        self.results_dict = {}

        self.setup_ui()

    def setup_ui(self):
        # --- Top Header ---
        header_frame = ttk.Frame(self.root, padding=15)
        header_frame.pack(fill=tk.X)
        
        title_label = ttk.Label(header_frame, text="IPv4 Subnet Calculator Dhika", font=("Helvetica", 16, "bold"))
        title_label.pack(anchor=tk.W)
        
        subtitle_label = ttk.Label(header_frame, text="Format: 192.168.1.1/24 atau 192.168.1.1/255.255.255.0", font=("Helvetica", 9), foreground="gray")
        subtitle_label.pack(anchor=tk.W, pady=(2, 0))

        # --- Input Section ---
        input_frame = ttk.LabelFrame(self.root, text=" Input IP & Subnet ", padding=15)
        input_frame.pack(fill=tk.X, padx=15, pady=5)

        self.ip_entry = ttk.Entry(input_frame, font=("Helvetica", 11))
        self.ip_entry.pack(fill=tk.X, side=tk.LEFT, expand=True, padx=(0, 10))
        self.ip_entry.insert(0, "192.168.1.5/24") 
        self.ip_entry.bind("<Return>", lambda event: self.calculate())

        btn_calculate = ttk.Button(input_frame, text="Calculate", command=self.calculate)
        btn_calculate.pack(side=tk.RIGHT, ipadx=10)

        # --- Output Section ---
        output_frame = ttk.LabelFrame(self.root, text=" Calculation Results ", padding=15)
        output_frame.pack(fill=tk.BOTH, expand=True, padx=15, pady=10)

        self.labels_config = [
            ("IP Address", "ip"),
            ("Network Class", "class"),
            ("IP Type", "type"),
            ("Network Address", "network"),
            ("Subnet Mask", "netmask"),
            ("Wildcard Mask", "wildcard"),
            ("Broadcast Address", "broadcast"),
            ("First Usable IP", "first_ip"),
            ("Last Usable IP", "last_ip"),
            ("Total Hosts", "total_hosts"),
            ("Usable Hosts", "usable_hosts")
        ]

        self.value_labels = {}

        for i, (display_name, key) in enumerate(self.labels_config):
          
            lbl_name = ttk.Label(output_frame, text=display_name, font=("Helvetica", 10, "bold"))
            lbl_name.grid(row=i, column=0, sticky=tk.W, pady=6)
            
            lbl_colon = ttk.Label(output_frame, text=" :  ", font=("Helvetica", 10))
            lbl_colon.grid(row=i, column=1, sticky=tk.W)

            lbl_val = ttk.Label(output_frame, text="-", font=("Helvetica", 10), foreground="#0056b3")
            lbl_val.grid(row=i, column=2, sticky=tk.W)
            
            self.value_labels[key] = lbl_val

        # --- Footer / Action Button ---
        footer_frame = ttk.Frame(self.root, padding=15)
        footer_frame.pack(fill=tk.X)

        btn_copy = ttk.Button(footer_frame, text="Copy All Results", command=self.copy_to_clipboard)
        btn_copy.pack(fill=tk.X, ipady=5)

    def calculate(self):
        ip_input = self.ip_entry.get().strip()
        if not ip_input:
            messagebox.showwarning("Warning", "Input IP tidak boleh kosong!")
            return

        try:
      
            network = ipaddress.IPv4Network(ip_input, strict=False)
            ip_interface = ipaddress.IPv4Interface(ip_input)
            specific_ip = ip_interface.ip
            
            prefix_len = network.prefixlen
            total_hosts = network.num_addresses
            
           
            if prefix_len <= 30:
                usable_hosts = total_hosts - 2
                first_usable = network.network_address + 1
                last_usable = network.broadcast_address - 1
            else:
                usable_hosts = total_hosts
                first_usable = network.network_address
                last_usable = network.broadcast_address

            
            first_octet = int(specific_ip.exploded.split('.')[0])
            if 1 <= first_octet <= 126: ip_class = "A"
            elif first_octet == 127: ip_class = "A (Loopback)"
            elif 128 <= first_octet <= 191: ip_class = "B"
            elif 192 <= first_octet <= 223: ip_class = "C"
            elif 224 <= first_octet <= 239: ip_class = "D (Multicast)"
            else: ip_class = "E (Experimental)"

            
            ip_type = "Private" if specific_ip.is_private else "Public"
          
            self.results_dict = {
                "ip": str(specific_ip),
                "class": ip_class,
                "type": ip_type,
                "network": f"{network.network_address}/{prefix_len}",
                "netmask": str(network.netmask),
                "wildcard": str(network.hostmask),
                "broadcast": str(network.broadcast_address),
                "first_ip": str(first_usable),
                "last_ip": str(last_usable),
                "total_hosts": f"{total_hosts:,}",
                "usable_hosts": f"{usable_hosts:,}"
            }

            for key, label_obj in self.value_labels.items():
                label_obj.config(text=self.results_dict[key])

        except ValueError as e:
            messagebox.showerror("Invalid Input", f"Format IP atau Subnet Mask salah!\n\nDetail: {e}")
        except Exception as e:
            messagebox.showerror("Error", f"Terjadi kesalahan: {e}")

    def copy_to_clipboard(self):
        if not self.results_dict:
            messagebox.showwarning("Copy Failed", "Belum ada hasil kalkulasi yang bisa disalin.")
            return
        
        text_lines = ["=== IP CALCULATOR REPORT ==="]
        for display_name, key in self.labels_config:
            text_lines.append(f"{display_name}: {self.results_dict[key]}")
        
        full_text = "\n".join(text_lines)
      
        self.root.clipboard_clear()
        self.root.clipboard_append(full_text)
        messagebox.showinfo("Success", "Semua hasil kalkulasi berhasil disalin ke clipboard!")

if __name__ == "__main__":
    root = tk.Tk()
    app = IPCalculatorGUI(root)
    root.mainloop()
