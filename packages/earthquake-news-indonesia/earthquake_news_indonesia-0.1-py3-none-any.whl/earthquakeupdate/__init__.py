import requests
from bs4 import BeautifulSoup


def ekstraksi_data():
    """
    tanggal: 26 April 2022
    Magnitudo: 4.8
    Kedalaman: 25 km
    Lokasi: LS=7.48  BT=106.68
    Titik Gempa: Pusat gempa berada di laut 56 km tenggarakab. Sukabumi
    Dampak Gempak Dirasakan (Skala MMI): II - III Sukabumi, II - III Cianjur selatan, II Garut, II Pangandaran
    :return:
    """
    try:
        content = requests.get('https://bmkg.go.id')
    except Exception:
        return None

    if content.status_code == 200:
        soup = BeautifulSoup(content.text, 'html.parser')

        time = soup.find('span', {'class': 'waktu'})
        time = time.text.split(', ')
        waktu = time[1]
        tanggal = time[0]

        result = soup.find('div', {'class': 'col-md-6 col-xs-6 gempabumi-detail no-padding'})
        result = result.findChildren('li')
        i = 0
        magnitudo = None
        kedalaman = None
        ls = None
        bt = None
        lokasi = None
        dirasakan = None

        for res in result:
            print(i, res)
            if i == 1:
                magnitudo = res.text
            elif i == 2:
                kedalaman = res.text
            elif i == 3:
                koordinat = res.text.split(' - ')
                ls = koordinat[0]
                bt = koordinat[1]
            elif i == 4:
                lokasi = res.text
            elif i == 5:
                dirasakan = res.text
            i = i + 1

        # waktu = time.text.split(', ')[1]
        # tanggal = time.text.split(', ')[0]
        # print(title.string)

        result = dict()
        result['tanggal'] = tanggal
        result['waktu'] = waktu
        result['magnitudo'] = magnitudo
        result['kedalaman'] = kedalaman
        result['koordinat'] = {'ls': ls, 'bt': bt}
        result['lokasi'] = lokasi
        result['dirasakan'] = dirasakan
        return result
    else:
        return None


def tampilkan_data(result):
    if result is None:
        print("Tidak dapat menemukan data terkini")
        return

    print('\nGempa Terakhir berdasarkan BMKG')
    print(f"Tanggal: {result['tanggal']}")
    print(f"Waktu: {result['waktu']}")
    print(f"Magnitudo: {result['magnitudo']}")
    print(f"Kedalaman: {result['kedalaman']}")
    print(f"koordinat LS adalah {result['koordinat']['ls']} dan BT={result['koordinat']['bt']}")
    print(f"Lokasi Gempa {result['lokasi']}")
    print(f"gempa {result['dirasakan']}")

if __name__ == '__main__':
    print('aplikasi utama')
    result = ekstraksi_data()
    tampilkan_data(result)
