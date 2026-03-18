email_html = """<html>
  <head></head>
  <body>
    <p>Değerli Yöneticilerimiz ve Çalışma Arkadaşlarımız,
    <br>
    <br>
    <p>Günlük SSH Raporunu bilgilerinize sunarız.</p>
    <p>İyi Çalışmalar</p>
    <p><b>{} {}</b></p>
    <table>
        <tr>
            <th>&nbsp;&nbsp;&nbsp;&nbsp;Gerçekleşen İş Günü Sayısı&nbsp;&nbsp;&nbsp;&nbsp;</th>
            <th>Kalan İş Günü Sayısı</th>
        </tr>
        <tr>
            <td style="text-align:center; border:1px;"><b>{}</b></td>
            <td style="text-align:center; border:1px;"><b>{}</b></td>
        </tr>
    </table>
    <br>
    <div class="container" style="width:100%;">
          <hr style="border-style: solid; width:90%;">
            <table>
                <tr>
                    <th colspan="1" style="background-color:#F1F2F2; width:320px">Günlük SSH Raporu</th>
                    <th colspan="1" style="background-color:#F1F2F2; width:120px">Gün</th>
                    <th colspan="1" style="background-color:#F1F2F2; width:120px">Aylık Kümüle</th>
                    <th colspan="1" style="background-color:#F1F2F2; width:120px">Aylık Hedef</th>
                    <th colspan="1" style="background-color:#F1F2F2; width:120px">Yıllık Kümüle</th>
                    <th colspan="1" style="background-color:#F1F2F2; width:120px">{}/{}</th>
                </tr>
                <tr>
                    <td style="text-align:center; border: 1px solid #F1F2F2;"><b>Servis Girişi</b></td>
                    <td style="text-align:center; border: 1px solid #F1F2F2;">{}</td>
                    <td style="text-align:center; border: 1px solid #F1F2F2;">{}</td>
                    <td style="text-align:center; border: 1px solid #F1F2F2;">{}</td>
                    <td style="text-align:center; border: 1px solid #F1F2F2;">{}</td>
                    <td style="text-align:center; border: 1px solid #F1F2F2;">{}</td>
                </tr>
                <tr>
                    <td style="text-align:center; border: 1px solid #F1F2F2;"><b>Randevulu Servis Girişi (Oran)</b></td>
                    <td style="text-align:center; border: 1px solid #F1F2F2;">{}&nbsp;({})</td>
                    <td style="text-align:center; border: 1px solid #F1F2F2;">{}&nbsp;({})</td>
                    <td style="text-align:center; border: 1px solid #F1F2F2;">-</td>
                    <td style="text-align:center; border: 1px solid #F1F2F2;">{}&nbsp;({})</td>
                    <td style="text-align:center; border: 1px solid #F1F2F2;">{}</td>
                </tr>
                <tr>
                    <td style="text-align:center; border: 1px solid #F1F2F2;"><b>Müşteri Şikayet Adedi</b></td>
                    <td style="text-align:center; border: 1px solid #F1F2F2;">{}</td>
                    <td style="text-align:center; border: 1px solid #F1F2F2;">{}</td>
                    <td style="text-align:center; border: 1px solid #F1F2F2;">-</td>
                    <td style="text-align:center; border: 1px solid #F1F2F2;">{}</td>
                    <td style="text-align:center; border: 1px solid #F1F2F2;">{}</td>
                </tr>
                <tr>
                    <td>&nbsp;</td>
                    <td">&nbsp;</td>
                    <td>&nbsp;</td>
                    <td>&nbsp;</td>
                </tr>
                <tr>
                    <td style="text-align:center; border: 1px solid #F1F2F2;">İş Emri</td>
                    <td style="text-align:center; border: 1px solid #F1F2F2;">{}</td>
                    <td style="text-align:center; border: 1px solid #F1F2F2;">{}</td>
                    <td style="text-align:center; border: 1px solid #F1F2F2;">-</td>
                    <td style="text-align:center; border: 1px solid #F1F2F2;">{}</td>
                    <td style="text-align:center; border: 1px solid #F1F2F2;">{}</td>
                </tr>
                <tr>
                    <td style="text-align:center; border: 1px solid #F1F2F2;">Garanti</td>
                    <td style="text-align:center; border: 1px solid #F1F2F2;">{}</td>
                    <td style="text-align:center; border: 1px solid #F1F2F2;">{}</td>
                    <td style="text-align:center; border: 1px solid #F1F2F2;">-</td>
                    <td style="text-align:center; border: 1px solid #F1F2F2;">{}</td>
                    <td style="text-align:center; border: 1px solid #F1F2F2;">{}</td>
                </tr>
                <tr>
                    <td style="text-align:center; border: 1px solid #F1F2F2;">Banko</td>
                    <td style="text-align:center; border: 1px solid #F1F2F2;">{}</td>
                    <td style="text-align:center; border: 1px solid #F1F2F2;">{}</td>
                    <td style="text-align:center; border: 1px solid #F1F2F2;">-</td>
                    <td style="text-align:center; border: 1px solid #F1F2F2;">{}</td>
                    <td style="text-align:center; border: 1px solid #F1F2F2;">{}</td>
                </tr>
                <tr>
                    <td style="text-align:center; border: 1px solid #F1F2F2;"><b>Toplam Parça Satışı</b></td>
                    <td style="text-align:center; border: 1px solid #F1F2F2;">{}</td>
                    <td style="text-align:center; border: 1px solid #F1F2F2;">{}</td>
                    <td style="text-align:center; border: 1px solid #F1F2F2;">{}</td>
                    <td style="text-align:center; border: 1px solid #F1F2F2;">{}</td>
                    <td style="text-align:center; border: 1px solid #F1F2F2;">{}</td>
                </tr>
                <tr>
                    <td>&nbsp;</td>
                    <td">&nbsp;</td>
                    <td>&nbsp;</td>
                    <td>&nbsp;</td>
                </tr>
                <tr>
                    <td style="text-align:center; border: 1px solid #F1F2F2;"><b>Aksesuar Satışı</b></td>
                    <td style="text-align:center; border: 1px solid #F1F2F2;">{}</td>
                    <td style="text-align:center; border: 1px solid #F1F2F2;">{}</td>
                    <td style="text-align:center; border: 1px solid #F1F2F2;">{}</td>
                    <td style="text-align:center; border: 1px solid #F1F2F2;">{}</td>
                    <td style="text-align:center; border: 1px solid #F1F2F2;">{}</td>
                </tr>
                <tr>
                    <td>&nbsp;</td>
                    <td">&nbsp;</td>
                    <td>&nbsp;</td>
                    <td>&nbsp;</td>
                </tr>
                <tr>
                    <td style="text-align:center; border: 1px solid #F1F2F2;"><b>YS Parça Stok</b></td>
                    <td style="text-align:center; border: 1px solid #F1F2F2;">{}</td>
                    <td></td>
                    <td></td>
                    <td></td>
                    <td></td>
                </tr>
                <tr>
                    <td style="text-align:center; border: 1px solid #F1F2F2;"><b>YS Aksesuar Stok</b></td>
                    <td style="text-align:center; border: 1px solid #F1F2F2;">{}</td>
                    <td></td>
                    <td></td>
                    <td></td>
                    <td></td>
                </tr>
            </table>
            <br>
            <img src="data:image/png;base64,{}" style="width:200px !important; height:200px !important;">
            <img src="data:image/png;base64,{}" style="width:200px !important; height:200px !important;">
            <img src="data:image/png;base64,{}" style="width:200px !important; height:200px !important;">
            <br>
            <img src="data:image/png;base64,{}">
            <br>
            <img src="data:image/png;base64,{}">
            <br>
            <img src="data:image/png;base64,{}">
    </div>
    <div class="container" style="width:100%; display:flex;">
        <br>
        <p>Kurumsal bilgiler içermektedir. Sadece ilgili ekipler ve 3. taraflar ile kontrollü olarak paylaşılmalıdır. \\ Contains corporate information. It should only be shared in a controlled manner with the relevant teams and third parties.</p>
    </div>
  </body>
</html>"""
