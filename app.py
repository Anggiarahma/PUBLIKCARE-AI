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
    
    tips_dict = issues_data.get('tips', {}).get(kategori_layanan, {})
    tips_darurat_dict = issues_data.get('tips_darurat', {}).get(kategori_layanan, {})
    
    # ============================================
    # LISTRIK - Pemadaman listrik
    # ============================================
    if kategori_layanan == "listrik" and jenis_masalah == "pemadaman-listrik" and not darurat:
        tips_list = tips_dict.get(jenis_masalah)

    elif kategori_layanan == "listrik" and jenis_masalah == "pemadaman-listrik" and darurat:
        tips_list = tips_darurat_dict.get(jenis_masalah)
    
    # ============================================
    # LISTRIK - Kabel listrik di jalan mengganggu
    # ============================================
    elif kategori_layanan == "listrik" and jenis_masalah == "kabel-listrik-di-jalan-mengganggu" and not darurat:
        tips_list = tips_dict.get(jenis_masalah)

    elif kategori_layanan == "listrik" and jenis_masalah == "kabel-listrik-di-jalan-mengganggu" and darurat:
        tips_list = tips_darurat_dict.get(jenis_masalah)
        
    # ============================================
    # LISTRIK - Kebakaran akibat listrik
    # ============================================
    elif kategori_layanan == "listrik" and jenis_masalah == "kebakaran-akibat-listrik":
        tips_list = tips_darurat_dict.get(jenis_masalah)
    
    # ============================================
    # AIR - Air tidak mengalir
    # ============================================
    elif kategori_layanan == "air" and jenis_masalah == "air-tidak-mengalir" and not darurat:
        tips_list = tips_dict.get(jenis_masalah)
        
    elif kategori_layanan == "air" and jenis_masalah == "air-tidak-mengalir" and darurat:
        tips_list = tips_darurat_dict.get(jenis_masalah)
    
    # ============================================
    # AIR - Kualitas air buruk
    # ============================================
    elif kategori_layanan == "air" and jenis_masalah == "kualitas-air-buruk" and not darurat:
        tips_list = tips_dict.get(jenis_masalah)

    elif kategori_layanan == "air" and jenis_masalah == "kualitas-air-buruk" and darurat:
        tips_list = tips_darurat_dict.get(jenis_masalah)
           
    # ============================================
    # AIR - Kebocoran pipa distribusi
    # ============================================
    elif kategori_layanan == "air" and jenis_masalah == "kebocoran-pipa-distribusi" and not darurat:
        tips_list = tips_dict.get(jenis_masalah)
 
    elif kategori_layanan == "air" and jenis_masalah == "kebocoran-pipa-distribusi" and darurat:
        tips_list = tips_darurat_dict.get(jenis_masalah)    
    
    # ============================================
    # SAMPAH - Sampah menumpuk tidak diangkut
    # ============================================
    elif kategori_layanan == "sampah" and jenis_masalah == "sampah-menumpuk-tidak-diangkut" and not darurat:
        tips_list = tips_dict.get(jenis_masalah)

    elif kategori_layanan == "sampah" and jenis_masalah == "sampah-menumpuk-tidak-diangkut" and darurat:
        tips_list = tips_darurat_dict.get(jenis_masalah)
    
    # ============================================
    # SAMPAH - Sungai tersumbat sampah
    # ============================================
    elif kategori_layanan == "sampah" and jenis_masalah == "sungai-tersumbat-sampah" and not darurat:
        tips_list = tips_dict.get(jenis_masalah)

    elif kategori_layanan == "sampah" and jenis_masalah == "sungai-tersumbat-sampah" and darurat:
        tips_list = tips_darurat_dict.get(jenis_masalah)
    
    # ============================================
    # SAMPAH - Sampah B3 dibuang sembarangan
    # ============================================
    elif kategori_layanan == "sampah" and jenis_masalah == "sampah-b3-dibuang-sembarangan" and not darurat:
        tips_list = tips_dict.get(jenis_masalah)

    elif kategori_layanan == "sampah" and jenis_masalah == "sampah-b3-dibuang-sembarangan" and darurat:
        tips_list = tips_darurat_dict.get(jenis_masalah)
    
    return tips_list


@app.route('/submit', methods=['POST'])
def submit():
    try:
        kategori_layanan = request.form.get('mainCategory', '').strip()
        jenis_masalah = request.form.get('issueType', '')
        darurat = request.form.get('status_darurat', 'off') == 'on'
        
        if not kategori_layanan:
            return jsonify({'status': 'error', 'error': 'Kategori utama belum dipilih'}), 400
        
        if not jenis_masalah:
            return jsonify({'status': 'error', 'error': 'Jenis masalah belum dipilih'}), 400
        
        tips_output = get_tips_for_condition(kategori_layanan, jenis_masalah, darurat)
        
        response_data = {
            'status': 'success',
            'kategori_layanan': kategori_layanan,
            'jenis_masalah': jenis_masalah,
            'status_darurat': 'DARURAT' if (darurat or jenis_masalah == "kebakaran-akibat-listrik") else 'Non-Darurat',
            'tips': tips_output
        }
        
        return jsonify(response_data), 200
    
    except Exception as e:
        return jsonify({'status': 'error', 'error': f'Server error: {str(e)}'}), 500


if __name__ == "__main__":
    app.run(debug=True, port=5000)
