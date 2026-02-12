from flask import Flask, render_template, request, jsonify
import json

app = Flask(__name__)

def load_issues_data():
    try:
        with open('static/issues.json', 'r', encoding='utf-8') as f:
            return json.load(f)
    except:
        return None

issues_data = load_issues_data()

@app.route("/")
def index():
    return render_template("index.html")

def get_tips_for_condition(kategori, jenis_masalah, darurat):
    
    tips_list = []
    
    if not issues_data:
        return tips_list
    
    tips_dict = issues_data.get('tips', {}).get(kategori, {})
    tips_darurat_dict = issues_data.get('tips_darurat', {}).get(kategori, {})
    
    # ============================================
    # LISTRIK - Pemadaman listrik
    # ============================================
    if kategori == "listrik" and jenis_masalah == "pemadaman-listrik":
        tips_list.extend([
            tips_dict.get('hubungi-pln-umum'),
            tips_dict.get('catat-durasi-padam'),
            tips_dict.get('siapkan-penerangan-darurat'),
            tips_dict.get('periksa-instalasi-pribadi')
        ])

    elif kategori == "listrik" and jenis_masalah == "pemadaman-listrik" and darurat:
        tips_list.extend([
            tips_darurat_dict.get('hubungi-damkar', 'Hubungi Dinas Damkar 113'),
            tips_darurat_dict.get('evakuasi-area-bahaya', 'Evakuasi area bahaya'),
            tips_darurat_dict.get('siapkan-genset-komunal', 'Siapkan genset komunal'),
            tips_darurat_dict.get('suspend-aktivitas-normal', 'Suspend aktivitas normal')
        ])
    
    # ============================================
    # LISTRIK - Kabel listrik di jalan mengganggu
    # ============================================
    elif kategori == "listrik" and jenis_masalah == "kabel-listrik-di-jalan-mengganggu":
        tips_list.extend([
            tips_dict.get('hubungi-pln-umum'),
            tips_dict.get('ambil-dokumentasi-foto'),
            tips_dict.get('koordinasi-warga-massal', 'Koordinasi warga untuk laporan massal')
        ])

    elif kategori == "listrik" and jenis_masalah == "kabel-listrik-di-jalan-mengganggu" and darurat:
        tips_list.extend([
            tips_darurat_dict.get('hubungi-damkar', 'Hubungi Dinas Damkar 113'),
            tips_darurat_dict.get('evakuasi-area-bahaya', 'Evakuasi area bahaya'),
            tips_darurat_dict.get('siapkan-genset-komunal', 'Siapkan genset komunal'),
            tips_darurat_dict.get('inform-media-massa', 'Inform media massa')
        ])
        
    # ============================================
    # LISTRIK - Kebakaran akibat listrik
    # ============================================
    elif kategori == "listrik" and jenis_masalah == "kebakaran-akibat-listrik":
        tips_list.extend([
            tips_darurat_dict.get('hubungi-damkar', 'Hubungi Damkar 113 SEGERA'),
            tips_darurat_dict.get('evakuasi-area-bahaya', 'Evakuasi area bahaya'),
            tips_darurat_dict.get('siapkan-genset-komunal', 'Siapkan genset komunal')
        ])
    
    # ============================================
    # AIR - Air tidak mengalir
    # ============================================
    elif kategori == "air" and jenis_masalah == "air-tidak-mengalir":
        tips_list.extend([
            tips_dict.get('lapor-pdam-umum', 'Laporkan ke PDAM'),
            tips_dict.get('periksa-kebocoran-rumah', 'Periksa kebocoran rumah'),
            tips_dict.get('sediakan-tangki-air', 'Sediakan tangki air cadangan')
        ])
    elif kategori == "air" and jenis_masalah == "air-tidak-mengalir" and darurat:
        tips_list.extend([
            tips_darurat_dict.get('hubungi-dinkes-emergency', 'Hubungi Dinas Kesehatan emergency'),
            tips_darurat_dict.get('distribusikan-air-darurat', 'Distribusikan air minum darurat'),
            tips_darurat_dict.get('buat-sistem-rationing', 'Buat sistem rationing air'),
            tips_darurat_dict.get('siapkan-water-tanker', 'Siapkan water tanker')
        ])
    
    # ============================================
    # AIR - Kualitas air buruk
    # ============================================
    elif kategori == "air" and jenis_masalah == "kualitas-air-buruk":
         tips_list.extend([
                tips_dict.get('dokumentasi-kualitas', 'Dokumentasi sampel air'),
                tips_dict.get('lapor-ke-dinkes', 'Laporkan ke Dinas Kesehatan'),
                tips_dict.get('lapor-pdam-umum', 'Laporkan ke PDAM')
            ])
    elif kategori == "air" and jenis_masalah == "kualitas-air-buruk" and darurat:
        tips_list.extend([
            tips_darurat_dict.get('hubungi-dinkes-emergency', 'Hubungi Dinas Kesehatan emergency'),
            tips_darurat_dict.get('monitoring-penyakit', 'Monitoring penyakit terkait air'),
            tips_darurat_dict.get('siapkan-water-tanker', 'Siapkan water tanker'),
            tips_darurat_dict.get('inform-media-international', 'Inform media jika sangat severe')
        ])
           
    # ============================================
    # AIR - Kebocoran pipa distribusi
    # ============================================
    elif kategori == "air" and jenis_masalah == "kebocoran-pipa-distribusi":
        tips_list.extend([
                tips_dict.get('lapor-pdam-umum', 'Laporkan ke PDAM'),
                tips_dict.get('dokumentasi-kualitas', 'Dokumentasi lokasi kebocoran'),
                tips_dict.get('lapor-ke-dinkes', 'Catat waktu dan durasi kebocoran')
            ])
    elif kategori == "air" and jenis_masalah == "kebocoran-pipa-distribusi" and darurat:
        tips_list.extend([
            tips_darurat_dict.get('distribusikan-air-darurat', 'Distribusikan air minum darurat'),
            tips_darurat_dict.get('buat-sistem-rationing', 'Buat sistem rationing air'),
            tips_darurat_dict.get('setup-water-distribution-point', 'Setup water distribution point'),
            tips_darurat_dict.get('siapkan-water-tanker', 'Siapkan water tanker')
        ])       
    
    # ============================================
    # SAMPAH - Sampah menumpuk tidak diangkut
    # ============================================
    elif kategori == "sampah" and jenis_masalah == "sampah-menumpuk-tidak-diangkut":
        tips_list.extend([
                tips_dict.get('lapor-dinas-kebersihan', 'Laporkan ke Dinas Kebersihan'),
                tips_dict.get('dokumentasi-volume-sampah', 'Dokumentasi volume sampah'),
                tips_dict.get('edukasi-pemilahan-awal', 'Edukasi pemilahan sampah'),
                tips_dict.get('batasi-pembakaran-sampah', 'Batasi pembakaran sampah')
            ])
    elif kategori == "sampah" and jenis_masalah == "sampah-menumpuk-tidak-diangkut" and darurat:
        tips_list.extend([
            tips_darurat_dict.get('hubungi-dinkes-sanitation', 'Hubungi Dinas Kesehatan'),
            tips_darurat_dict.get('establish-emergency-dump', 'Establish emergency dump site'),
            tips_darurat_dict.get('koordinasi-heavy-equipment', 'Koordinasi heavy equipment'),
            tips_darurat_dict.get('setup-emergency-tpa', 'Setup emergency TPA sementara')
        ])
            
    
    # ============================================
    # SAMPAH - Sungai tersumbat sampah
    # ============================================
    elif kategori == "sampah" and jenis_masalah == "sungai-tersumbat-sampah":
        tips_list.extend([
            tips_dict.get('lapor-dinas-kebersihan', 'Laporkan ke Dinas Kebersihan dan Lingkungan'),
            tips_dict.get('dokumentasi-volume-sampah', 'Dokumentasi kondisi sungai'),
            tips_dict.get('edukasi-pemilahan-awal', 'Edukasi warga tentang pembuangan sampah')
        ])
    elif kategori == "sampah" and jenis_masalah == "sungai-tersumbat-sampah" and darurat:
        tips_list.extend([
            tips_darurat_dict.get('hubungi-dinkes-sanitation', 'Hubungi Dinas Kesehatan'),
            tips_darurat_dict.get('implementasi-lockdown-area', 'Implementasi lockdown area'),
            tips_darurat_dict.get('evakuasi-area-tercemar', 'Evakuasi area tercemar'),
            tips_darurat_dict.get('setup-emergency-tpa', 'Setup emergency TPA sementara')
        ])
    
    # ============================================
    # SAMPAH - Sampah B3 dibuang sembarangan
    # ============================================
    elif kategori == "sampah" and jenis_masalah == "sampah-b3-dibuang-sembarangan":
        tips_list.extend([
            tips_dict.get('lapor-ke-dinkes', 'Laporkan ke Dinas Kesehatan dan Lingkungan'),
            tips_dict.get('dokumentasi-kualitas', 'Dokumentasi lokasi dan jenis sampah B3')
        ])
    elif kategori == "sampah" and jenis_masalah == "sampah-b3-dibuang-sembarangan" and darurat:
        tips_list.extend([
            tips_darurat_dict.get('hubungi-dinkes-sanitation', 'Hubungi Dinas Kesehatan'),
            tips_darurat_dict.get('implementasi-lockdown-area', 'Implementasi lockdown area'),
            tips_darurat_dict.get('siapkan-ppe-workers', 'Siapkan PPE lengkap untuk workers'),
            tips_darurat_dict.get('evakuasi-area-tercemar', 'Evakuasi area tercemar')
        ])
    
    # ============================================
    # DEFAULT - Jika tidak ada kondisi spesifik
    # ============================================
    else:
        if not darurat:
            tips_list.extend([
                "Laporkan ke dinas terkait",
                "Dokumentasikan kondisi dengan foto/video",
                "Koordinasikan dengan komunitas lokal"
            ])
        else:
            tips_list.extend([
                "Hubungi dinas terkait untuk situasi darurat",
                "Evakuasi dari area jika diperlukan",
                "Dokumentasikan kondisi dengan foto/video",
                "Koordinasikan dengan komunitas lokal"
            ])
    
    seen = set()
    unique_tips = []
    for tip in tips_list:
        if tip not in seen:
            seen.add(tip)
            unique_tips.append(tip)
    
    return unique_tips


@app.route('/submit', methods=['POST'])
def submit():
    try:
        kategori_layanan = request.form.get('mainCategory', '').strip()
        jenis_masalah = request.form.get('issueType', '')
        status_darurat = request.form.get('status_darurat', 'off') == 'on'
        
        if not kategori_layanan:
            return jsonify({'status': 'error', 'error': 'Kategori utama belum dipilih'}), 400
        
        if not jenis_masalah:
            return jsonify({'status': 'error', 'error': 'Jenis masalah belum dipilih'}), 400
        
        tips_output = get_tips_for_condition(kategori_layanan, jenis_masalah, status_darurat)
        
        response_data = {
            'status': 'success',
            'kategori_layanan': kategori_layanan,
            'jenis_masalah': jenis_masalah,
            'status_darurat': 'DARURAT' if status_darurat else '',
            'tips': tips_output
        }
        
        return jsonify(response_data), 200
    
    except Exception as e:
        return jsonify({'status': 'error', 'error': f'Server error: {str(e)}'}), 500


if __name__ == "__main__":
    app.run(debug=True, port=5000)
