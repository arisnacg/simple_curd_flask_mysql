from flask import Flask, render_template, request, redirect, url_for
from database import Database
from sys import argv

app = Flask(__name__)

db = Database(argv[2], argv[3], argv[4], argv[5], argv[6])
db.connect()

def init_table():
    query = ''' CREATE TABLE IF NOT EXISTS `tb_kegiatan` (
    `kegiatan_id` INT(11) NOT NULL AUTO_INCREMENT,
    `nama` VARCHAR(100) DEFAULT NULL,
    `status` TINYINT(1) DEFAULT NULL,
    PRIMARY KEY (`kegiatan_id`)
    )'''
    db.execute(query)

@app.route('/')
def index():
    query = 'SELECT kegiatan_id, nama, status FROM tb_kegiatan ORDER BY kegiatan_id'
    daftar_kegiatan = db.select(query)
    return render_template('base.html', jumlah_kegiatan=len(daftar_kegiatan), daftar_kegiatan=daftar_kegiatan)

@app.route("/tambah", methods=["POST"])
def add_todo():
    nama = request.form.get("nama")
    query = 'INSERT INTO tb_kegiatan(nama, status) VALUES("%s", 0)' % (nama.capitalize())
    db.insert(query)
    return redirect(url_for('index'))

@app.route("/centang/<int:kegiatan_id>")
def update_todo(kegiatan_id):
    query = 'UPDATE tb_kegiatan SET status = 1 WHERE kegiatan_id = %d' % (kegiatan_id)
    db.update(query)
    return redirect(url_for('index'))

@app.route("/hapus/<int:kegiatan_id>")
def delete(kegiatan_id):
    query = 'DELETE FROM tb_kegiatan WHERE kegiatan_id = %d' %(kegiatan_id)
    db.delete(query)
    return redirect(url_for('index'))

if __name__ == '__main__':
    init_table()
    app.run(host="0.0.0.0", port=argv[1], debug=True)