from flask import Flask, render_template, request
import re

app = Flask(__name__)

def baca_kata_dari_file(nama_file):
    semua_kata = []
    with open(nama_file, 'r', encoding='utf-8') as file:
        for baris in file:
            kata_dari_baris = re.findall(r'\b\w+\b', baris.lower())
            semua_kata.extend(kata_dari_baris)
    return semua_kata

def cari_kata(kata_list, jenis, pola):
    hasil = []
    pola = pola.lower()
    for kata in kata_list:
        kata = kata.lower()
        if jenis == 'prefix' and kata.startswith(pola):
            hasil.append(kata)
        elif jenis == 'suffix' and kata.endswith(pola):
            hasil.append(kata)
        elif jenis == 'infix' and pola in kata:
            hasil.append(kata)
    return sorted(set(hasil), key=len)  # Urutkan dari yang paling pendek

@app.route('/', methods=['GET', 'POST'])
def index():
    hasil = []
    jenis = ''
    pola = ''
    if request.method == 'POST':
        jenis = request.form.get('jenis')
        pola = request.form.get('pola', '').strip().lower()

        daftar_kata = baca_kata_dari_file('dataset.txt')
        hasil = cari_kata(daftar_kata, jenis, pola)

    return render_template('index.html', hasil=hasil, jenis=jenis, pola=pola)

if __name__ == '__main__':
    app.run()
