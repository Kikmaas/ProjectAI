import ctypes
import tkinter as tk
from tkinter import messagebox, ttk
import tkintermapview
import heapq
import math
import requests

try:
    ctypes.windll.shcore.SetProcessDpiAwareness(1)
except Exception:
    pass

# ==========================================
# 1. DATA GEOGRAFIS WISATA & GRAF
# ==========================================

kordinat_wisata = {
    'Pantai Anyer (Banten)': (-6.0753, 105.8856),
    'Ancol (Jakarta)': (-6.1246, 106.8322),
    'Monas (Jakarta)': (-6.1754, 106.8272),
    'Kebun Raya Bogor': (-6.5976, 106.7996),
    'Taman Safari (Puncak)': (-6.7171, 106.9452),
    'Tangkuban Perahu (Bandung)': (-6.7596, 107.6098),
    'Kawah Putih (Ciwidey)': (-7.1662, 107.4021),
    'Pantai Pangandaran': (-7.7011, 108.6536),
    'Lawang Sewu (Semarang)': (-6.9839, 110.4104),
    'Dieng Plateau (Wonosobo)': (-7.2029, 109.9142),
    'Candi Borobudur (Magelang)': (-7.6079, 110.2038),
    'Malioboro (Jogja)': (-7.7926, 110.3658),
    'Pantai Parangtritis (Jogja)': (-8.0255, 110.3297),
    'Candi Prambanan': (-7.7520, 110.4915),
    'Keraton Solo': (-7.5778, 110.8282),
    'Tawangmangu (Karanganyar)': (-7.6622, 111.1215),
    'Kebun Binatang Surabaya': (-7.2954, 112.7352),
    'Jatim Park (Batu)': (-7.8860, 112.5283),
    'Gunung Bromo': (-7.9425, 112.9530),
    'Kawah Ijen (Banyuwangi)': (-8.0584, 114.2420),
    'TN Baluran (Situbondo)': (-7.8284, 114.3750)
}

info_wisata = {
    'Pantai Anyer (Banten)': {'jam': '24 Jam', 'tiket': 'Rp 25.000'},
    'Ancol (Jakarta)': {'jam': '06:00 - 23:00', 'tiket': 'Rp 30.000'},
    'Monas (Jakarta)': {'jam': '06:00 - 16:00', 'tiket': 'Rp 15.000'},
    'Kebun Raya Bogor': {'jam': '08:00 - 16:00', 'tiket': 'Rp 16.500'},
    'Taman Safari (Puncak)': {'jam': '08:30 - 17:00', 'tiket': 'Rp 230.000'},
    'Tangkuban Perahu (Bandung)': {'jam': '07:00 - 17:00', 'tiket': 'Rp 20.000'},
    'Kawah Putih (Ciwidey)': {'jam': '07:30 - 17:00', 'tiket': 'Rp 28.000'},
    'Pantai Pangandaran': {'jam': '24 Jam', 'tiket': 'Rp 10.000'},
    'Lawang Sewu (Semarang)': {'jam': '08:00 - 20:00', 'tiket': 'Rp 20.000'},
    'Dieng Plateau (Wonosobo)': {'jam': '07:00 - 17:00', 'tiket': 'Rp 20.000'},
    'Candi Borobudur (Magelang)': {'jam': '06:30 - 16:30', 'tiket': 'Rp 50.000'},
    'Malioboro (Jogja)': {'jam': '24 Jam', 'tiket': 'Gratis'},
    'Pantai Parangtritis (Jogja)': {'jam': '24 Jam', 'tiket': 'Rp 10.000'},
    'Candi Prambanan': {'jam': '06:30 - 17:00', 'tiket': 'Rp 50.000'},
    'Keraton Solo': {'jam': '09:00 - 14:00', 'tiket': 'Rp 15.000'},
    'Tawangmangu (Karanganyar)': {'jam': '08:00 - 17:00', 'tiket': 'Rp 20.000'},
    'Kebun Binatang Surabaya': {'jam': '08:00 - 16:00', 'tiket': 'Rp 15.000'},
    'Jatim Park (Batu)': {'jam': '09:30 - 17:30', 'tiket': 'Rp 140.000'},
    'Gunung Bromo': {'jam': '24 Jam', 'tiket': 'Rp 29.000'},
    'Kawah Ijen (Banyuwangi)': {'jam': '02:00 - 12:00', 'tiket': 'Rp 7.500'},
    'TN Baluran (Situbondo)': {'jam': '07:30 - 16:00', 'tiket': 'Rp 15.000'}
}

graf_wisata = {
    'Pantai Anyer (Banten)': {'Ancol (Jakarta)': 130},
    'Ancol (Jakarta)': {'Pantai Anyer (Banten)': 130, 'Monas (Jakarta)': 10},
    'Monas (Jakarta)': {'Ancol (Jakarta)': 10, 'Kebun Raya Bogor': 60},
    'Kebun Raya Bogor': {'Monas (Jakarta)': 60, 'Taman Safari (Puncak)': 30, 'Kawah Putih (Ciwidey)': 160},
    'Taman Safari (Puncak)': {'Kebun Raya Bogor': 30, 'Tangkuban Perahu (Bandung)': 90},
    'Tangkuban Perahu (Bandung)': {'Taman Safari (Puncak)': 90, 'Kawah Putih (Ciwidey)': 60, 'Dieng Plateau (Wonosobo)': 260},
    'Kawah Putih (Ciwidey)': {'Kebun Raya Bogor': 160, 'Tangkuban Perahu (Bandung)': 60, 'Pantai Pangandaran': 190},
    'Pantai Pangandaran': {'Kawah Putih (Ciwidey)': 190, 'Candi Borobudur (Magelang)': 210},
    'Dieng Plateau (Wonosobo)': {'Tangkuban Perahu (Bandung)': 260, 'Lawang Sewu (Semarang)': 100, 'Candi Borobudur (Magelang)': 60},
    'Lawang Sewu (Semarang)': {'Dieng Plateau (Wonosobo)': 100, 'Keraton Solo': 105},
    'Candi Borobudur (Magelang)': {'Pantai Pangandaran': 210, 'Dieng Plateau (Wonosobo)': 60, 'Malioboro (Jogja)': 40},
    'Malioboro (Jogja)': {'Candi Borobudur (Magelang)': 40, 'Pantai Parangtritis (Jogja)': 30, 'Candi Prambanan': 18},
    'Pantai Parangtritis (Jogja)': {'Malioboro (Jogja)': 30},
    'Candi Prambanan': {'Malioboro (Jogja)': 18, 'Keraton Solo': 50},
    'Keraton Solo': {'Lawang Sewu (Semarang)': 105, 'Candi Prambanan': 50, 'Tawangmangu (Karanganyar)': 40, 'Kebun Binatang Surabaya': 260},
    'Tawangmangu (Karanganyar)': {'Keraton Solo': 40, 'Jatim Park (Batu)': 230},
    'Kebun Binatang Surabaya': {'Keraton Solo': 260, 'Jatim Park (Batu)': 100, 'Gunung Bromo': 130},
    'Jatim Park (Batu)': {'Tawangmangu (Karanganyar)': 230, 'Kebun Binatang Surabaya': 100, 'Gunung Bromo': 70},
    'Gunung Bromo': {'Jatim Park (Batu)': 70, 'Kebun Binatang Surabaya': 130, 'Kawah Ijen (Banyuwangi)': 200},
    'Kawah Ijen (Banyuwangi)': {'Gunung Bromo': 200, 'TN Baluran (Situbondo)': 60},
    'TN Baluran (Situbondo)': {'Kawah Ijen (Banyuwangi)': 60}
}

# ==========================================
# 2. LOGIKA ALGORITMA A*
# ==========================================

def hitung_jarak_haversine(lat1, lon1, lat2, lon2):
    R = 6371 
    dLat = math.radians(lat2 - lat1)
    dLon = math.radians(lon2 - lon1)
    a = math.sin(dLat/2) * math.sin(dLat/2) + \
        math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) * \
        math.sin(dLon/2) * math.sin(dLon/2)
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))
    return R * c

def heuristik(lokasi_a, lokasi_b):
    lat1, lon1 = kordinat_wisata[lokasi_a]
    lat2, lon2 = kordinat_wisata[lokasi_b]
    return hitung_jarak_haversine(lat1, lon1, lat2, lon2)

def algoritma_astar(awal, tujuan):
    open_set = []
    heapq.heappush(open_set, (0, awal, [awal]))
    
    g_score = {lokasi: float('inf') for lokasi in graf_wisata}
    g_score[awal] = 0
    
    while open_set:
        _, lokasi_sekarang, jalur = heapq.heappop(open_set)
        
        if lokasi_sekarang == tujuan:
            return jalur, g_score[tujuan]
            
        for tetangga, jarak in graf_wisata[lokasi_sekarang].items():
            g_sementara = g_score[lokasi_sekarang] + jarak
            
            if g_sementara < g_score[tetangga]:
                g_score[tetangga] = g_sementara
                f_score = g_sementara + heuristik(tetangga, tujuan)
                heapq.heappush(open_set, (f_score, tetangga, jalur + [tetangga]))
                
    return None, float('inf')

def dapatkan_lokasi_saat_ini():
    """Mengambil koordinat Latitude & Longitude berdasarkan IP Address"""
    try:
        # Memanggil API Geolocation gratis
        response = requests.get('http://ip-api.com/json/')
        data = response.json()
        if data['status'] == 'success':
            return data['lat'], data['lon'], data['city']
        return None, None, None
    except:
        messagebox.showerror("Error", "Gagal mendapatkan lokasi. Pastikan internet terhubung.")
        return None, None, None

# ==========================================
# 3. UI DENGAN PETA (TkinterMapView)
# ==========================================

class MapPathfinderApp:
    def __init__(self, root):
        self.root = root
        self.root.title("A* Roadtrip Wisata Jawa")
        self.root.geometry("1200x750")
        
        # --- COLOR PALETTE ---
        self.bg_sidebar = "#1E1E2E"       
        self.bg_content = "#CDD6F4"       
        self.color_accent = "#89B4FA"     
        self.color_start = "#A6E3A1"      
        self.color_end = "#F38BA8"        
        self.color_default = "#F9E2AF"    
        self.color_path = "#A6E3A1"       

        self.lokasi_awal = None
        self.lokasi_tujuan = None
        self.map_path = None 
        self.marker_list = [] 

        # --- SIDEBAR ---
        self.control_panel = tk.Frame(root, width=340, bg=self.bg_sidebar)
        self.control_panel.pack(side="left", fill="y")
        self.control_panel.pack_propagate(False) 

        tk.Label(self.control_panel, text="🌴 A* Roadtrip", font=("Segoe UI", 20, "bold"), bg=self.bg_sidebar, fg=self.color_accent).pack(pady=(30, 5), padx=20, anchor="w")
        tk.Label(self.control_panel, text="Edisi Wisata Mainstream Jawa", font=("Segoe UI", 10), bg=self.bg_sidebar, fg="#A6ADC8").pack(pady=(0, 10), padx=20, anchor="w")

        tk.Frame(self.control_panel, height=1, bg="#313244").pack(fill="x", padx=20, pady=5)

        # --- FITUR PENCARIAN (DROPDOWN) ---
        search_frame = tk.Frame(self.control_panel, bg=self.bg_sidebar)
        search_frame.pack(fill="x", padx=20, pady=10)
        
        tk.Label(search_frame, text="PILIH RUTE", font=("Segoe UI", 9, "bold"), bg=self.bg_sidebar, fg="#A6ADC8").pack(anchor="w", pady=(0,5))

        # Mengatur style combobox agar lebih rapi
        style = ttk.Style()
        style.theme_use('clam')
        
        self.combo_awal = ttk.Combobox(search_frame, values=list(kordinat_wisata.keys()), state="readonly")
        self.combo_awal.pack(fill="x", pady=2)
        self.combo_awal.set("Titik Keberangkatan...")

        self.combo_tujuan = ttk.Combobox(search_frame, values=list(kordinat_wisata.keys()), state="readonly")
        self.combo_tujuan.pack(fill="x", pady=2)
        self.combo_tujuan.set("Tujuan Akhir...")

        self.btn_cari = tk.Button(
            search_frame, 
            text="🔍 Cari Rute", 
            font=("Segoe UI", 9, "bold"), 
            bg=self.color_accent, 
            fg="#11111B", 
            relief="flat", 
            cursor="hand2",
            command=self.cari_via_dropdown
        )
        self.btn_cari.pack(fill="x", pady=5)

        self.btn_lokasi_saya = tk.Button(
            search_frame, 
            text="📍 Lokasi Saya Saat Ini", 
            font=("Segoe UI", 9, "bold"), 
            bg="#89DCEB",
            fg="#11111B", 
            relief="flat", 
            cursor="hand2",
            command=self.tampilkan_lokasi_saya
        )
        self.btn_lokasi_saya.pack(fill="x", pady=(10, 5))

        tk.Frame(self.control_panel, height=1, bg="#313244").pack(fill="x", padx=20, pady=5)

        self.lbl_status = tk.Label(self.control_panel, text="Pilih rute dari daftar/peta", fg=self.color_accent, bg=self.bg_sidebar, font=("Segoe UI", 11, "bold"))
        self.lbl_status.pack(pady=10, padx=20, anchor="w")

        # Scrollable Frame untuk Hasil yang Panjang
        self.result_canvas = tk.Canvas(self.control_panel, bg="#313244", bd=0, highlightthickness=0)
        self.scrollbar = tk.Scrollbar(self.control_panel, orient="vertical", command=self.result_canvas.yview)
        self.result_frame = tk.Frame(self.result_canvas, bg="#313244", padx=15, pady=15)

        self.result_canvas.pack(fill="both", expand=True, padx=(20, 0), pady=5)
        self.scrollbar.pack(side="right", fill="y", pady=5)
        
        self.result_canvas.create_window((0, 0), window=self.result_frame, anchor="nw", width=290)
        self.result_canvas.configure(yscrollcommand=self.scrollbar.set)
        
        self.lbl_hasil = tk.Label(self.result_frame, text="Belum ada rute\nyang dihitung.", justify="left", bg="#313244", fg=self.bg_content, wraplength=250, font=("Segoe UI", 10))
        self.lbl_hasil.pack(fill="x", anchor="w")

        self.result_frame.bind("<Configure>", lambda e: self.result_canvas.configure(scrollregion=self.result_canvas.bbox("all")))

        self.btn_reset = tk.Button(
            self.control_panel, 
            text="🔄 Reset Rute", 
            font=("Segoe UI", 10, "bold"), 
            bg="#F38BA8", 
            fg="#11111B", 
            relief="flat", 
            activebackground="#EBA0AC",
            cursor="hand2",
            command=self.reset_selection,
            pady=8
        )
        self.btn_reset.pack(side="bottom", fill="x", padx=20, pady=20)

        # --- MAP WIDGET ---
        self.map_frame = tk.Frame(root, bg="#11111B")
        self.map_frame.pack(side="right", fill="both", expand=True)

        self.map_widget = tkintermapview.TkinterMapView(self.map_frame, corner_radius=0)
        self.map_widget.pack(fill="both", expand=True)

        # SETTING SERVER GOOGLE MAPS BIAR NGEBUT
        self.map_widget.set_tile_server("https://mt0.google.com/vt/lyrs=m&hl=en&x={x}&y={y}&z={z}&s=Ga", max_zoom=22)

        # Posisi default di tengah Pulau Jawa
        self.map_widget.set_position(-7.5, 110.0) 
        self.map_widget.set_zoom(7.5) 

        self.buat_marker_wisata()

    def tampilkan_lokasi_saya(self):
        self.lbl_status.config(text="Mencari lokasi...", fg=self.color_accent)
        self.root.update() # Memaksa UI untuk render teks status

        lat, lon, kota = dapatkan_lokasi_saat_ini()
        
        if lat and lon:
            # Hapus path lama jika ada
            if self.map_path:
                self.map_path.delete()
                self.map_path = None
                
            # Set posisi peta ke lokasi user dan beri zoom
            self.map_widget.set_position(lat, lon)
            self.map_widget.set_zoom(12)
            
            # Berikan marker khusus warna biru (melambangkan lokasi user)
            self.map_widget.set_marker(
                lat, lon, 
                text=f"Lokasi Kamu ({kota})", 
                marker_color_circle="white",
                marker_color_outside="#1E90FF" # Biru terang ala Google Maps
            )
            self.lbl_status.config(text=f"Lokasi terdeteksi di sekitar {kota}", fg="#A6E3A1")
        else:
            self.lbl_status.config(text="Gagal mendeteksi lokasi", fg=self.color_end)

    def cari_via_dropdown(self):
        awal = self.combo_awal.get()
        tujuan = self.combo_tujuan.get()

        if awal not in kordinat_wisata or tujuan not in kordinat_wisata:
            messagebox.showwarning("Perhatian", "Silakan pilih titik keberangkatan dan tujuan dari dropdown!")
            return

        if awal == tujuan:
            messagebox.showwarning("Perhatian", "Tujuan tidak boleh sama dengan titik awal.")
            return

        # [PERBAIKAN BUG]: Hapus garis rute lama jika ada sebelum mencari rute baru
        if self.map_path:
            self.map_path.delete()
            self.map_path = None

        self.lokasi_awal = awal
        self.lokasi_tujuan = tujuan
        self.lbl_status.config(text="Rute Wisata Ditemukan!", fg=self.color_end)
        
        self.buat_marker_wisata()
        self.hitung_dan_gambar_rute()

    def buat_marker_wisata(self):
        self.map_widget.delete_all_marker()
        self.marker_list.clear()

        for lokasi, kord in kordinat_wisata.items():
            if lokasi == self.lokasi_awal:
                warna = self.color_start
            elif lokasi == self.lokasi_tujuan:
                warna = self.color_end
            else:
                warna = self.color_default

            marker = self.map_widget.set_marker(
                kord[0], kord[1], 
                text=lokasi, 
                command=self.on_marker_click,
                marker_color_circle="#1E1E2E",
                marker_color_outside=warna
            )
            self.marker_list.append(marker)

    def on_marker_click(self, marker):
        nama_lokasi = marker.text

        if self.map_path:
            self.map_path.delete()
            self.map_path = None
        self.lbl_hasil.config(text="Menunggu tujuan liburan...")

        if self.lokasi_awal is None:
            self.lokasi_awal = nama_lokasi
            self.combo_awal.set(nama_lokasi) # Sinkronisasi dropdown
            self.lbl_status.config(text=f"Start: {self.lokasi_awal}", fg=self.color_start)
            self.buat_marker_wisata() 
        
        elif self.lokasi_tujuan is None:
            if nama_lokasi == self.lokasi_awal:
                messagebox.showwarning("Perhatian", "Tujuan tidak boleh sama dengan titik awal.")
                return

            self.lokasi_tujuan = nama_lokasi
            self.combo_tujuan.set(nama_lokasi) # Sinkronisasi dropdown
            self.lbl_status.config(text="Rute Wisata Ditemukan!", fg=self.color_end)
            
            self.buat_marker_wisata() 
            self.hitung_dan_gambar_rute()
        
        else:
            self.reset_selection()
            self.lokasi_awal = nama_lokasi
            self.combo_awal.set(nama_lokasi)
            self.lbl_status.config(text=f"Start: {self.lokasi_awal}", fg=self.color_start)
            self.buat_marker_wisata()

    def hitung_dan_gambar_rute(self):
        jalur, total_jarak = algoritma_astar(self.lokasi_awal, self.lokasi_tujuan)
        
        # [PERBAIKAN BUG]: Pastikan jalur sebelumnya benar-benar terhapus sebelum menggambar ulang
        if self.map_path:
            self.map_path.delete()
            self.map_path = None
            
        if jalur:
            kordinat_jalur = [kordinat_wisata[lokasi] for lokasi in jalur]
            self.map_path = self.map_widget.set_path(kordinat_jalur, color=self.color_path, width=4)
            
            # Merangkai Output Teks dengan Informasi Pariwisata
            jalur_str = ""
            for i, lokasi in enumerate(jalur):
                info = info_wisata.get(lokasi, {})
                jam = info.get('jam', '-')
                tiket = info.get('tiket', '-')
                
                if i == 0:
                    simbol = "📍 [START]"
                elif i == len(jalur) - 1:
                    simbol = "🏁 [FINISH]"
                else:
                    simbol = "🚗 [LEWAT]"
                    
                jalur_str += f"{simbol} {lokasi}\n      🕒 Buka: {jam}\n      🎟️ Tiket: {tiket}\n\n"

            teks_hasil = f"ESTIMASI JARAK:\n{round(total_jarak, 2)} KM\n\nITINERARY PERJALANAN:\n\n{jalur_str}"
            self.lbl_hasil.config(text=teks_hasil)
        else:
            self.lbl_hasil.config(text="Jalur darat antar lokasi wisata ini belum terhubung di graf.")

    def reset_selection(self):
        self.lokasi_awal = None
        self.lokasi_tujuan = None
        
        self.combo_awal.set("Titik Keberangkatan...")
        self.combo_tujuan.set("Tujuan Akhir...")
        
        self.buat_marker_wisata() 

        if self.map_path:
            self.map_path.delete()
            self.map_path = None
            
        self.lbl_status.config(text="Pilih rute dari daftar/peta", fg=self.color_accent)
        self.lbl_hasil.config(text="Belum ada rute\nyang dihitung.")

if __name__ == "__main__":
    root = tk.Tk()
    app = MapPathfinderApp(root)
    root.mainloop()