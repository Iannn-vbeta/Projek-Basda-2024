import pandas as pd

def create_universitas(db, nama_universitas):
    query = "INSERT INTO universitas (nama_universitas) VALUES (%s) RETURNING id_universitas"
    db.execute(query, (nama_universitas,))
    return db.fetch_one()[0]

def create_fakultas(db, nama_fakultas):
    query = "INSERT INTO fakultas (nama_fakultas) VALUES (%s) RETURNING id_fakultas"
    db.execute(query, (nama_fakultas,))
    return db.fetch_one()[0]

def create_role(db, nama_role):
    query = "INSERT INTO role (nama_role) VALUES (%s) RETURNING id_role"
    db.execute(query, (nama_role,))
    return db.fetch_one()[0]

def check_universitas_exists(self, nama_universitas):
    query = "SELECT id_universitas FROM universitas WHERE nama_universitas ILIKE %s"
    self.execute(query, ('%' + nama_universitas + '%',))
    return self.fetch_one()[0]

def check_fakultas_exists(self, nama_fakultas):
    query = "SELECT id_fakultas FROM fakultas WHERE nama_fakultas ILIKE %s"
    self.execute(query, ('%' + nama_fakultas + '%',))
    return self.fetch_one()[0]

def check_role_exists(self, nama_role):
    query = "SELECT id_role FROM role WHERE nama_role ILIKE %s"
    self.execute(query, ('%' + nama_role + '%',))
    return self.fetch_one()[0]

def create_or_get_universitas(db, nama_universitas):
    existing = db.check_universitas_exists(nama_universitas)
    if existing:
        return existing[0]
    return create_universitas(db, nama_universitas)

def create_or_get_fakultas(db, nama_fakultas):
    existing = db.check_fakultas_exists(nama_fakultas)
    if existing:
        return existing[0]
    return create_fakultas(db, nama_fakultas)

def create_or_get_role(db, nama_role):
    existing = db.check_role_exists(nama_role)
    if existing:
        return existing[0]
    return create_role(db, nama_role)

def create_alamat(db, jalan, kota, kode_pos, provinsi):
    query = "INSERT INTO alamat (jalan, kota, kode_pos, provinsi) VALUES (%s, %s, %s, %s) RETURNING id_alamat"
    db.execute(query, (jalan, kota, kode_pos, provinsi))
    return db.fetch_one()[0]

def create_user(db, id_user, nama_user, no_telepon, id_alamat, durasi_huni, id_universitas, id_fakultas, id_role, no_kamar):
    query = """
    INSERT INTO users (id_user, nama_user, no_telepon, id_alamat, durasi_huni, id_universitas, id_fakultas, id_role, no_kamar) 
    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s) RETURNING id_user
    """
    db.execute(query, (id_user, nama_user, no_telepon, id_alamat, durasi_huni, id_universitas, id_fakultas, id_role, no_kamar))
    return db.fetch_one()[0]

def register_user(db):
    try:        
        user_details = {
            'id_user': int(input("Masukkan ID Pengguna: ")),
            'nama_user': input("Masukkan Nama Pengguna: "),
            'no_telepon': input("Masukkan Nomor Telepon: "),
            'jalan': input("Masukkan Jalan: "),
            'kota': input("Masukkan Kota: "),
            'kode_pos': int(input("Masukkan Kode Pos: ")),
            'provinsi': input("Masukkan Provinsi: "),
            'durasi_huni': input("Masukkan Durasi Huni (YYYY-MM-DD): "),
            'nama_universitas': input("Masukkan Nama Universitas: "),
            'nama_fakultas': input("Masukkan Nama Fakultas: "),
            'nama_role': input("Masukkan Peran: "),
            'no_kamar': int(input("Masukkan Nomor Kamar: "))
        }
    
        try:
            # Begin transaction
            db.connection.autocommit = False

            # Create alamat
            id_alamat = create_alamat(db, user_details['jalan'], user_details['kota'], user_details['kode_pos'], user_details['provinsi'])
            
            # Create or get universitas
            id_universitas = create_or_get_universitas(db, user_details['nama_universitas'])
            
            # Create or get fakultas
            id_fakultas = create_or_get_fakultas(db, user_details['nama_fakultas'])
            
            # Create or get role
            id_role = create_or_get_role(db, user_details['nama_role'])
            
            # Create user
            id_user = create_user(db, user_details['id_user'], user_details['nama_user'], user_details['no_telepon'], id_alamat, 
                                  user_details['durasi_huni'], id_universitas, id_fakultas, id_role, user_details['no_kamar'])
            # Commit transaction
            db.connection.commit()
            print("Registrasi Berhasil:")
            print("ID Pengguna:", id_user)
            print("Nama Pengguna:", user_details['nama_user'])
            print("Nomor Telepon:", user_details['no_telepon'])
            print("Alamat:", user_details['jalan'] + ", " + user_details['kota'] + ", " + user_details['provinsi'] + ", " + str(user_details['kode_pos']))
            print("Durasi Huni:", user_details['durasi_huni'])
            print("Universitas:", user_details['nama_universitas'])
            print("Fakultas:", user_details['nama_fakultas'])
            print("Peran:", user_details['nama_role'])
            print("Nomor Kamar:", user_details['no_kamar'])
            return id_user

        except Exception as e:
            # Rollback transaction on error
            db.connection.rollback() 
            db.close()
            print("Registrasi Gagal:", e)
            return None
        
    except:
        print("Input tidak valid.")        

def view_all_users(db):
    try:
        # Ambil ID pengguna, nama pengguna, dan nomor kamar
        query = """
        SELECT u.id_user, u.nama_user, u.no_kamar
        FROM users u
        WHERE u.id_role = 1
        """
        db.execute(query)
        users_data = db.fetch_data()

        # Membuat DataFrame dari hasil query
        columns = ['ID Pengguna', 'Nama Pengguna', 'Nomor Kamar']
        users_df = pd.DataFrame(users_data, columns=columns)

        # Mengubah nilai yang kosong menjadi 0 dan mengonversi kolom Nomor Kamar menjadi integer
        users_df['Nomor Kamar'] = users_df['Nomor Kamar'].fillna(0).astype(int)

        # Tampilkan daftar semua penghuni beserta indeks
        print("Daftar Semua Penghuni:")
        print(users_df)

        # Biarkan pengguna memilih indeks dari DataFrame
        selected_index = int(input("\nPilih indeks pengguna untuk melihat detailnya: "))

        # Periksa apakah indeks yang dipilih valid
        if selected_index < 0 or selected_index >= len(users_df):
            print("Indeks tidak valid.")
            return

        # Dapatkan ID pengguna berdasarkan indeks yang dipilih
        selected_user_id = users_df.loc[selected_index, 'ID Pengguna']

        # Ambil detail pengguna yang dipilih dengan menggabungkan tabel
        selected_user_query = """
        SELECT u.id_user, u.nama_user, u.no_telepon, a.jalan, a.kota, a.kode_pos, a.provinsi,
               u.durasi_huni, un.nama_universitas, f.nama_fakultas, r.nama_role, u.no_kamar
        FROM users u
        JOIN alamat a ON u.id_alamat = a.id_alamat
        LEFT JOIN universitas un ON u.id_universitas = un.id_universitas
        LEFT JOIN fakultas f ON u.id_fakultas = f.id_fakultas
        LEFT JOIN role r ON u.id_role = r.id_role
        WHERE u.id_user = %s and u.id_role=1
        """
        db.execute(selected_user_query, (int(selected_user_id),))
        selected_user_data = db.fetch_data()

        if not selected_user_data:
            print("Pengguna dengan ID", selected_user_id, "tidak ditemukan.")
            return

        # Menambahkan kolom untuk detail pengguna
        detail_columns = ['ID Pengguna', 'Nama Pengguna', 'Nomor Telepon', 'Jalan', 'Kota', 'Kode Pos', 'Provinsi',
                          'Durasi Huni', 'Universitas', 'Fakultas', 'Peran', 'Nomor Kamar']

        # Membuat DataFrame untuk detail pengguna yang dipilih
        selected_user_df = pd.DataFrame(selected_user_data, columns=detail_columns)

        # Mengubah nilai yang kosong menjadi 0 dan mengonversi kolom Nomor Kamar menjadi integer
        selected_user_df['Nomor Kamar'] = selected_user_df['Nomor Kamar'].fillna(0).astype(int)

        # Tampilkan detail pengguna yang dipilih
        print("\nDetail Pengguna yang Dipilih:")
        for index, row in selected_user_df.iterrows():
            print("{:<15}: {}".format("Nama", row['Nama Pengguna']))
            print("{:<15}: {}".format("Nomor Kamar", row['Nomor Kamar']))
            print("{:<15}: {}".format("Fakultas", row['Fakultas']))
            print("{:<15}: {}".format("Universitas", row['Universitas']))
            print("{:<15}: {}".format("Provinsi", row['Provinsi']))
            print("{:<15}: {}".format("Durasi Huni", row['Durasi Huni']))
            print("{:<15}: {}".format("Nomor Telepon", row['Nomor Telepon']))
            print("{:<15}: {}".format("Jalan", row['Jalan']))
            print("{:<15}: {}".format("Kota", row['Kota']))
            print("{:<15}: {}".format("Kode Pos", row['Kode Pos']))
            print()
    except Exception as e:
        print("Error:", e)

