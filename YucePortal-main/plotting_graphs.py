import matplotlib.pyplot as plt
from datetime import datetime
import numpy as np
import calendar
import pymysql


# Gelen Müşteri ve Gelen Telefon Grafiğini oluşturup kaydeder
def plot_visitor_phonecall_graph():
    now = datetime.now()
    year = now.year
    month = now.month
    num_days = calendar.monthrange(year, month)[1]

    if now.month == 1:
        ay = "Ocak"
    elif now.month == 2:
        ay = "Şubt"
    elif now.month == 3:
        ay = "Mar"
    elif now.month == 4:
        ay = "Nis"
    elif now.month == 5:
        ay = "May"
    elif now.month == 6:
        ay = "Haz"
    elif now.month == 7:
        ay = "Tem"
    elif now.month == 8:
        ay = "Ağus"
    elif now.month == 9:
        ay = "Eyl"
    elif now.month == 10:
        ay = "Ekim"
    elif now.month == 11:
        ay = "Kas"
    elif now.month == 12:
        ay = "Aral"

    conn = pymysql.connect(host='localhost', user='root', db='ya_rpa')
    cursor = conn.cursor()
    query = "Select * from graph_data where Month = '{}' AND Year = '{}'".format(month, year)

    result = cursor.execute(query)

    datas = cursor.fetchall()

    Gelen_Telefon_list = []
    Gelen_Musteri_list = []
    week_list = []
    i = 1
    for data in datas:
        week_list.append(int(data[2]))
        

        Gelen_Telefon_list.append(int(data[5]))
        Gelen_Musteri_list.append(int(data[6]))


    conn.commit()
    cursor.close()
    conn.close()
    x = week_list
    
    y1 = Gelen_Telefon_list
    y2 = Gelen_Musteri_list
    max_y1 = max(y1)
    max_y2 = max(y2)
    if max_y1 > max_y2:
        max_val = max_y1
    else:
        max_val = max_y2

    # Create a figure and axis object
    fig, ax = plt.subplots()
    # Plot the data as two line graphs
    
    ax.plot(x, y1, color='#78FAAE', linewidth=3, label='Gelen Telefon', marker='o', markerfacecolor='#0E3A2F')
    ax.plot(x, y2, color='#FAEB67', linewidth=3, label='Gelen Müşteri', marker='o', markerfacecolor='#F7B046')


    # Add some custom styling to the plot
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.set_xlabel('')
    ax.set_ylabel('Adet')
    ax.set_title('Gelen Müşteri - Gelen Telefon', fontweight='bold')

    ax.legend() # Add legend

    for i in range(len(x)):
        plt.text(x[i], y1[i] + 25, f"{y1[i]}", fontsize=9, weight='bold')
        plt.text(x[i], y2[i]+ 25, f"{y2[i]}", fontsize=9, weight='bold')

    plt.xticks(fontsize=9)
    plt.yticks(fontsize=9)
    plt.xlim(0, 30)

    ticks = []
    for i in range(num_days):
        ticks.append(i + 1)

    labels = []
    for i in range(num_days):
        labels.append(str(i + 1) + '-' + ay)

    plt.xticks(ticks, labels, rotation=60)

    x = 0
    while x <= max_val + 100 :
        ax.axhline(x, color='#0E3A2F', linestyle='--', alpha=0.05)
        x = x + 100
    fig.set_size_inches(12, 5)
    fig.savefig('Gelen_Musteri_Telefon_Graph.png')
    #plt.show()

def plot_visitor_graph():
    now = datetime.now()
    year = now.year
    month = now.month
    num_days = calendar.monthrange(year, month)[1]

    aylaar = ["Ocak", "Şubat", "Mart", "Nisan", "Mayıs", "Haziran", "Temmuz", "Ağustos", "Eylül", "Ekim", "Kasım", "Aralık"]

    if now.month == 1:
        ay = "Ocak"
    elif now.month == 2:
        ay = "Şubt"
    elif now.month == 3:
        ay = "Mar"
    elif now.month == 4:
        ay = "Nis"
    elif now.month == 5:
        ay = "May"
    elif now.month == 6:
        ay = "Haz"
    elif now.month == 7:
        ay = "Tem"
    elif now.month == 8:
        ay = "Ağus"
    elif now.month == 9:
        ay = "Eyl"
    elif now.month == 10:
        ay = "Ekim"
    elif now.month == 11:
        ay = "Kas"
    elif now.month == 12:
        ay = "Aral"

    conn = pymysql.connect(host='localhost', user='root', db='ya_rpa')
    cursor = conn.cursor()

    query = "Select * from graph_data where Month = '{}' AND Year = '{}'".format(month, year)
    result = cursor.execute(query)
    datas = cursor.fetchall()

    Gelen_Musteri_list = []
    week_list = []
    i = 1
    for data in datas:
        week_list.append(int(data[2]))
        Gelen_Musteri_list.append(int(data[6]))
    
    if month == 1:
        line_2nd = 12
        line_2nd_year = year - 1
        query2 = "Select * from graph_data where Month = '{}' AND Year = '{}'".format(12, year - 1)
    else:
        line_2nd = month - 1
        line_2nd_year = year
        query2 = "Select * from graph_data where Month = '{}' AND Year = '{}'".format(month - 1, year)
    result2 = cursor.execute(query2)
    datas2 = cursor.fetchall()
    Gelen_Musteri_list2 = []
    week_list2 = []
    for data in datas2:
        week_list2.append(int(data[2]))
        Gelen_Musteri_list2.append(int(data[6]))


    if month <= 2:
        if month == 2:
            line_3rd = 12
            line_3rd_year = year - 1
            query3 = "Select * from graph_data where Month = '{}' AND Year = '{}'".format(12, year - 1)
        elif month == 1:
            line_3rd = 11
            line_3rd_year = year - 1
            query3 = "Select * from graph_data where Month = '{}' AND Year = '{}'".format(11, year - 1)
    else:
        line_3rd = month - 2
        line_3rd_year = year 
        query3 = "Select * from graph_data where Month = '{}' AND Year = '{}'".format(month - 2, year)
    result3 = cursor.execute(query3)
    datas3 = cursor.fetchall()
    Gelen_Musteri_list3 = []
    week_list3 = []
    for data in datas3:
        week_list3.append(int(data[2]))
        Gelen_Musteri_list3.append(int(data[6]))

    conn.commit()
    cursor.close()
    conn.close()
    x = week_list
    x2 = week_list2
    x3 = week_list3
    
    y1 = Gelen_Musteri_list
    y2 = Gelen_Musteri_list2
    y3 = Gelen_Musteri_list3
    max_y1 = max(y1)
    max_y2 = max(y2)
    max_y3 = max(y3)
    if max_y1 > max_y2:
        max_val = max_y1
    else:
        max_val = max_y2
    if max_y3 > max_val:
        max_val = max_y3
    else:
        max_val = max_val

    # Create a figure and axis object
    fig, ax = plt.subplots()
    # Plot the data as two line graphs
    ax.plot(x, y1, color='#78FAAE', linewidth=3, label='{} {}'.format(aylaar[month - 1], year), marker='o', markerfacecolor='#0E3A2F')
    ax.plot(x2, y2, color='#FAEB67', linewidth=3, label='{} {}'.format(aylaar[line_2nd - 1], line_2nd_year), marker='o', markerfacecolor='#F7B046')
    ax.plot(x3, y3, color='#1ED4DF', linewidth=3, label='{} {}'.format(aylaar[line_3rd - 1], line_3rd_year), marker='o', markerfacecolor='#0961A1')


    # Add some custom styling to the plot
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.set_xlabel('')
    ax.set_ylabel('Adet')
    ax.set_title('Gelen Müşteri', fontweight='bold')

    ax.legend() # Add legend

    for i in range(len(x)):
        plt.text(x[i], y1[i] + 25, f"{y1[i]}", fontsize=5, weight='bold')
    for i in range(len(x2)):
        plt.text(x2[i], y2[i]+ 25, f"{y2[i]}", fontsize=5, weight='bold')
    for i in range(len(x3)):
        plt.text(x3[i], y3[i]+ 25, f"{y3[i]}", fontsize=5, weight='bold')

    plt.xticks(fontsize=9)
    plt.yticks(fontsize=9)
    plt.xlim(0, 30)

    ticks = []
    for i in range(num_days):
        ticks.append(i + 1)

    labels = []
    for i in range(num_days):
        labels.append(str(i + 1) + '-' + ay)

    plt.xticks(ticks, labels, rotation=60)

    x = 0
    while x <= max_val + 100 :
        ax.axhline(x, color='#0E3A2F', linestyle='--', alpha=0.05)
        x = x + 100
    fig.set_size_inches(12, 5)
    fig.savefig('Gelen_Musteri_Graph.png')
    #plt.show()

def plot_phonecall_graph():
    now = datetime.now()
    year = now.year
    month = now.month
    num_days = calendar.monthrange(year, month)[1]

    aylaar = ["Ocak", "Şubat", "Mart", "Nisan", "Mayıs", "Haziran", "Temmuz", "Ağustos", "Eylül", "Ekim", "Kasım", "Aralık"]

    if now.month == 1:
        ay = "Ocak"
    elif now.month == 2:
        ay = "Şubt"
    elif now.month == 3:
        ay = "Mar"
    elif now.month == 4:
        ay = "Nis"
    elif now.month == 5:
        ay = "May"
    elif now.month == 6:
        ay = "Haz"
    elif now.month == 7:
        ay = "Tem"
    elif now.month == 8:
        ay = "Ağus"
    elif now.month == 9:
        ay = "Eyl"
    elif now.month == 10:
        ay = "Ekim"
    elif now.month == 11:
        ay = "Kas"
    elif now.month == 12:
        ay = "Aral"

    conn = pymysql.connect(host='localhost', user='root', db='ya_rpa')
    cursor = conn.cursor()

    query = "Select * from graph_data where Month = '{}' AND Year = '{}'".format(month, year)
    result = cursor.execute(query)
    datas = cursor.fetchall()

    Gelen_Telefon_list = []
    week_list = []
    i = 1
    for data in datas:
        week_list.append(int(data[2]))
        Gelen_Telefon_list.append(int(data[5]))
    
    if month == 1:
        line_2nd = 12
        line_2nd_year = year - 1
        query2 = "Select * from graph_data where Month = '{}' AND Year = '{}'".format(12, year - 1)
    else:
        line_2nd = month - 1
        line_2nd_year = year
        query2 = "Select * from graph_data where Month = '{}' AND Year = '{}'".format(month - 1, year)
    result2 = cursor.execute(query2)
    datas2 = cursor.fetchall()
    Gelen_Telefon_list2 = []
    week_list2 = []
    for data in datas2:
        week_list2.append(int(data[2]))
        Gelen_Telefon_list2.append(int(data[5]))



    if month <= 2:
        if month == 2:
            line_3rd = 12
            line_3rd_year = year - 1
            query3 = "Select * from graph_data where Month = '{}' AND Year = '{}'".format(12, year - 1)
        elif month == 1:
            line_3rd = 11
            line_3rd_year = year - 1
            query3 = "Select * from graph_data where Month = '{}' AND Year = '{}'".format(11, year - 1)
    else:
        line_3rd = month - 2
        line_3rd_year = year 
        query3 = "Select * from graph_data where Month = '{}' AND Year = '{}'".format(month - 2, year)

    result3 = cursor.execute(query3)
    datas3 = cursor.fetchall()
    Gelen_Telefon_list3 = []
    week_list3 = []
    for data in datas3:
        week_list3.append(int(data[2]))
        Gelen_Telefon_list3.append(int(data[5]))

    conn.commit()
    cursor.close()
    conn.close()
    x = week_list
    x2 = week_list2
    x3 = week_list3
    
    y1 = Gelen_Telefon_list
    y2 = Gelen_Telefon_list2
    y3 = Gelen_Telefon_list3
    max_y1 = max(y1)
    max_y2 = max(y2)
    max_y3 = max(y3)
    if max_y1 > max_y2:
        max_val = max_y1
    else:
        max_val = max_y2
    if max_y3 > max_val:
        max_val = max_y3
    else:
        max_val = max_val

    # Create a figure and axis object
    fig, ax = plt.subplots()
    # Plot the data as two line graphs
    ax.plot(x, y1, color='#78FAAE', linewidth=3, label='{} {}'.format(aylaar[month - 1], year), marker='o', markerfacecolor='#0E3A2F')
    ax.plot(x2, y2, color='#FAEB67', linewidth=3, label='{} {}'.format(aylaar[line_2nd - 1], line_2nd_year), marker='o', markerfacecolor='#F7B046')
    ax.plot(x3, y3, color='#1ED4DF', linewidth=3, label='{} {}'.format(aylaar[line_3rd - 1], line_3rd_year), marker='o', markerfacecolor='#0961A1')


    # Add some custom styling to the plot
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.set_xlabel('')
    ax.set_ylabel('Adet')
    ax.set_title('Gelen Telefon', fontweight='bold')

    ax.legend() # Add legend

    for i in range(len(x)):
        plt.text(x[i], y1[i] + 25, f"{y1[i]}", fontsize=5, weight='bold')
    for i in range(len(x2)):
        plt.text(x2[i], y2[i]+ 25, f"{y2[i]}", fontsize=5, weight='bold')
    for i in range(len(x3)):
        plt.text(x3[i], y3[i]+ 25, f"{y3[i]}", fontsize=5, weight='bold')

    plt.xticks(fontsize=9)
    plt.yticks(fontsize=9)
    plt.xlim(0, 30)

    ticks = []
    for i in range(num_days):
        ticks.append(i + 1)

    labels = []
    for i in range(num_days):
        labels.append(str(i + 1) + '-' + ay)

    plt.xticks(ticks, labels, rotation=60)

    x = 0
    while x <= max_val + 100 :
        ax.axhline(x, color='#0E3A2F', linestyle='--', alpha=0.05)
        x = x + 100
    fig.set_size_inches(12, 5)
    fig.savefig('Gelen_Telefon_Graph.png')
    #plt.show()

#Bağlantı Grafiğini oluşturup kaydeder
def plot_Baglanti_graph():
    now = datetime.now()
    year = now.year
    month = now.month
    num_days = calendar.monthrange(year, month)[1]

    if now.month == 1:
        ay = "Ocak"
    elif now.month == 2:
        ay = "Şubt"
    elif now.month == 3:
        ay = "Mar"
    elif now.month == 4:
        ay = "Nis"
    elif now.month == 5:
        ay = "May"
    elif now.month == 6:
        ay = "Haz"
    elif now.month == 7:
        ay = "Tem"
    elif now.month == 8:
        ay = "Ağus"
    elif now.month == 9:
        ay = "Eyl"
    elif now.month == 10:
        ay = "Ekim"
    elif now.month == 11:
        ay = "Kas"
    elif now.month == 12:
        ay = "Aral"

    conn = pymysql.connect(host='localhost', user='root', db='ya_rpa')
    cursor = conn.cursor()
    query = "Select * from graph_data where Month = '{}' AND Year = '{}'".format(month, year)

    result = cursor.execute(query)

    datas = cursor.fetchall()

    Baglanti_list = []
    week_list = []
    i = 1
    for data in datas:
        week_list.append(int(data[2]))
        """
        if int(data[2]) == i:
            week_list.append(i)
            i += 1
        elif int(data[2]) != i:
            i = i + 2
            week_list.append(i)
            i += 1
        """
        
        #print('Month : ' + data[3])
        #print('Year : ' + data[4])
        Baglanti_list.append(int(data[7]))
        #print('P Satis : ' + data[8])
        #print('Euro : ' + data[9])

    conn.commit()
    cursor.close()
    conn.close()

    x = week_list
    y1 = Baglanti_list
    max_val = max(y1)

    # Create a figure and axis object
    fig, ax = plt.subplots()

    # Plot the data as two line graphs
    ax.plot(x, y1, color='#78FAAE', linewidth=3, label='Bağlantı', marker='o', markerfacecolor='#0E3A2F')

    # Add some custom styling to the plot
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.set_xlabel('')
    ax.set_ylabel('Adet')
    ax.set_title('Bağlantı', fontweight='bold')
    ax.legend() # Add legend

    for i in range(len(x)):
        plt.text(x[i], y1[i] + 2, f"{y1[i]}", fontsize=9, weight='bold')

    plt.xticks(fontsize=9)
    plt.yticks(fontsize=9)

    plt.xlim(0, 30)

    ticks = []
    for i in range(num_days):
        ticks.append(i + 1)

    labels = []
    for i in range(num_days):
        labels.append(str(i + 1) + '-' + ay)

    plt.xticks(ticks, labels, rotation=60)

    x = 0
    while x < max_val + 10:
        ax.axhline(x, color='#0E3A2F', linestyle='--', alpha=0.05)
        x = x + 10

    fig.set_size_inches(12, 5)
    fig.savefig('Baglanti_Graph.png')
    #plt.show()

#Perakende Satış Grafiğini oluşturup kaydeder
def plot_Perakende_Satis_graph():
    now = datetime.now()
    year = now.year
    month = now.month
    num_days = calendar.monthrange(year, month)[1]

    aylaar = ["Ocak", "Şubat", "Mart", "Nisan", "Mayıs", "Haziran", "Temmuz", "Ağustos", "Eylül", "Ekim", "Kasım", "Aralık"]

    if now.month == 1:
        ay = "Ocak"
    elif now.month == 2:
        ay = "Şubt"
    elif now.month == 3:
        ay = "Mar"
    elif now.month == 4:
        ay = "Nis"
    elif now.month == 5:
        ay = "May"
    elif now.month == 6:
        ay = "Haz"
    elif now.month == 7:
        ay = "Tem"
    elif now.month == 8:
        ay = "Ağus"
    elif now.month == 9:
        ay = "Eyl"
    elif now.month == 10:
        ay = "Ekim"
    elif now.month == 11:
        ay = "Kas"
    elif now.month == 12:
        ay = "Aral"

    conn = pymysql.connect(host='localhost', user='root', db='ya_rpa')
    cursor = conn.cursor()
    query = "Select * from graph_data where Month = '{}' AND Year = '{}'".format(month, year)
    result = cursor.execute(query)
    datas = cursor.fetchall()

    PerakendeSatis_list = []
    week_list = []
    i = 1
    for data in datas:
        week_list.append(int(data[2]))   
        PerakendeSatis_list.append(int(data[8]))

    if month == 1:
        line_2nd = 12
        line_2nd_year = year - 1
        query2 = "Select * from graph_data where Month = '{}' AND Year = '{}'".format(12, year - 1)
    else:
        line_2nd = month - 1
        line_2nd_year = year
        query2 = "Select * from graph_data where Month = '{}' AND Year = '{}'".format(month - 1, year)
    result2 = cursor.execute(query2)
    datas2 = cursor.fetchall()
    PerakendeSatis_list2 = []
    week_list2 = []
    for data in datas2:
        week_list2.append(int(data[2]))
        PerakendeSatis_list2.append(int(data[8]))

    if month <= 2:
        if month == 2:
            line_3rd = 12
            line_3rd_year = year - 1
            query3 = "Select * from graph_data where Month = '{}' AND Year = '{}'".format(12, year - 1)
        elif month == 1:
            line_3rd = 11
            line_3rd_year = year - 1
            query3 = "Select * from graph_data where Month = '{}' AND Year = '{}'".format(11, year - 1)
    else:
        line_3rd = month - 2
        line_3rd_year = year 
        query3 = "Select * from graph_data where Month = '{}' AND Year = '{}'".format(month - 2, year)
    result3 = cursor.execute(query3)
    datas3 = cursor.fetchall()
    PerakendeSatis_list3 = []
    week_list3 = []
    for data in datas3:
        week_list3.append(int(data[2]))
        PerakendeSatis_list3.append(int(data[8]))

    conn.commit()
    cursor.close()
    conn.close()

    x1 = week_list
    x2 = week_list2
    x3 = week_list3
    y1 = PerakendeSatis_list
    y2 = PerakendeSatis_list2
    y3 = PerakendeSatis_list3
    max_value1 = max(y1)
    max_value2 = max(y2)
    max_value3 = max(y3)
    max_value = max([max_value1, max_value2, max_value3])

    # Create a figure and axis object
    fig, ax = plt.subplots()

    # Plot the data as two line graphs
    ax.plot(x1, y1, color='#78FAAE', linewidth=3, label='Perakende Satış {} {}'.format(aylaar[month - 1], year), marker='o', markerfacecolor='#0E3A2F')
    ax.plot(x2, y2, color='#FAEB67', linewidth=3, label='Perakende Satış {} {}'.format(aylaar[line_2nd - 1], line_2nd_year), marker='o', markerfacecolor='#F7B046')
    ax.plot(x3, y3, color='#1ED4DF', linewidth=3, label='Perakende Satış {} {}'.format(aylaar[line_3rd - 1], line_3rd_year), marker='o', markerfacecolor='#0961A1')

    # Add some custom styling to the plot
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.set_xlabel('')
    ax.set_ylabel('Adet')
    ax.set_title('Perakende Satış', fontweight='bold')
    ax.legend()  # Add legend

    for i in range(len(x1)):
        plt.text(x1[i], y1[i] + 2, f"{y1[i]}", fontsize=9, weight='bold')
    for i in range(len(x2)):
        plt.text(x2[i], y2[i] + 2, f"{y2[i]}", fontsize=9, weight='bold')
    for i in range(len(x3)):
        plt.text(x3[i], y3[i] + 2, f"{y3[i]}", fontsize=9, weight='bold')

    plt.xticks(fontsize=9)
    plt.yticks(fontsize=9)

    plt.xlim(0, 30)

    ticks = []
    for i in range(num_days):
        ticks.append(i + 1)

    labels = []
    for i in range(num_days):
        labels.append(str(i + 1) + '-' + ay)

    plt.xticks(ticks, labels, rotation=60)

    x = 0
    while x <= max_value + 20:
        ax.axhline(x, color='#0E3A2F', linestyle='--', alpha=0.05)
        x = x + 20

    fig.set_size_inches(12, 5)
    fig.savefig('Perakende_Satis_Graph.png')
    #plt.show()

#Euro/TL Kur Grafiğini oluşturup kaydeder
def plot_Kur_graph():
    now = datetime.now()
    year = now.year
    month = now.month
    num_days = calendar.monthrange(year, month)[1]

    if now.month == 1:
        ay = "Ocak"
    elif now.month == 2:
        ay = "Şubt"
    elif now.month == 3:
        ay = "Mar"
    elif now.month == 4:
        ay = "Nis"
    elif now.month == 5:
        ay = "May"
    elif now.month == 6:
        ay = "Haz"
    elif now.month == 7:
        ay = "Tem"
    elif now.month == 8:
        ay = "Ağus"
    elif now.month == 9:
        ay = "Eyl"
    elif now.month == 10:
        ay = "Ekim"
    elif now.month == 11:
        ay = "Kas"
    elif now.month == 12:
        ay = "Aral"

    conn = pymysql.connect(host='localhost', user='root', db='ya_rpa')
    cursor = conn.cursor()
    query = "Select * from graph_data where Month = '{}' AND Year = '{}'".format(month, year)

    result = cursor.execute(query)

    datas = cursor.fetchall()

    EuroKur_list = []
    week_list = []
    i = 1
    for data in datas:
        week_list.append(int(data[2]))
        """
        if int(data[2]) == i:
            week_list.append(i)
            i += 1
        elif int(data[2]) != i:
            i = i + 2
            week_list.append(i)
            i += 1
        """

        EuroKur_list.append(float(data[9]))

    conn.commit()
    cursor.close()
    conn.close()

    x = week_list
    y1 = EuroKur_list
    max_val = max(y1)
    min_val = min(y1)

    # Create a figure and axis object
    fig, ax = plt.subplots()

    # Plot the data as two line graphs
    ax.plot(x, y1, color='#78FAAE', linewidth=3, label='€/₺', marker='o', markerfacecolor='#0E3A2F')

    # Add some custom styling to the plot
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.set_xlabel('')
    ax.set_ylabel('TL')
    ax.set_title('Kur €/₺', fontweight='bold')
    ax.legend()  # Add legend

    for i in range(len(x)):
        plt.text(x[i], y1[i] + 0.02, f"{y1[i]}", fontsize=9, weight='bold')

    plt.xticks(fontsize=9)
    plt.yticks(fontsize=9)

    plt.xlim(0, 30)

    ticks = []
    for i in range(num_days):
        ticks.append(i + 1)

    labels = []
    for i in range(num_days):
        labels.append(str(i + 1) + '-' + ay)

    plt.xticks(ticks, labels, rotation=60)

    x = round(min_val)
    while x < max_val + 0.2:
        ax.axhline(x, color='#0E3A2F', linestyle='--', alpha=0.05)
        x = x + 0.2

    fig.set_size_inches(12, 5)
    fig.savefig('Kur_Graph.png')
    #plt.show()

# 2.0 Motorlu araçların aylık bar grafiğini oluşturup kaydeder
def plot_2_0_veh_sales_graph():
    now = datetime.now()
    year = now.year
    month = now.month

    conn = pymysql.connect(host='localhost', user='root', db='ya_rpa')
    cursor = conn.cursor()
    query = "SELECT * FROM sales_2_0_veh WHERE Year = {}".format(year)

    result = cursor.execute(query)

    datas = cursor.fetchall()
    amount_of_months = len(datas)
    values = []
    for data in datas:
        values.append(data[3])
        values.append(data[4])

    groups = ["Ocak x", "Şubat x", "Mart x", "Nisan x", "Mayıs x", "Haziran x", "Temmuz x", "Ağustos x", "Eylül x", "Ekim x", "Kasım x", "Aralık x"]
    for i in range(len(groups)):
        groups[i] = groups[i].replace("x", str(year))
    groups = groups[:month]

    from matplotlib.lines import Line2D

    group_space=0.4
    bar_width=1.0
    y_label = "Adet"
    x_label = "Ay - Yıl"
    title = "2.0 Motorlu Araç Satış Adetleri"

    fig, ax = plt.subplots()

    num_groups = len(groups)
    group_size = len(values) // num_groups
    num_columns = 2  # Two columns per group

    odd_color = "#78FAAE"  # Color for odd-numbered columns
    even_color = "#0E3A2F"  # Color for even-numbered columns

    legend_labels = ['Perakende', 'Filo']  # Legend labels
    legend_colors = ['#0E3A2F', '#78FAAE']  # Legend colors

    # Create groups of bars with specified spacing, alternating colors, and bar width
    for i in range(num_groups):
        group_values = values[i * group_size:(i + 1) * group_size]
        group_x = np.arange(len(group_values)) + i * (group_size * num_columns + group_space)

        # Alternate colors based on column index
        for j, (x, y) in enumerate(zip(group_x, group_values)):
            color = even_color if j % 2 == 0 else odd_color
            ax.bar(x, y, color=color, width=bar_width)  # Adjust the width here

            # Annotate each bar with its value (adjust the y value for spacing)
            ax.text(x, y + 0.5, str(y), ha='center', va='bottom', weight='bold')

    # Set chart title and labels
    ax.set_title(title, fontweight='bold')
    ax.set_xlabel(x_label)
    ax.set_ylabel(y_label)

    # Remove the top, left, and right spines
    ax.spines['top'].set_visible(False)
    ax.spines['left'].set_visible(False)
    ax.spines['right'].set_visible(False)

    # Calculate the positions for group ticks and set labels between the bars of each group
    offset = 0.1  # Adjust this value to move labels left or right
    group_ticks = np.arange(group_size * 0.5 - offset, num_groups * (group_size * num_columns + group_space) - offset,
                            group_size * num_columns + group_space)
    ax.set_xticks(group_ticks)
    ax.set_xticklabels([f'{group}' for group in groups])

    # Rotate x-axis labels for better readability
    plt.xticks(rotation=30)

    # Add a legend with custom entries
    legend_entries = [Line2D([0], [0], color=color, lw=4, label=label) for label, color in
                      zip(legend_labels, legend_colors)]

    ax.legend(handles=legend_entries)

    max_value = max(values)  # Find the maximum value in the data
    for y_value in range(0, max_value + 1, 10):
        ax.axhline(y_value, color='#0E3A2F', linestyle='--', alpha=0.05)

    fig.set_size_inches(12, 6)
    fig.savefig('Sales_2_0_Veh.png')
    #plt.show()
