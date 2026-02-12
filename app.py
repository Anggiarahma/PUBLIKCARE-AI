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

def get_tips_for_condition(kategori_layanan, jenis_masalah, darurat):
    
    tips_list = []
    
    if not issues_data:
        return tips_list
    
    tips_dict = issues_data.get('tips', {}).get(kategori_layanan, {})
    tips_darurat_dict = issues_data.get('tips_darurat', {}).get(kategori_layanan, {})
    
    # ============================================
    # LISTRIK - Pemadaman listrik
    # ============================================
    if kategori_layanan == "listrik" and jenis_masalah == "pemadaman-listrik" and not darurat:
        tips_list.extend([
            tips_dict.get('hubungi-pln-umum'),
            tips_dict.get('catat-durasi-padam'),
            tips_dict.get('siapkan-penerangan-darurat'),
            tips_dict.get('periksa-instalasi-pribadi')
        ])

    elif kategori_layanan == "listrik" and jenis_masalah == "pemadaman-listrik" and darurat:
        tips_list.extend([
            tips_darurat_dict.get('hubungi-damkar'),
            tips_darurat_dict.get('evakuasi-area-bahaya'),
            tips_darurat_dict.get('siapkan-genset-komunal'),
            tips_darurat_dict.get('suspend-aktivitas-normal')
        ])
    
    # ============================================
    # LISTRIK - Kabel listrik di jalan mengganggu
    # ============================================
    elif kategori_layanan == "listrik" and jenis_masalah == "kabel-listrik-di-jalan-mengganggu" and not darurat:
        tips_list.extend([
            tips_dict.get('hubungi-pln-umum'),
            tips_dict.get('ambil-dokumentasi-foto'),
            tips_dict.get('koordinasi-warga-massal')
        ])

    elif kategori_layanan == "listrik" and jenis_masalah == "kabel-listrik-di-jalan-mengganggu" and darurat:
        tips_list.extend([
            tips_darurat_dict.get('hubungi-damkar'),
            tips_darurat_dict.get('evakuasi-area-bahaya'),
            tips_darurat_dict.get('siapkan-genset-komunal'),
            tips_darurat_dict.get('inform-media-massa')
        ])
        
    # ============================================
    # LISTRIK - Kebakaran akibat listrik
    # ============================================
    elif kategori_layanan == "listrik" and jenis_masalah == "kebakaran-akibat-listrik":
        tips_list.extend([
            tips_darurat_dict.get('hubungi-damkar'),
            tips_darurat_dict.get('evakuasi-area-bahaya'),
            tips_darurat_dict.get('siapkan-genset-komunal')
        ])
    
    # ============================================
    # AIR - Air tidak mengalir
    # ============================================
    elif kategori_layanan == "air" and jenis_masalah == "air-tidak-mengalir" and not darurat:
        tips_list.extend([
            tips_dict.get('lapor-pdam-umum'),
            tips_dict.get('periksa-kebocoran-rumah'),
            tips_dict.get('sediakan-tangki-air')
        ])
    elif kategori_layanan == "air" and jenis_masalah == "air-tidak-mengalir" and darurat:
        tips_list.extend([
            tips_darurat_dict.get('hubungi-dinkes-emergency'),
            tips_darurat_dict.get('distribusikan-air-darurat'),
            tips_darurat_dict.get('buat-sistem-rationing'),
            tips_darurat_dict.get('siapkan-water-tanker')
        ])
    
    # ============================================
    # AIR - Kualitas air buruk
    # ============================================
    elif kategori_layanan == "air" and jenis_masalah == "kualitas-air-buruk" and not darurat:
         tips_list.extend([
                tips_dict.get('dokumentasi-kualitas'),
                tips_dict.get('lapor-ke-dinkes'),
                tips_dict.get('lapor-pdam-umum')
            ])
    elif kategori_layanan == "air" and jenis_masalah == "kualitas-air-buruk" and darurat:
        tips_list.extend([
            tips_darurat_dict.get('hubungi-dinkes-emergency'),
            tips_darurat_dict.get('monitoring-penyakit'),
            tips_darurat_dict.get('siapkan-water-tanker'),
            tips_darurat_dict.get('inform-media-international')
        ])
           
    # ============================================
    # AIR - Kebocoran pipa distribusi
    # ============================================
    elif kategori_layanan == "air" and jenis_masalah == "kebocoran-pipa-distribusi" and not darurat:
        tips_list.extend([
                tips_dict.get('lapor-pdam-umum'),
                tips_dict.get('dokumentasi-kualitas'),
                tips_dict.get('lapor-ke-dinkes')
            ])
    elif kategori_layanan == "air" and jenis_masalah == "kebocoran-pipa-distribusi" and darurat:
        tips_list.extend([
            tips_darurat_dict.get('distribusikan-air-darurat'),
            tips_darurat_dict.get('buat-sistem-rationing'),
            tips_darurat_dict.get('setup-water-distribution-point'),
            tips_darurat_dict.get('siapkan-water-tanker')
        ])       
    
    # ============================================
    # SAMPAH - Sampah menumpuk tidak diangkut
    # ============================================
    elif kategori_layanan == "sampah" and jenis_masalah == "sampah-menumpuk-tidak-diangkut" and not darurat:
        tips_list.extend([
                tips_dict.get('lapor-dinas-kebersihan'),
                tips_dict.get('dokumentasi-volume-sampah'),
                tips_dict.get('edukasi-pemilahan-awal'),
                tips_dict.get('batasi-pembakaran-sampah')
            ])
    elif kategori_layanan == "sampah" and jenis_masalah == "sampah-menumpuk-tidak-diangkut" and darurat:
        tips_list.extend([
            tips_darurat_dict.get('hubungi-dinkes-sanitation'),
            tips_darurat_dict.get('establish-emergency-dump'),
            tips_darurat_dict.get('koordinasi-heavy-equipment'),
            tips_darurat_dict.get('setup-emergency-tpa')
        ])
            
    
    # ============================================
    # SAMPAH - Sungai tersumbat sampah
    # ============================================
    elif kategori_layanan == "sampah" and jenis_masalah == "sungai-tersumbat-sampah" and not darurat:
        tips_list.extend([
            tips_dict.get('lapor-dinas-kebersihan'),
            tips_dict.get('dokumentasi-volume-sampah'),
            tips_dict.get('edukasi-pemilahan-awal')
        ])
    elif kategori_layanan == "sampah" and jenis_masalah == "sungai-tersumbat-sampah" and darurat:
        tips_list.extend([
            tips_darurat_dict.get('hubungi-dinkes-sanitation'),
            tips_darurat_dict.get('implementasi-lockdown-area'),
            tips_darurat_dict.get('evakuasi-area-tercemar'),
            tips_darurat_dict.get('setup-emergency-tpa')
        ])
    
    # ============================================
    # SAMPAH - Sampah B3 dibuang sembarangan
    # ============================================
    elif kategori_layanan == "sampah" and jenis_masalah == "sampah-b3-dibuang-sembarangan" and not darurat:
        tips_list.extend([
            tips_dict.get('lapor-ke-dinkes'),
            tips_dict.get('dokumentasi-kualitas')
        ])
    elif kategori_layanan == "sampah" and jenis_masalah == "sampah-b3-dibuang-sembarangan" and darurat:
        tips_list.extend([
            tips_darurat_dict.get('hubungi-dinkes-sanitation'),
            tips_darurat_dict.get('implementasi-lockdown-area'),
            tips_darurat_dict.get('siapkan-ppe-workers'),
            tips_darurat_dict.get('evakuasi-area-tercemar')
        ])
    
    # ============================================
    # DEFAULT - Jika tidak ada kondisi spesifik
    # ============================================
    else:
        if darurat:
            tips_list.extend([
                "Hubungi dinas terkait untuk situasi darurat",
                "Evakuasi dari area jika diperlukan",
                "Dokumentasikan kondisi dengan foto/video",
                "Koordinasikan dengan komunitas lokal"
            ])
        else:
            tips_list.extend([
                "Laporkan ke dinas terkait",
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
        
        if not kategori_layanan == "":
            return jsonify({'status': 'error', 'error': 'Kategori utama belum dipilih'}), 400
        
        if not jenis_masalah == "":
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
