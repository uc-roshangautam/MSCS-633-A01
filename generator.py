#!/usr/bin/env python3


import qrcode
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from PIL import Image, ImageTk
import os
from datetime import datetime


class QRCodeGenerator:
    """
    A class to create QR codes from URL inputs with a GUI interface.
    
    This application allows users to:
    - Input a URL or text
    - Generate a QR code
    - Preview the QR code
    - Save the QR code as an image file
    """
    
    def __init__(self, root):
        """
        Initialize the QR Code Generator GUI.
        
        Args:
            root: The main tkinter window
        """
        self.root = root
        self.root.title("Biox Systems - AI QR Code Generator")
        self.root.geometry("600x700")
        self.root.configure(bg='#f0f0f0')
        
        # Variables to store QR code data
        self.qr_image = None
        self.current_data = ""
        
        self.setup_ui()
        
    def setup_ui(self):
        """Set up the user interface components."""
        
        # Title Frame
        title_frame = tk.Frame(self.root, bg='#2c3e50', height=80)
        title_frame.pack(fill='x', padx=0, pady=0)
        title_frame.pack_propagate(False)
        
        title_label = tk.Label(
            title_frame, 
            text="Biox Systems QR Code Generator", 
            font=('Arial', 18, 'bold'),
            fg='white',
            bg='#2c3e50'
        )
        title_label.pack(expand=True)
        
        # Main container
        main_frame = tk.Frame(self.root, bg='#f0f0f0')
        main_frame.pack(fill='both', expand=True, padx=20, pady=20)
        
        # Input Section
        input_frame = tk.LabelFrame(
            main_frame, 
            text="Input Data", 
            font=('Arial', 12, 'bold'),
            bg='#f0f0f0',
            fg='#2c3e50'
        )
        input_frame.pack(fill='x', pady=(0, 20))
        
        # URL input
        tk.Label(
            input_frame, 
            text="Enter URL or Text:",
            font=('Arial', 10),
            bg='#f0f0f0'
        ).pack(anchor='w', padx=10, pady=(10, 5))
        
        self.url_entry = tk.Entry(
            input_frame,
            font=('Arial', 11),
            width=50,
            relief='solid',
            borderwidth=1
        )
        self.url_entry.pack(padx=10, pady=(0, 10), fill='x')
        self.url_entry.insert(0, "https://example.com")
        
        # QR Code Options
        options_frame = tk.LabelFrame(
            main_frame,
            text="QR Code Options",
            font=('Arial', 12, 'bold'),
            bg='#f0f0f0',
            fg='#2c3e50'
        )
        options_frame.pack(fill='x', pady=(0, 20))
        
        # Size selection
        size_frame = tk.Frame(options_frame, bg='#f0f0f0')
        size_frame.pack(fill='x', padx=10, pady=10)
        
        tk.Label(
            size_frame,
            text="Size:",
            font=('Arial', 10),
            bg='#f0f0f0'
        ).pack(side='left')
        
        self.size_var = tk.StringVar(value="Medium")
        size_combo = ttk.Combobox(
            size_frame,
            textvariable=self.size_var,
            values=["Small", "Medium", "Large"],
            state="readonly",
            width=15
        )
        size_combo.pack(side='left', padx=(10, 0))
        
        # Error correction level
        error_frame = tk.Frame(options_frame, bg='#f0f0f0')
        error_frame.pack(fill='x', padx=10, pady=(0, 10))
        
        tk.Label(
            error_frame,
            text="Error Correction:",
            font=('Arial', 10),
            bg='#f0f0f0'
        ).pack(side='left')
        
        self.error_var = tk.StringVar(value="Medium")
        error_combo = ttk.Combobox(
            error_frame,
            textvariable=self.error_var,
            values=["Low", "Medium", "High", "Highest"],
            state="readonly",
            width=15
        )
        error_combo.pack(side='left', padx=(10, 0))
        
        # Buttons Frame
        button_frame = tk.Frame(main_frame, bg='#f0f0f0')
        button_frame.pack(fill='x', pady=(0, 20))
        
        self.generate_btn = tk.Button(
            button_frame,
            text="Generate QR Code",
            command=self.generate_qr_code,
            font=('Arial', 12, 'bold'),
            bg='#3498db',
            fg='white',
            relief='flat',
            padx=20,
            pady=10,
            cursor='hand2'
        )
        self.generate_btn.pack(side='left', padx=(0, 10))
        
        self.save_btn = tk.Button(
            button_frame,
            text="Save QR Code",
            command=self.save_qr_code,
            font=('Arial', 12),
            bg='#27ae60',
            fg='white',
            relief='flat',
            padx=20,
            pady=10,
            cursor='hand2',
            state='disabled'
        )
        self.save_btn.pack(side='left', padx=(0, 10))
        
        self.clear_btn = tk.Button(
            button_frame,
            text="Clear",
            command=self.clear_form,
            font=('Arial', 12),
            bg='#e74c3c',
            fg='white',
            relief='flat',
            padx=20,
            pady=10,
            cursor='hand2'
        )
        self.clear_btn.pack(side='right')
        
        # QR Code Display Frame
        self.display_frame = tk.LabelFrame(
            main_frame,
            text="Generated QR Code",
            font=('Arial', 12, 'bold'),
            bg='#f0f0f0',
            fg='#2c3e50'
        )
        self.display_frame.pack(fill='both', expand=True)
        
        # QR Code Label (will hold the image)
        self.qr_label = tk.Label(
            self.display_frame,
            text="QR Code will appear here",
            font=('Arial', 12),
            bg='white',
            fg='gray',
            relief='sunken',
            borderwidth=2
        )
        self.qr_label.pack(expand=True, fill='both', padx=10, pady=10)
        
        # Status bar
        self.status_var = tk.StringVar()
        self.status_var.set("Ready to generate QR codes")
        status_bar = tk.Label(
            self.root,
            textvariable=self.status_var,
            relief='sunken',
            anchor='w',
            bg='#ecf0f1',
            font=('Arial', 9)
        )
        status_bar.pack(side='bottom', fill='x')
        
    def get_size_params(self):
        """
        Get QR code size parameters based on user selection.
        
        Returns:
            tuple: (box_size, border) parameters for QR code generation
        """
        size_map = {
            "Small": (8, 2),
            "Medium": (10, 4),
            "Large": (15, 6)
        }
        return size_map.get(self.size_var.get(), (10, 4))
    
    def get_error_correction(self):
        """
        Get error correction level based on user selection.
        
        Returns:
            qrcode constant: Error correction level
        """
        error_map = {
            "Low": qrcode.constants.ERROR_CORRECT_L,
            "Medium": qrcode.constants.ERROR_CORRECT_M,
            "High": qrcode.constants.ERROR_CORRECT_Q,
            "Highest": qrcode.constants.ERROR_CORRECT_H
        }
        return error_map.get(self.error_var.get(), qrcode.constants.ERROR_CORRECT_M)
    
    def generate_qr_code(self):
        """
        Generate QR code from the input data.
        
        This method validates the input, creates the QR code,
        and displays it in the GUI.
        """
        try:
            # Get input data
            data = self.url_entry.get().strip()
            
            if not data:
                messagebox.showerror("Error", "Please enter a URL or text to generate QR code")
                return
            
            # Update status
            self.status_var.set("Generating QR code...")
            self.root.update()
            
            # Get parameters
            box_size, border = self.get_size_params()
            error_correction = self.get_error_correction()
            
            # Create QR code instance
            qr = qrcode.QRCode(
                version=1,  # Controls the size of the QR Code
                error_correction=error_correction,
                box_size=box_size,
                border=border,
            )
            
            # Add data to QR code
            qr.add_data(data)
            qr.make(fit=True)
            
            # Create QR code image
            self.qr_image = qr.make_image(fill_color="black", back_color="white")
            
            # Resize image for display (maintain aspect ratio)
            display_size = (300, 300)
            display_image = self.qr_image.resize(display_size, Image.Resampling.LANCZOS)
            
            # Convert to PhotoImage for tkinter
            self.photo = ImageTk.PhotoImage(display_image)
            
            # Update the label with the QR code image
            self.qr_label.configure(image=self.photo, text="")
            self.qr_label.image = self.photo  # Keep a reference
            
            # Store current data
            self.current_data = data
            
            # Enable save button
            self.save_btn.configure(state='normal')
            
            # Update status
            self.status_var.set(f"QR code generated successfully for: {data[:50]}...")
            
            # Log generation
            print(f"[{datetime.now().strftime('%H:%M:%S')}] QR code generated for: {data}")
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to generate QR code: {str(e)}")
            self.status_var.set("Error generating QR code")
            print(f"Error: {e}")
    
    def save_qr_code(self):
        """
        Save the generated QR code to a file.
        
        Opens a file dialog for the user to choose where to save the image.
        """
        if not self.qr_image:
            messagebox.showwarning("Warning", "No QR code to save. Please generate one first.")
            return
        
        try:
            # Get filename from user
            filename = filedialog.asksaveasfilename(
                defaultextension=".png",
                filetypes=[
                    ("PNG files", "*.png"),
                    ("JPEG files", "*.jpg"),
                    ("All files", "*.*")
                ],
                title="Save QR Code As"
            )
            
            if filename:
                # Save the image
                self.qr_image.save(filename)
                
                # Update status
                self.status_var.set(f"QR code saved to: {os.path.basename(filename)}")
                
                # Show success message
                messagebox.showinfo("Success", f"QR code saved successfully to:\n{filename}")
                
                # Log save action
                print(f"[{datetime.now().strftime('%H:%M:%S')}] QR code saved to: {filename}")
                
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save QR code: {str(e)}")
            self.status_var.set("Error saving QR code")
    
    def clear_form(self):
        """
        Clear the form and reset the interface.
        """
        # Clear input
        self.url_entry.delete(0, tk.END)
        self.url_entry.insert(0, "https://example.com")
        
        # Reset QR code display
        self.qr_label.configure(image="", text="QR Code will appear here")
        self.qr_image = None
        
        # Reset variables
        self.size_var.set("Medium")
        self.error_var.set("Medium")
        
        # Disable save button
        self.save_btn.configure(state='disabled')
        
        # Update status
        self.status_var.set("Form cleared - Ready to generate QR codes")
        
        print(f"[{datetime.now().strftime('%H:%M:%S')}] Form cleared")


def main():
    """
    Main function to run the QR Code Generator application.
    """
    try:
        # Create main window
        root = tk.Tk()
        
        # Create application instance
        app = QRCodeGenerator(root)
        
        # Set window icon (optional - comment out if no icon file)
        # root.iconbitmap('icon.ico')
        
        # Center window on screen
        root.update_idletasks()
        width = root.winfo_width()
        height = root.winfo_height()
        x = (root.winfo_screenwidth() // 2) - (width // 2)
        y = (root.winfo_screenheight() // 2) - (height // 2)
        root.geometry(f'{width}x{height}+{x}+{y}')
        
        # Start the GUI event loop
        print("Starting Biox Systems QR Code Generator...")
        print("Application ready!")
        root.mainloop()
        
    except ImportError as e:
        print(f"Missing required library: {e}")
        print("Please install required packages:")
        print("pip install qrcode[pil] pillow")
    except Exception as e:
        print(f"Application error: {e}")


if __name__ == "__main__":
    main()