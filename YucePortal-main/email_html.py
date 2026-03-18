email_html = """<html>
  <head></head>
  <body>
    <p>Değerli Yöneticilerimiz ve Çalışma Arkadaşlarımız,
    <br>
    <br>
    <b>{}</b> tarihli sabah raporunu bilgilerinize sunarız.
    <br>
    <table>
      <tr>
        <td colspan="1"></td>
        <th colspan="2" style="border: 1px solid black; background-color:#F1F2F2">Satış Adetleri</th>
      </tr>
      <tr>
        <th></th>
        <th style="border: 1px solid black;">AY</th>
        <th style="border: 1px solid black;">YIL</th>
      </tr>
      <tr>
        <td style="border: 1px solid black;"><b>PERAKENDE</b></td>
        <td style="border: 1px solid black; text-align:center;">&nbsp;{}&nbsp;</td>
        <td style="border: 1px solid black; text-align:center;">&nbsp;{}&nbsp;</td>
      </tr>
      <tr>
        <td style="border: 1px solid black;"><b>TOPTAN</b></td>
        <td style="border: 1px solid black; text-align:center;">&nbsp;{}&nbsp;</td>
        <td style="border: 1px solid black; text-align:center;">&nbsp;{}&nbsp;</td>
      </tr>
    </table>
    <p style="color:red"><b>FİLO/PERAKENDE DETAYLI ADETLER AŞAĞIDAKİ GİBİDİR:</b><p>
    <b>Aylık Perakende: {} ({}F + {}P)</b>
    <br>
    <b>Aylık Toptan: {} ({}F + {}P)</b>
    <br>
    <p style="color:red"><b>Fatura + Bağlantı: {} (filo hariç)</b></p>
    <br>
    İthalat: {} ({}P + {}F) 
    <br>
    Toptan Fatura: {} ({}P + {}F)
    <br>
    {}
    <br>
    <hr style="width:90%;">
    <br>
    <table>
        <tr>
            <td style="border: none" colspan="2"></td>
            <td style="border: 1px solid black; text-align:center; background-color:#0E3A2F; color:#78FAAE" colspan="3"><b>Perakende</b></td>
            <td style="border: 1px solid black; text-align:center; background-color:#78FAAE;" colspan="3"><b>Filo</b></td>
            <td style="border: 1px solid black; text-align:center; background-color:#F7B046;" colspan="3"><b>Toplam</b></td>
        </tr>
        <tr>
            <td style="border: 1px solid black; text-align:center; height:90px; width:120px; background-color:#CACECF" colspan="2"><b>STATÜ</b></td>
            <td style="border: 1px solid black; text-align:center; width:90px; background-color:#0E3A2F; color:#78FAAE"; text-align:center><b>ADET</b></td>
            <td style="border: 1px solid black; text-align:center; width:90px; background-color:#0E3A2F; color:#78FAAE"><b>MÜŞTERİ İSİMLİ ARAÇ SAYISI</b></td>
            <td style="border: 1px solid black; text-align:center; width:90px; background-color:#0E3A2F; color:#78FAAE"><b>MÜŞTERİ ORANI</b></td>
            <td style="border: 1px solid black; text-align:center; width:90px; background-color:#78FAAE;"><b>ADET</b></td>
            <td style="border: 1px solid black; text-align:center; width:90px; background-color:#78FAAE;"><b>MÜŞTERİ İSİMLİ ARAÇ SAYISI</b></td>
            <td style="border: 1px solid black; text-align:center; width:90px; background-color:#78FAAE;"><b>MÜŞTERİ ORANI</b></td>
            <td style="border: 1px solid black; text-align:center; width:90px; background-color:#F7B046;"><b>ADET</b></td>
            <td style="border: 1px solid black; text-align:center; width:90px; background-color:#F7B046;"><b>MÜŞTERİ İSİMLİ ARAÇ SAYISI</b></td>
            <td style="border: 1px solid black; text-align:center; width:90px; background-color:#F7B046;"><b>MÜŞTERİ ORANI</b></td>
        </tr>
        <tr>
            <td style="border: 1px solid black; text-align:center; background-color:#CACECF; opacity: 0.92;" colspan="2">YS STOK</td>
            <td style="border: 1px solid black; text-align:center; background-color:#0E3A2F; opacity: 0.92; color:#78FAAE">{}</td>
            <td style="border: 1px solid black; text-align:center; background-color:#0E3A2F; opacity: 0.92; color:#78FAAE">{}</td>
            <td style="border: 1px solid black; text-align:center; background-color:#0E3A2F; opacity: 0.92; color:#78FAAE">{}</td>
            <td style="border: 1px solid black; text-align:center; background-color:#78FAAE; opacity: 0.92;">{}</td>
            <td style="border: 1px solid black; text-align:center; background-color:#78FAAE; opacity: 0.92;">{}</td>
            <td style="border: 1px solid black; text-align:center; background-color:#78FAAE; opacity: 0.92;">{}</td>
            <td style="border: 1px solid black; text-align:center; background-color:#F7B046; opacity: 0.92;">{}</td>
            <td style="border: 1px solid black; text-align:center; background-color:#F7B046; opacity: 0.92;">{}</td>
            <td style="border: 1px solid black; text-align:center; background-color:#F7B046; opacity: 0.92;">{}</td>
        </tr>
        <tr>
            <td style="border: 1px solid black; text-align:center; background-color:#CACECF" colspan="2">DS STOK</td>
            <td style="border: 1px solid black; text-align:center; background-color:#0E3A2F; color:#78FAAE">{}</td>
            <td style="border: 1px solid black; text-align:center; background-color:#0E3A2F; color:#78FAAE">{}</td>
            <td style="border: 1px solid black; text-align:center; background-color:#0E3A2F; color:#78FAAE">{}</td>
            <td style="border: 1px solid black; text-align:center; background-color:#78FAAE;">{}</td>
            <td style="border: 1px solid black; text-align:center; background-color:#78FAAE;">{}</td>
            <td style="border: 1px solid black; text-align:center; background-color:#78FAAE;">{}</td>
            <td style="border: 1px solid black; text-align:center; background-color:#F7B046">{}</td>
            <td style="border: 1px solid black; text-align:center; background-color:#F7B046">{}</td>
            <td style="border: 1px solid black; text-align:center; background-color:#F7B046">{}</td>
        </tr>
        <tr>
            <td style="border: 1px solid black; text-align:center; background-color:#CACECF; opacity: 0.92;" colspan="2">FİKTİF</td>
            <td style="border: 1px solid black; text-align:center; background-color:#0E3A2F; color:#78FAAE; opacity: 0.92;">{}</td>
            <td style="border: 1px solid black; text-align:center; background-color:#0E3A2F; color:#78FAAE; opacity: 0.92;">{}</td>
            <td style="border: 1px solid black; text-align:center; background-color:#0E3A2F; color:#78FAAE; opacity: 0.92;">{}</td>
            <td style="border: 1px solid black; text-align:center; background-color:#78FAAE; opacity: 0.92;">{}</td>
            <td style="border: 1px solid black; text-align:center; background-color:#78FAAE; opacity: 0.92;">{}</td>
            <td style="border: 1px solid black; text-align:center; background-color:#78FAAE; opacity: 0.92;">{}</td>
            <td style="border: 1px solid black; text-align:center; background-color:#F7B046; opacity: 0.92;">{}</td>
            <td style="border: 1px solid black; text-align:center; background-color:#F7B046; opacity: 0.92;">{}</td>
            <td style="border: 1px solid black; text-align:center; background-color:#F7B046; opacity: 0.92;">{}</td>
        </tr>
        <tr>
            <td style="border: 1px solid black; text-align:center; background-color:#CACECF" colspan="2">YOLDA</td>
            <td style="border: 1px solid black; text-align:center; background-color:#0E3A2F; color:#78FAAE">{}</td>
            <td style="border: 1px solid black; text-align:center; background-color:#0E3A2F; color:#78FAAE">{}</td>
            <td style="border: 1px solid black; text-align:center; background-color:#0E3A2F; color:#78FAAE">{}</td>
            <td style="border: 1px solid black; text-align:center; background-color:#78FAAE;">{}</td>
            <td style="border: 1px solid black; text-align:center; background-color:#78FAAE;">{}</td>
            <td style="border: 1px solid black; text-align:center; background-color:#78FAAE;">{}</td>
            <td style="border: 1px solid black; text-align:center; background-color:#F7B046">{}</td>
            <td style="border: 1px solid black; text-align:center; background-color:#F7B046">{}</td>
            <td style="border: 1px solid black; text-align:center; background-color:#F7B046">{}</td>
        </tr>
        <tr>
            <td style="border: 1px solid black; text-align:center; background-color:#CACECF; opacity: 0.92;" colspan="2">LİMAN</td>
            <td style="border: 1px solid black; text-align:center; background-color:#0E3A2F; color:#78FAAE; opacity: 0.92;">{}</td>
            <td style="border: 1px solid black; text-align:center; background-color:#0E3A2F; color:#78FAAE; opacity: 0.92;">{}</td>
            <td style="border: 1px solid black; text-align:center; background-color:#0E3A2F; color:#78FAAE; opacity: 0.92;">{}</td>
            <td style="border: 1px solid black; text-align:center; background-color:#78FAAE; opacity: 0.92;">{}</td>
            <td style="border: 1px solid black; text-align:center; background-color:#78FAAE; opacity: 0.92;">{}</td>
            <td style="border: 1px solid black; text-align:center; background-color:#78FAAE; opacity: 0.92;">{}</td>
            <td style="border: 1px solid black; text-align:center; background-color:#F7B046; opacity: 0.92;">{}</td>
            <td style="border: 1px solid black; text-align:center; background-color:#F7B046; opacity: 0.92;">{}</td>
            <td style="border: 1px solid black; text-align:center; background-color:#F7B046; opacity: 0.92;">{}</td>
        </tr>
        <tr>
            <td style="border: 1px solid black; text-align:center; background-color:#CACECF" colspan="2">&nbsp;PRODUCED & INT&nbsp;</td>
            <td style="border: 1px solid black; text-align:center; background-color:#0E3A2F; color:#78FAAE">{}</td>
            <td style="border: 1px solid black; text-align:center; background-color:#0E3A2F; color:#78FAAE">{}</td>
            <td style="border: 1px solid black; text-align:center; background-color:#0E3A2F; color:#78FAAE">{}</td>
            <td style="border: 1px solid black; text-align:center; background-color:#78FAAE;">{}</td>
            <td style="border: 1px solid black; text-align:center; background-color:#78FAAE;">{}</td>
            <td style="border: 1px solid black; text-align:center; background-color:#78FAAE;">{}</td>
            <td style="border: 1px solid black; text-align:center; background-color:#F7B046">{}</td>
            <td style="border: 1px solid black; text-align:center; background-color:#F7B046">{}</td>
            <td style="border: 1px solid black; text-align:center; background-color:#F7B046">{}</td>
        </tr>
    </table>
    <br>
    <hr style="width:90%;">
    <br>
    <table>
        <tr>
            <td style="border: 1px solid black; text-align:center; border: none" colspan="11"><b>YS STOK ÜST MODEL BAZLI MÜŞTERİLİ ARAÇ ORANI</b></td>
        </tr>
        <tr>
            <td style="border: none" colspan="2"></td>
            <td style="border: 1px solid black; text-align:center; background-color:#0E3A2F; color:#78FAAE" colspan="3"><b>Perakende</b></td>
            <td style="border: 1px solid black; text-align:center; background-color:#78FAAE;" colspan="3"><b>Filo</b></td>
            <td style="border: 1px solid black; text-align:center; background-color:#F7B046;" colspan="3"><b>Toplam</b></td>
        </tr>
        <tr>
            <td style="border: 1px solid black; text-align:center; height:90px; width:120px; background-color:#CACECF" colspan="2"><b>ÜST MODEL</b></td>
            <td style="border: 1px solid black; text-align:center; width:90px; background-color:#0E3A2F; color:#78FAAE"; text-align:center><b>ADET</b></td>
            <td style="border: 1px solid black; text-align:center; width:90px; background-color:#0E3A2F; color:#78FAAE"><b>MÜŞTERİ İSİMLİ ARAÇ SAYISI</b></td>
            <td style="border: 1px solid black; text-align:center; width:90px; background-color:#0E3A2F; color:#78FAAE"><b>MÜŞTERİ ORANI</b></td>
            <td style="border: 1px solid black; text-align:center; width:90px; background-color:#78FAAE;"><b>ADET</b></td>
            <td style="border: 1px solid black; text-align:center; width:90px; background-color:#78FAAE;"><b>MÜŞTERİ İSİMLİ ARAÇ SAYISI</b></td>
            <td style="border: 1px solid black; text-align:center; width:90px; background-color:#78FAAE;"><b>MÜŞTERİ ORANI</b></td>
            <td style="border: 1px solid black; text-align:center; width:90px; background-color:#F7B046;"><b>ADET</b></td>
            <td style="border: 1px solid black; text-align:center; width:90px; background-color:#F7B046;"><b>MÜŞTERİ İSİMLİ ARAÇ SAYISI</b></td>
            <td style="border: 1px solid black; text-align:center; width:90px; background-color:#F7B046;"><b>MÜŞTERİ ORANI</b></td>
        </tr>
        <tr>
            <td style="border: 1px solid black; text-align:center; background-color:#CACECF; opacity: 0.92;" colspan="2">FABIA</td>
            <td style="border: 1px solid black; text-align:center; background-color:#0E3A2F; opacity: 0.92; color:#78FAAE">{}</td>
            <td style="border: 1px solid black; text-align:center; background-color:#0E3A2F; opacity: 0.92; color:#78FAAE">{}</td>
            <td style="border: 1px solid black; text-align:center; background-color:#0E3A2F; opacity: 0.92; color:#78FAAE">{}</td>
            <td style="border: 1px solid black; text-align:center; background-color:#78FAAE; opacity: 0.92;">{}</td>
            <td style="border: 1px solid black; text-align:center; background-color:#78FAAE; opacity: 0.92;">{}</td>
            <td style="border: 1px solid black; text-align:center; background-color:#78FAAE; opacity: 0.92;">{}</td>
            <td style="border: 1px solid black; text-align:center; background-color:#F7B046; opacity: 0.92;">{}</td>
            <td style="border: 1px solid black; text-align:center; background-color:#F7B046; opacity: 0.92;">{}</td>
            <td style="border: 1px solid black; text-align:center; background-color:#F7B046; opacity: 0.92;">{}</td>
        </tr>
        <tr>
            <td style="border: 1px solid black; text-align:center; background-color:#CACECF" colspan="2">SCALA</td>
            <td style="border: 1px solid black; text-align:center; background-color:#0E3A2F; color:#78FAAE">{}</td>
            <td style="border: 1px solid black; text-align:center; background-color:#0E3A2F; color:#78FAAE">{}</td>
            <td style="border: 1px solid black; text-align:center; background-color:#0E3A2F; color:#78FAAE">{}</td>
            <td style="border: 1px solid black; text-align:center; background-color:#78FAAE;">{}</td>
            <td style="border: 1px solid black; text-align:center; background-color:#78FAAE;">{}</td>
            <td style="border: 1px solid black; text-align:center; background-color:#78FAAE;">{}</td>
            <td style="border: 1px solid black; text-align:center; background-color:#F7B046">{}</td>
            <td style="border: 1px solid black; text-align:center; background-color:#F7B046">{}</td>
            <td style="border: 1px solid black; text-align:center; background-color:#F7B046">{}</td>
        </tr>
        <tr>
            <td style="border: 1px solid black; text-align:center; background-color:#CACECF; opacity: 0.92;" colspan="2">OCTAVIA</td>
            <td style="border: 1px solid black; text-align:center; background-color:#0E3A2F; color:#78FAAE; opacity: 0.92;">{}</td>
            <td style="border: 1px solid black; text-align:center; background-color:#0E3A2F; color:#78FAAE; opacity: 0.92;">{}</td>
            <td style="border: 1px solid black; text-align:center; background-color:#0E3A2F; color:#78FAAE; opacity: 0.92;">{}</td>
            <td style="border: 1px solid black; text-align:center; background-color:#78FAAE; opacity: 0.92;">{}</td>
            <td style="border: 1px solid black; text-align:center; background-color:#78FAAE; opacity: 0.92;">{}</td>
            <td style="border: 1px solid black; text-align:center; background-color:#78FAAE; opacity: 0.92;">{}</td>
            <td style="border: 1px solid black; text-align:center; background-color:#F7B046; opacity: 0.92;">{}</td>
            <td style="border: 1px solid black; text-align:center; background-color:#F7B046; opacity: 0.92;">{}</td>
            <td style="border: 1px solid black; text-align:center; background-color:#F7B046; opacity: 0.92;">{}</td>
        </tr>
        <tr>
            <td style="border: 1px solid black; text-align:center; background-color:#CACECF; opacity: 0.92;" colspan="2">YENİ SUPERB</td>
            <td style="border: 1px solid black; text-align:center; background-color:#0E3A2F; color:#78FAAE; opacity: 0.92;">{}</td>
            <td style="border: 1px solid black; text-align:center; background-color:#0E3A2F; color:#78FAAE; opacity: 0.92;">{}</td>
            <td style="border: 1px solid black; text-align:center; background-color:#0E3A2F; color:#78FAAE; opacity: 0.92;">{}</td>
            <td style="border: 1px solid black; text-align:center; background-color:#78FAAE; opacity: 0.92;">{}</td>
            <td style="border: 1px solid black; text-align:center; background-color:#78FAAE; opacity: 0.92;">{}</td>
            <td style="border: 1px solid black; text-align:center; background-color:#78FAAE; opacity: 0.92;">{}</td>
            <td style="border: 1px solid black; text-align:center; background-color:#F7B046; opacity: 0.92;">{}</td>
            <td style="border: 1px solid black; text-align:center; background-color:#F7B046; opacity: 0.92;">{}</td>
            <td style="border: 1px solid black; text-align:center; background-color:#F7B046; opacity: 0.92;">{}</td>
        </tr>
        <tr>
            <td style="border: 1px solid black; text-align:center; background-color:#CACECF" colspan="2">KAMIQ</td>
            <td style="border: 1px solid black; text-align:center; background-color:#0E3A2F; color:#78FAAE">{}</td>
            <td style="border: 1px solid black; text-align:center; background-color:#0E3A2F; color:#78FAAE">{}</td>
            <td style="border: 1px solid black; text-align:center; background-color:#0E3A2F; color:#78FAAE">{}</td>
            <td style="border: 1px solid black; text-align:center; background-color:#78FAAE;">{}</td>
            <td style="border: 1px solid black; text-align:center; background-color:#78FAAE;">{}</td>
            <td style="border: 1px solid black; text-align:center; background-color:#78FAAE;">{}</td>
            <td style="border: 1px solid black; text-align:center; background-color:#F7B046">{}</td>
            <td style="border: 1px solid black; text-align:center; background-color:#F7B046">{}</td>
            <td style="border: 1px solid black; text-align:center; background-color:#F7B046">{}</td>
        </tr>
        <tr>
            <td style="border: 1px solid black; text-align:center; background-color:#CACECF" colspan="2">KAROQ</td>
            <td style="border: 1px solid black; text-align:center; background-color:#0E3A2F; color:#78FAAE">{}</td>
            <td style="border: 1px solid black; text-align:center; background-color:#0E3A2F; color:#78FAAE">{}</td>
            <td style="border: 1px solid black; text-align:center; background-color:#0E3A2F; color:#78FAAE">{}</td>
            <td style="border: 1px solid black; text-align:center; background-color:#78FAAE;">{}</td>
            <td style="border: 1px solid black; text-align:center; background-color:#78FAAE;">{}</td>
            <td style="border: 1px solid black; text-align:center; background-color:#78FAAE;">{}</td>
            <td style="border: 1px solid black; text-align:center; background-color:#F7B046">{}</td>
            <td style="border: 1px solid black; text-align:center; background-color:#F7B046">{}</td>
            <td style="border: 1px solid black; text-align:center; background-color:#F7B046">{}</td>
        </tr>
        <tr>
            <td style="border: 1px solid black; text-align:center; background-color:#CACECF" colspan="2">YENİ KODIAQ</td>
            <td style="border: 1px solid black; text-align:center; background-color:#0E3A2F; color:#78FAAE">{}</td>
            <td style="border: 1px solid black; text-align:center; background-color:#0E3A2F; color:#78FAAE">{}</td>
            <td style="border: 1px solid black; text-align:center; background-color:#0E3A2F; color:#78FAAE">{}</td>
            <td style="border: 1px solid black; text-align:center; background-color:#78FAAE;">{}</td>
            <td style="border: 1px solid black; text-align:center; background-color:#78FAAE;">{}</td>
            <td style="border: 1px solid black; text-align:center; background-color:#78FAAE;">{}</td>
            <td style="border: 1px solid black; text-align:center; background-color:#F7B046">{}</td>
            <td style="border: 1px solid black; text-align:center; background-color:#F7B046">{}</td>
            <td style="border: 1px solid black; text-align:center; background-color:#F7B046">{}</td>
        </tr>
        <tr>
            <td style="border: 1px solid black; text-align:center; background-color:#E3E5E6;" colspan="2">TOPLAM</td>
            <td style="border: 1px solid black; text-align:center; background-color:#E3E5E6;">{}</td>
            <td style="border: 1px solid black; text-align:center; background-color:#E3E5E6;">{}</td>
            <td style="border: 1px solid black; text-align:center; background-color:#E3E5E6;">{}</td>
            <td style="border: 1px solid black; text-align:center; background-color:#E3E5E6;">{}</td>
            <td style="border: 1px solid black; text-align:center; background-color:#E3E5E6;">{}</td>
            <td style="border: 1px solid black; text-align:center; background-color:#E3E5E6;">{}</td>
            <td style="border: 1px solid black; text-align:center; background-color:#E3E5E6;">{}</td>
            <td style="border: 1px solid black; text-align:center; background-color:#E3E5E6;">{}</td>
            <td style="border: 1px solid black; text-align:center; background-color:#E3E5E6;">{}</td>
        </tr>
    </table>
    <br>
    <h4><b>Saygılarımızla,</b></h4>
    <p>Kurumsal bilgiler içermektedir. Sadece ilgili ekipler ve 3. taraflar ile kontrollü olarak paylaşılmalıdır. \\ Contains corporate information. It should only be shared in a controlled manner with the relevant teams and third parties.</p>
  </body>
</html>"""