from jinja2 import Template

satis_email_html = """
<html>
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Alış ve Satış Hedefleri</title>
</head>
<body style="font-family: Arial, sans-serif;">

    <p>{},</p>

    <p>Birlikte mutabık kaldığımız {} ayı “Alış ve Satış Hedefleri”niz aşağıdaki gibidir;</p>

    <ul>
        <li><strong>SATIŞ HEDEFİ:</strong> {}</li>
        <li><strong>ALIŞ HEDEFİ:</strong> {}</li>
    </ul>

    <p><strong>Not:</strong> Satış hedefi aynı zamanda {} ayı “Satış Ekipleri Prim” hedefidir.</p>

    <p>Hedefler, filo araçları dışında kalan perakende araçları kapsamaktadır.</p>

    <p><strong><span style="color: red; font-size: 20px;">{}</span></strong></p>

</body>
</html>
"""


