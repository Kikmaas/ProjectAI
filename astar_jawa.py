import tkinter as tk
from tkinter import messagebox
import tkintermapview
import heapq
import math

# ==========================================
# 1. DATA GEOGRAFIS & GRAF (DIPERLUAS)
# ==========================================

# Koordinat Asli 19 Kota di Pulau Jawa
kordinat_kota = {
    'Serang': (-6.1104, 106.1636),
    'Jakarta': (-6.2088, 106.8456),
    'Bogor': (-6.5971, 106.7900),
    'Bandung': (-6.9175, 107.6191),
    'Tasikmalaya': (-7.3274, 108.2232),
    'Cirebon': (-6.7320, 108.5523),
    'Tegal': (-6.8694, 109.1402),
    'Purwokerto': (-7.4245, 109.2302),
    'Semarang': (-6.9667, 110.4167),
    'Magelang': (-7.4797, 110.2177),
    'Salatiga': (-7.3305, 110.5084),
    'Yogyakarta': (-7.7956, 110.3695),
    'Surakarta': (-7.5703, 110.8271),
    'Madiun': (-7.6298, 111.5239),
    'Kediri': (-7.8228, 112.0119),
    'Surabaya': (-7.2575, 112.7521),
    'Malang': (-7.9797, 112.6304),
    'Jember': (-8.1721, 113.6995),
    'Banyuwangi': (-8.2192, 114.3691)
}

# Graf hubungan antar kota (Jarak estimasi dalam KM)
graf_jawa = {
    'Serang': {'Jakarta': 90},
    'Jakarta': {'Serang': 90, 'Bogor': 60, 'Bandung': 150, 'Cirebon': 220},
    'Bogor': {'Jakarta': 60, 'Bandung': 120},
    'Bandung': {'Jakarta': 150, 'Bogor': 120, 'Tasikmalaya': 110, 'Cirebon': 130},
    'Tasikmalaya': {'Bandung': 110, 'Cirebon': 120, 'Purwokerto': 140},
    'Cirebon': {'Jakarta': 220, 'Bandung': 130, 'Tasikmalaya': 120, 'Tegal': 80, 'Semarang': 230},
    'Tegal': {'Cirebon': 80, 'Semarang': 150, 'Purwokerto': 110},
    'Purwokerto': {'Tasikmalaya': 140, 'Tegal': 110, 'Magelang': 100, 'Yogyakarta': 160},
    'Semarang': {'Cirebon': 230, 'Tegal': 150, 'Salatiga': 50, 'Surakarta': 100},
    'Magelang': {'Purwokerto': 100, 'Salatiga': 40, 'Yogyakarta': 45},
    'Salatiga': {'Semarang': 50, 'Magelang': 40, 'Surakarta': 50},
    'Yogyakarta': {'Purwokerto': 160, 'Magelang': 45, 'Surakarta': 60},
    'Surakarta': {'Semarang': 100, 'Salatiga': 50, 'Yogyakarta': 60, 'Madiun': 110},
    'Madiun': {'Surakarta': 110, 'Kediri': 60, 'Surabaya': 160},
    'Kediri': {'Madiun': 60, 'Malang': 100, 'Surabaya': 120},
    'Surabaya': {'Madiun': 160, 'Kediri': 120, 'Malang': 90, 'Jember': 200},
    'Malang': {'Kediri': 100, 'Surabaya': 90, 'Jember': 150},
    'Jember': {'Surabaya': 200, 'Malang': 150, 'Banyuwangi': 100},
    'Banyuwangi': {'Jember': 100}
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

def heuristik(kota_a, kota_b):
    lat1, lon1 = kordinat_kota[kota_a]
    lat2, lon2 = kordinat_kota[kota_b]
    return hitung_jarak_haversine(lat1, lon1, lat2, lon2)

def algoritma_astar(awal, tujuan):
    open_set = []
    heapq.heappush(open_set, (0, awal, [awal]))
    
    g_score = {kota: float('inf') for kota in graf_jawa}
    g_score[awal] = 0
    
    while open_set:
        _, kota_sekarang, jalur = heapq.heappop(open_set)
        
        if kota_sekarang == tujuan:
            return jalur, g_score[tujuan]
            
        for tetangga, jarak in graf_jawa[kota_sekarang].items():
            g_sementara = g_score[kota_sekarang] + jarak
            
            if g_sementara < g_score[tetangga]:
                g_score[tetangga] = g_sementara
                f_score = g_sementara + heuristik(tetangga, tujuan)
                heapq.heappush(open_set, (f_score, tetangga, jalur + [tetangga]))
                
    return None, float('inf')

# ==========================================
# 3. UI DENGAN PETA (TkinterMapView)
# ==========================================

class MapPathfinderApp:
    def __init__(self, root):
        self.root = root
        self.root.title("A* Java Map Pathfinder")
        self.root.geometry("1100x700")

        self.kota_awal = None
        self.kota_tujuan = None
        self.map_path = None 
        self.marker_list = [] 

        self.control_panel = tk.Frame(root, width=250, bg="#f0f0f0", padx=10, pady=10)
        self.control_panel.pack(side="left", fill="y")

        tk.Label(self.control_panel, text="A* Pathfinder Pulau Jawa", font=("Arial", 12, "bold"), bg="#f0f0f0").pack(pady=(0, 10))
        
        instructions = (
            "Cara Penggunaan:\n"
            "1. Klik PIN kota di peta untuk memilih KOTA AWAL (hijau).\n"
            "2. Klik PIN kota lain untuk memilih KOTA TUJUAN (merah).\n"
            "3. Rute tercepat akan otomatis digambar."
        )
        tk.Label(self.control_panel, text=instructions, justify="left", wraplength=230, bg="#f0f0f0").pack(pady=10)

        self.lbl_status = tk.Label(self.control_panel, text="Status: Pilih Kota Awal", fg="blue", bg="#f0f0f0", font=("Arial", 10, "bold"))
        self.lbl_status.pack(pady=15)

        self.lbl_hasil = tk.Label(self.control_panel, text="", justify="left", bg="#f0f0f0", wraplength=230, font=("Arial", 9))
        self.lbl_hasil.pack(pady=10, fill="x")

        tk.Button(self.control_panel, text="Reset Pilihan", command=self.reset_selection, bg="#FF9800", fg="white").pack(side="bottom", fill="x", pady=10)

        self.map_widget = tkintermapview.TkinterMapView(root, width=850, height=700, corner_radius=0)
        self.map_widget.pack(side="right", fill="both", expand=True)

        self.map_widget.set_position(-7.5, 110.0) 
        self.map_widget.set_zoom(7) 

        self.buat_marker_kota()

    def buat_marker_kota(self):
        self.map_widget.delete_all_marker()
        self.marker_list.clear()

        for kota, kord in kordinat_kota.items():
            if kota == self.kota_awal:
                warna = "#28a745" 
            elif kota == self.kota_tujuan:
                warna = "#dc3545" 
            else:
                warna = "#1f6aa5" 

            marker = self.map_widget.set_marker(
                kord[0], kord[1], 
                text=kota, 
                command=self.on_marker_click,
                marker_color_outside=warna
            )
            self.marker_list.append(marker)

    def on_marker_click(self, marker):
        nama_kota = marker.text

        if self.map_path:
            self.map_path.delete()
            self.map_path = None
        self.lbl_hasil.config(text="")

        if self.kota_awal is None:
            self.kota_awal = nama_kota
            self.lbl_status.config(text=f"Awal: {self.kota_awal}. Pilih Tujuan.", fg="#2E7D32")
            self.buat_marker_kota() 
        
        elif self.kota_tujuan is None:
            if nama_kota == self.kota_awal:
                messagebox.showwarning("Perhatian", "Kota tujuan tidak boleh sama dengan kota awal.")
                return

            self.kota_tujuan = nama_kota
            self.lbl_status.config(text=f"Rute: {self.kota_awal} -> {self.kota_tujuan}", fg="black")
            
            self.buat_marker_kota() 
            self.hitung_dan_gambar_rute()
        
        else:
            self.reset_selection()
            self.kota_awal = nama_kota
            self.lbl_status.config(text=f"Awal: {self.kota_awal}. Pilih Tujuan.", fg="#2E7D32")
            self.buat_marker_kota()

    def hitung_dan_gambar_rute(self):
        jalur, total_jarak = algoritma_astar(self.kota_awal, self.kota_tujuan)
        
        if jalur:
            kordinat_jalur = [kordinat_kota[kota] for kota in jalur]
            self.map_path = self.map_widget.set_path(kordinat_jalur, color="green", width=4)
            
            teks_hasil = f"RUTE TERCEPAT (A*)\n\nJalur:\n" + " ➔ ".join(jalur) + f"\n\nTotal Nilai: {round(total_jarak, 2)} KM"
            self.lbl_hasil.config(text=teks_hasil)
        else:
            self.lbl_hasil.config(text="Rute tidak ditemukan dalam graf.")

    def reset_selection(self):
        self.kota_awal = None
        self.kota_tujuan = None
        
        self.buat_marker_kota() 

        if self.map_path:
            self.map_path.delete()
            self.map_path = None
            
        self.lbl_status.config(text="Status: Pilih Kota Awal", fg="blue")
        self.lbl_hasil.config(text="")

if __name__ == "__main__":
    root = tk.Tk()
    app = MapPathfinderApp(root)
    root.mainloop()