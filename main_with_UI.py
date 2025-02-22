import tkinter as tk
from tkinter import messagebox, scrolledtext
import sys
import threading
import crawler
import network_security_HTTPS
import network_security_Encryption_Protocol
import network_security_SSL
import network_security_HSTS
import network_security_X_FRAME

class TextRedirector:
    def __init__(self, widget):
        self.widget = widget

    def write(self, string):
        # Schedule the widget update on the main thread
        self.widget.after(0, self._write, string)

    def _write(self, string):
        self.widget.insert(tk.END, string)
        self.widget.see(tk.END)

    def flush(self):
        pass

def run_checks():
    url = url_entry.get().strip()
    if not url:
        # Use the main thread for UI alerts
        root.after(0, lambda: messagebox.showerror("Input Error", "Please enter a valid URL."))
        return

    # Clear previous results on the main thread
    text_area.after(0, text_area.delete, "1.0", tk.END)
    text_area.after(0, text_area.insert, tk.END, f"Processing URL: {url}\n\n")
    
    # Redirect stdout so that print() outputs appear in the text widget
    old_stdout = sys.stdout
    sys.stdout = TextRedirector(text_area)

    try:
        # The total number of potential weaknesses
        total_po_weaknesses = 0

        # Crawl for HTTPS links
        https_links, total_po_weaknesses = crawler.extract_external_links(url)
        if https_links:
            print("🔗 External HTTPS Links Found:")
            for link in https_links:
                print(link)
        else:
            print("No external HTTPS links found.")
        
        print("\n-- Checking TLS Certificates --")
        total_po_weaknesses += network_security_Encryption_Protocol.check_encryption_protocol(https_links)
        print("TLS Certificates check complete.")
        
        print("\n-- Checking SSL Certificates --")
        network_security_SSL.check_encryption_protocol_for_hosts(https_links)
        total_po_weaknesses += network_security_SSL.potential_weaknesses
        print("SSL Certificates check complete.")
        
        print("\n-- Checking HSTS --")
        network_security_HSTS.checking_hsts(https_links)
        total_po_weaknesses += network_security_HSTS.potential_weakness
        print("HSTS check complete.")
        
        print("\n-- Checking X-Frame Options --")
        total_po_weaknesses += network_security_X_FRAME.checking_x_frame(https_links)
        print("X-Frame Options check complete.")

        print("\nTEST OVER")
        print(f"⚠️ Number of Potential Weaknesses: {total_po_weaknesses}")
        
    except Exception as e:
        print(f"\nError occurred: {e}")
    finally:
        # Restore the original stdout
        sys.stdout = old_stdout

def run_checks_thread():
    # Run run_checks in a background thread so the UI remains responsive.
    thread = threading.Thread(target=run_checks)
    thread.start()

def create_gui():
    global root, url_entry, text_area
    
    root = tk.Tk()
    root.title("Network Security Checker")
    root.geometry("700x500")
    
    # Configure the grid so that the widgets can expand.
    root.columnconfigure(0, weight=1)
    root.rowconfigure(3, weight=1)  # This is the row for the scrolled text area

    # URL input label
    label = tk.Label(root, text="Enter Website URL (e.g., http://example.com):")
    label.grid(row=0, column=0, padx=10, pady=(10, 5), sticky="w")
    
    # URL entry field (fills horizontally)
    url_entry = tk.Entry(root)
    url_entry.grid(row=1, column=0, padx=10, pady=5, sticky="ew")
    # Bind the Return key to trigger the run_checks_thread function
    url_entry.bind("<Return>", lambda event: run_checks_thread())
    
    # Run button (fills horizontally)
    run_button = tk.Button(root, text="Run Checks", command=run_checks_thread)
    run_button.grid(row=2, column=0, padx=10, pady=5, sticky="ew")
    
    # Scrolled text area for output (expands in both directions)
    text_area = scrolledtext.ScrolledText(root)
    text_area.grid(row=3, column=0, padx=10, pady=(5, 10), sticky="nsew")
    
    root.mainloop()

if __name__ == '__main__':
    create_gui()
