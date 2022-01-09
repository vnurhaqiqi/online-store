# online-store

## Deskripsi Masalah

Penyebab utama kenapa review jelek setelah event 12.12 terjadi adalah karena pelanggan sudah melakukan pembayaran akan
tetapi barang tersebut sudah tidak ada stoknya. Lalu, pelanggan mendapat informasi dari customer service bahwa, pesanan
yang sebelumnya dibatalkan karena ketidak tersediaanya dari quantity barang. Pada sistem yang sedang berjalan tidak
adanya pengecekan stock dari barang yang dipasarkan. Sehingga saat berlangsung event besar seperti flash sale 12.12
ketika stock barang sudah kosong pelanggan dapat terus melakukan order.

## Propose Solution

Untuk mencegah kejadian ini terjadi kembali, dibutuhkan pengecekan stock barang ketika customer hendak melakukan
checkout. Serta pengecekan secara berkala untuk stock barang yang tersedia, sehingga department order processing dapat
mengetahui update terakhir dari stock barang tersebut. Khususnya ketika mendekati event flash sale atau ketika event
tersebut sedang berjalan.

## How to run

### Clone Project

    git clone https://github.com/vnurhaqiqi/online-store.git

### Buat Virtual ENV

Harap untuk menginstall python terlebih dahulu. Lalu selanjutnya menginstall virtual environment untuk menjalankan
program.

#### Install virtualenv

    python3 -m venv env

Selanjutnya run virtualenv yang telah dibuat sebelumnya.

#### Run Linux/MacOS

    source <folder_path>/bin/activate

#### Run Windows

    <folder_path>\Scripts\activate

### Install Requirements

Selanjutnya adalah install semua dependencies yang berkaitan dengan app.

    pip install -r requirements.txt

### Setup .ENV file

Tambahkan file .env dengan contoh dibawah ini;

    FLASK_APP=app.py
    FLASK_ENV=development
    DATABASE_URI=<DATABASE_URI>

### Run Flask Server

#### Migrate Database

Buat file migration terlebih dahulu jika memang belum ada dengan menggunakan command dibawah ini;

    flask db migrate

Selanjutnya adalah migration ke database dengan menggunakan command ini;

    flask db upgrade

#### Run Server

Terakhir adalah menjalan server dengan menggunakan command ini;

    flask run

## List of Endpoints

<table>
<thead>
<tr>
  <th>No.</th>
  <th>Description</th>
  <th>Endpoint</th>
  <th>Method</th>
</tr>
</thead>
<tbody>
  <tr>
    <td>1</td>
    <td>Get seluruh data produk</td>
    <td>/api/v1/products</td>
    <td>GET</td>
  </tr>
<tr>
    <td>2</td>
    <td>Menambahkan data produk</td>
    <td>/api/v1/products</td>
    <td>POST</td>
  </tr>
  <tr>
    <td>3</td>
    <td>Membuat data order</td>
    <td>/api/v1/create-order</td>
    <td>POST</td>
  </tr>
  <tr>
    <td>4</td>
    <td>Get data order dengan menggunakan order id</td>
    <td>/api/v1/order/[order_id]</td>
    <td>GET</td>
  </tr>
<tr>
    <td>5</td>
    <td>Proses melakukan checkout order</td>
    <td>/api/v1/checkout-order</td>
    <td>POST</td>
  </tr>
<tr>
    <td>6</td>
    <td>Membuat data payment berdasarkan data order</td>
    <td>/api/v1/payment-order</td>
    <td>POST</td>
  </tr>
<tr>
    <td>7</td>
    <td>Mengkonfirmasi payment order</td>
    <td>/api/v1/confirm-payment-order/[payment_id]</td>
    <td>PUT</td>
  </tr>
<tr>
    <td>8</td>
    <td>Reject payment order</td>
    <td>/api/v1/reject-payment-order/[payment_id]</td>
    <td>PUT</td>
  </tr>
<tr>
    <td>9</td>
    <td>Get data payment beserta detail order</td>
    <td>/api/v1/payment-order/[payment_id]</td>
    <td>GET</td>
  </tr>
<tr>
    <td>10</td>
    <td>Pengecekan stok tersedia pada produk dan menginformasikan berapa kuantiti yang harus ditambahkan</td>
    <td>/api/v1/check-product-quantity</td>
    <td>GET</td>
  </tr>
</tbody>
</table>

### Note

- Untuk request body untuk method POST dapat dilihat di collection yang dilampirkan juga pada repo ini.
- DDL Script untuk database juga dilampirkan di repo ini.