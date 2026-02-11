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


def calculate_weighting(jumlah_warga, durasi, jenis_masalah):
    """
    Hitung poin pembobotan berdasarkan:
    - Jumlah warga terdampak (max 1 poin)
    - Durasi gangguan (max 1 poin)
    - Jenis masalah severity (max 1 poin)
    Total: 0-3 poin
    """
    
    poin = 0.0
    
    # Poin dari jumlah warga terdampak (0-1)
    try:
        jumlah = int(jumlah_warga) if jumlah_warga else 0
        if jumlah > 0:
            if jumlah < 50:
                poin += 0.2
            elif jumlah < 100:
                poin += 0.4
            elif jumlah < 500:
                poin += 0.6
            elif jumlah < 1000:
                poin += 0.8
            else:
                poin += 1.0
    except:
        pass
    
    # Poin dari durasi gangguan (0-1)
    try:
        durasi_jam = int(durasi) if durasi else 0
        if durasi_jam > 0:
            # Skala: < 2 jam = 0.2, 2-6 jam = 0.4, 6-12 jam = 0.6, 12-24 jam = 0.8, > 24 jam = 1.0
            if durasi_jam < 2:
                poin += 0.2 
            elif durasi_jam < 6:
                poin += 0.4
            elif durasi_jam < 12:
                poin += 0.6
            elif durasi_jam < 24:
                poin += 0.8
            else:
                poin += 1.0
    except:
        pass
    
    # Poin dari jenis masalah (severity baseline) (0-1)
    # Beberapa jenis masalah memiliki severity lebih tinggi
    high_severity_keywords = [
        'rusak', 'danger', 'emergency', 'darurat', 'ilegal', 'parah',
        'terkelupas', 'keselamatan', 'kritis', 'tidak-layak'
    ]
    
    jenis_lower = jenis_masalah.lower() if jenis_masalah else ""
    if any(keyword in jenis_lower for keyword in high_severity_keywords):
        poin += 1.0
    else:
        poin += 0.3
    
    # Normalize jika perlu (capped at 3)
    poin = min(poin, 3.0)
    
    return round(poin, 2)


def determine_severity(poin):
    if poin <= 1:
        return "ringan"
    elif poin <= 2:
        return "sedang"
    else:
        return "berat"


def get_tips_for_category_severity(category, severity):
    if not issues_data:
        return []
    
    tips_section = issues_data.get('tips', {}).get(category, {})
    
    if severity == "berat":
        # Untuk berat, gabungkan tips berat + tips darurat
        tips = tips_section.get('berat', []) + tips_section.get('darurat', [])
    else:
        tips = tips_section.get(severity, [])
    
    return tips


def get_specific_issue_tips(category, issue_type):
    if not issues_data:
        return None
    
    tips_spesifik = issues_data.get('tipsSpesifik', {}).get(category, {})
    
    # Normalize issue_type key (sudah dalam format dengan dash)
    tip = tips_spesifik.get(issue_type)
    
    return tip


@app.route('/submit', methods=['POST'])
def submit():
    try:
        # Ambil data dari form
        kategori_layanan = request.form.get('mainCategory', '').strip()
        jenis_masalah = request.form.get('issueType', '').strip()
        jumlah_warga_terdampak = request.form.get('jumlah_warga_terdampak', '').strip()
        durasi_terdampak = request.form.get('durasi_gangguan', '').strip()
        
        # Validasi minimal
        if not kategori_layanan:
            return jsonify({
                'status': 'error',
                'error': 'Kategori utama belum dipilih'
            }), 400
        
        # Rule 1: Hitung pembobotan (modus ponens)
        poin_pembobotan = calculate_weighting(jumlah_warga_terdampak, durasi_terdampak, jenis_masalah)
        
        # Rule 2: Tentukan tingkat keparahan berdasarkan poin (modus ponens)
        tingkat_keparahan = determine_severity(poin_pembobotan)
        
        # Rule 3: Ambil tips umum untuk kategori & tingkat keparahan (modus ponens)
        tips_umum = get_tips_for_category_severity(kategori_layanan, tingkat_keparahan)
        
        # Rule 4: Cek apakah ada tips spesifik untuk jenis masalah (modus ponens)
        tips_spesifik_text = None
        if jenis_masalah and jenis_masalah != 'lainnya':
            tips_spesifik_text = get_specific_issue_tips(kategori_layanan, jenis_masalah)
        
        # Build response
        response_data = {
            'status': 'success',
            'poin_pembobotan': poin_pembobotan,
            'tingkat_keparahan': tingkat_keparahan,
            'kategori_layanan': kategori_layanan,
            'jenis_masalah': jenis_masalah,
            'jumlah_warga_terdampak': jumlah_warga_terdampak if jumlah_warga_terdampak else '-',
            'durasi_gangguan_jam': durasi_terdampak if durasi_terdampak else '-',
            'tips_umum': tips_umum,
            'tips_spesifik': tips_spesifik_text,
            'analisis': {
                'rule_poin_pembobotan': f"Poin = {poin_pembobotan} (max 3)",
                'rule_severity': f"{tingkat_keparahan.upper()}" if tingkat_keparahan == "ringan" else (
                    "SEDANG" if tingkat_keparahan == "sedang" else "BERAT ⚠️"
                ),
                'rule_applied': f"IF kategori={kategori_layanan} AND tingkat_keparahan={tingkat_keparahan} THEN output_tips"
            }
        }
        
        return jsonify(response_data), 200
    
    except Exception as e:
        return jsonify({
            'status': 'error',
            'error': f'Server error: {str(e)}'
        }), 500


if __name__ == "__main__":
    app.run(debug=True, port=5000)
