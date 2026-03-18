import matplotlib.pyplot as plt
from PIL import Image
import numpy as np
import calendar
from datetime import datetime
import pymysql
from format_with_period import format_with_period
import matplotlib.patches as mpatches
from ssh_sabahraporu.ssh_ora import ssh_aksesuar_isemri_fromOraDB, ssh_aksesuar_banko_fromOraDB


def resize_image(png_path, target_size):
    # Open the image file
    image = Image.open(png_path)

    # Preserve aspect ratio and calculate the new size
    width, height = image.size
    if width > height:
        new_width = target_size
        new_height = int(height / width * target_size)
    else:
        new_height = target_size
        new_width = int(width / height * target_size)

    # Resize the image
    resized_image = image.resize((new_width, new_height))

    # Save the resized image
    resized_image.save(png_path)

def plot_columnu_(isemri_kumule, isemri_gecensene, parca_kumule, parca_gecensene, aksesuar_kumule, aksesuar_gecensene, png_name, year, lastyear):
    x = np.array([1, 2, 3, 4, 5, 6, 7, 8])
    y = np.array([isemri_kumule, isemri_gecensene, parca_kumule, parca_gecensene, aksesuar_kumule, aksesuar_gecensene])

    # Gruplar ve sütunlar
    groups = [lastyear, '', '']
    columns = ['Sütun 1', 'Sütun 2']

    # Grafiği çizme
    fig, ax = plt.subplots()
    k = 0
    for i in range(len(groups)):
        start_index = i * 2
        end_index = start_index + 2
        ax.bar(x[start_index:end_index] + i * len(columns), y[start_index:end_index], label=groups[i], width=0.8,
               color=['#0E3A2F', '#78FAAE'])
        # Write values on top of the bars
        for j, value in enumerate(y[start_index:end_index]):
            if k == 0:
                pass
            elif k == 1:
                if isemri_kumule >= isemri_gecensene:
                    isemri_scale = 22
                else:
                    isemri_scale = -22
                ax.text(x[start_index + j] + i * len(columns), value + isemri_kumule/30, "%" + str(round(100 * ((isemri_gecensene - isemri_kumule) / isemri_kumule))), ha='center', fontsize=10)
                ax.annotate('', xy=(x[start_index+j]+i*len(columns), value+0.01), xytext=(x[start_index+j]+i*len(columns), value+0.3),
                arrowprops=dict(facecolor='#0E3A2F', arrowstyle='simple', lw=1.5, mutation_scale=isemri_scale))
            elif k == 2:
                pass
            elif k == 3:
                if parca_kumule >= parca_gecensene:
                    garanti_scale = 22
                else:
                    garanti_scale = -22
                ax.text(x[start_index + j] + i * len(columns), value + isemri_kumule/30, "%" + str(round(100 * ((parca_gecensene - parca_kumule) / parca_kumule))), ha='center', fontsize=10)
                ax.annotate('', xy=(x[start_index+j]+i*len(columns), value+0.01), xytext=(x[start_index+j]+i*len(columns), value+0.3),
                arrowprops=dict(facecolor='#0E3A2F', arrowstyle='simple', lw=1.5, mutation_scale=garanti_scale))
            elif k == 4:
                pass
            elif k == 5:
                if aksesuar_kumule >= aksesuar_gecensene:
                    banko_scale = 22
                else:
                    banko_scale = -22
                if aksesuar_kumule!=0:
                    ax.text(x[start_index + j] + i * len(columns), value + isemri_kumule/30, "%" + str(round(100 * ((aksesuar_gecensene - aksesuar_kumule) / aksesuar_kumule))), ha='center', fontsize=10)
                    ax.annotate('', xy=(x[start_index+j]+i*len(columns), value+0.01), xytext=(x[start_index+j]+i*len(columns), value+0.3),
                    arrowprops=dict(facecolor='#0E3A2F', arrowstyle='simple', lw=1.5, mutation_scale=banko_scale))
                else:
                    aksesuar_kumule=1
                    ax.text(x[start_index + j] + i * len(columns), value + isemri_kumule/30, "%" + str(round(100 * ((aksesuar_gecensene - aksesuar_kumule) / aksesuar_kumule))), ha='center', fontsize=10)
                    ax.annotate('', xy=(x[start_index+j]+i*len(columns), value+0.01), xytext=(x[start_index+j]+i*len(columns), value+0.3),
                    arrowprops=dict(facecolor='#0E3A2F', arrowstyle='simple', lw=1.5, mutation_scale=banko_scale))
            elif k == 6:
                pass
            """
            elif k == 7:   
                if toplam_kumule >= toplam_2022:
                   toplam_scale = 22
                else:
                   toplam_scale = -22
                ax.text(x[start_index + j] + i * len(columns), value + isemri_kumule/30, "%" + str(round(100 * ((toplam_2022 - toplam_kumule) / toplam_kumule))), ha='center', fontsize=10)
                ax.annotate('', xy=(x[start_index+j]+i*len(columns), value+0.01), xytext=(x[start_index+j]+i*len(columns), value+0.3),
                arrowprops=dict(facecolor='#0E3A2F', arrowstyle='simple', lw=1.5, mutation_scale=toplam_scale))
            """
            k += 1

    red_patch_1 = plt.Line2D([0], [0], color='#0E3A2F', lw=4, label=lastyear)

    # Create the second legend for the blue line
    blue_patch = plt.Line2D([0], [0], color='#78FAAE', lw=4, label=year)

    # Add both legends to the same axes
    ax.legend(handles=[red_patch_1, blue_patch])
            
    # Grafiğin etiketleri
    ax.set_title("")
    ax.set_ylabel("")
    #ax.legend()
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['left'].set_visible(False)
    ax.set_yticks([])

    # Sütunların altındaki isimlendirme
    tick_locations = []
    for i in range(len(groups)):
        start_index = i * 2
        end_index = start_index + 2
        mid_point = (x[start_index] + x[end_index - 1]) / 2  # Calculate midpoint of group
        tick_locations.append(mid_point + i * len(columns))  # Add to list of tick locations
    ax.set_xticks(tick_locations)
    ax.set_xticklabels(['İş Emri', 'Parça', 'Aksesuar'])

    #plt.show()
    plt.savefig(png_name + '.png', dpi=300, bbox_inches='tight')

def plot_line_(titl, png_name, last_month_data=False):
    now = datetime.now()
    if last_month_data == False:
        year = now.year
        month = now.month
    elif last_month_data == True:
        year = now.year
        month = now.month
        month = month - 1
        
    num_days = calendar.monthrange(year, month)[1]

    conn = pymysql.connect(host='localhost', user='root', db='ya_rpa')
    cursor = conn.cursor()
    query = "Select * from sshparca_data where Month = '{}' AND Year = '{}' ORDER BY Day;".format(month, year)

    result = cursor.execute(query)
    datas = cursor.fetchall()

    x_axis_vals = []
    adet_vals = []
    for data in datas:
        id_fromtuple, tarihi_fromtuple, gun_fromtuple, ay_fromtuple, yil_fromtuple, adet_bin_fromtuple, gun_text_fromtuple = data
        x_axis_vals.append(gun_fromtuple)
        adet_vals.append(adet_bin_fromtuple)
    
    week_list = x_axis_vals
    Gelen_Telefon_list = adet_vals

    num_days = calendar.monthrange(year, month)[1]

    if month == 1:
        ay = "Ocak"
    elif month == 2:
        ay = "Şubt"
    elif month == 3:
        ay = "Mar"
    elif month == 4:
        ay = "Nis"
    elif month == 5:
        ay = "May"
    elif month == 6:
        ay = "Haz"
    elif month == 7:
        ay = "Tem"
    elif month == 8:
        ay = "Ağus"
    elif month == 9:
        ay = "Eyl"
    elif month == 10:
        ay = "Ekim"
    elif month == 11:
        ay = "Kas"
    elif month == 12:
        ay = "Aral"

    x = week_list
    y1 = Gelen_Telefon_list

    max_val = max(y1)

    # Create a figure and axis object
    fig, ax = plt.subplots()

    # Plot the data as two line graphs
    ax.plot(x, y1, color='#78FAAE', linewidth=3, label='', marker='o', markerfacecolor='#0E3A2F')
    #ax.plot(x, y2, color='#FAEB67', linewidth=3, label='Gelen Müşteri', marker='o', markerfacecolor='#F7B046')

    # Add some custom styling to the plot
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.set_xlabel('')
    #ax.set_ylabel('Adet')
    ax.set_title(titl)

    #ax.legend()

    for i in range(len(x)):
        plt.text(x[i], y1[i] + 25, f"{format_with_period(y1[i])}", fontsize=9, weight='bold')

    plt.xticks(fontsize=9)
    plt.yticks(fontsize=9)
    plt.xlim(0, 30)

    ticks = []
    for i in range(num_days):
        ticks.append(i + 1)

    labels = []
    for i in range(num_days):
        labels.append(str(i + 1) + '-' + ay)

    plt.xticks(ticks, labels, rotation=90)

    x = 0
    while x <= max_val + 100:
        ax.axhline(x, color='#0E3A2F', linestyle='--', alpha=0.05)
        x = x + 1000

    fig.set_size_inches(12, 6)
    plt.tight_layout()
    fig.savefig(png_name + '.png')
    #plt.show()

def plot_line_2(titl, png_name, last_month_data=False):
    now = datetime.now()
    if last_month_data == False:
        year = now.year
        month = now.month
    elif last_month_data == True:
        year = now.year
        month = now.month 
        month = month - 1
    num_days = calendar.monthrange(year, month)[1]

    conn = pymysql.connect(host='localhost', user='root', db='ya_rpa')
    cursor = conn.cursor()
    query = "Select * from sshparca_data2 where Month = '{}' AND year = '{}' ORDER BY Day;".format(month, year)

    result = cursor.execute(query)
    datas = cursor.fetchall()

    x_axis_vals = []
    adet_vals = []
    for data in datas:
        id_fromtuple, tarihi_fromtuple, gun_fromtuple, ay_fromtuple, yil_fromtuple, servisgirisi_fromtuple, gun_fromtuple2 = data
        x_axis_vals.append(gun_fromtuple)
        adet_vals.append(servisgirisi_fromtuple)
    
    week_list = x_axis_vals
    Gelen_Telefon_list = adet_vals
    
    num_days = calendar.monthrange(year, month)[1]

    if month == 1:
        ay = "Ocak"
    elif month == 2:
        ay = "Şubt"
    elif month == 3:
        ay = "Mar"
    elif month == 4:
        ay = "Nis"
    elif month == 5:
        ay = "May"
    elif month == 6:
        ay = "Haz"
    elif month == 7:
        ay = "Tem"
    elif month == 8:
        ay = "Ağus"
    elif month == 9:
        ay = "Eyl"
    elif month == 10:
        ay = "Ekim"
    elif month == 11:
        ay = "Kas"
    elif month == 12:
        ay = "Aral"

    x = week_list
    y1 = Gelen_Telefon_list

    max_val = max(y1)

    # Create a figure and axis object
    fig, ax = plt.subplots()

    # Plot the data as two line graphs
    ax.plot(x, y1, color='#78FAAE', linewidth=3, label='', marker='o', markerfacecolor='#0E3A2F')
    #ax.plot(x, y2, color='#FAEB67', linewidth=3, label='Gelen Müşteri', marker='o', markerfacecolor='#F7B046')

    # Add some custom styling to the plot
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.set_xlabel('')
    #ax.set_ylabel('Adet')
    ax.set_title(titl)

    #ax.legend()

    for i in range(len(x)):
        plt.text(x[i], y1[i] + 25, f"{format_with_period(y1[i])}", fontsize=9, weight='bold')

    plt.xticks(fontsize=9)
    plt.yticks(fontsize=9)
    plt.xlim(0, 30)

    ticks = []
    for i in range(num_days):
        ticks.append(i + 1)

    labels = []
    for i in range(num_days):
        labels.append(str(i + 1) + '-' + ay)

    plt.xticks(ticks, labels, rotation=90)

    x = 0
    while x <= max_val + 100:
        ax.axhline(x, color='#0E3A2F', linestyle='--', alpha=0.05)
        x = x + 200

    fig.set_size_inches(12, 6)
    plt.tight_layout()
    fig.savefig(png_name + '.png')
    #plt.show()

def plot_aksesuar_graph(month, year, png_name="aksesuar_satis_grafik"):
    days, aksesuar_isemri_satis = ssh_aksesuar_isemri_fromOraDB(month, year)
    days2, aksesuar_banko_satis = ssh_aksesuar_banko_fromOraDB(month, year)
    days = [int(day) for day in days]
    days2 = [int(day) for day in days2]

    sales_dict = {}

    # Process the first store's sales
    for day, sale in zip(days, aksesuar_isemri_satis):
        if day in sales_dict:
            sales_dict[day] += sale
        else:
            sales_dict[day] = sale

    # Process the second store's sales
    for day, sale in zip(days2, aksesuar_banko_satis):
        if day in sales_dict:
            sales_dict[day] += sale
        else:
            sales_dict[day] = sale

    # Extract the combined days and sales
    combined_days = sorted(sales_dict.keys())
    combined_sales = [sales_dict[day] for day in combined_days]

    num_days = calendar.monthrange(year, month)[1]

    months_tr = ["Ocak", "Şub", "Mart", "Nisan", "May", "Haz", "Temmuz", "Ağustos", "Eyl", "Ekim", "Kas", "Ara"]
    ay = months_tr[month - 1]

    fig, ax = plt.subplots()

    # Plot sales data points
    prev_day = 1
    for i, day in enumerate(combined_days):
        if day - prev_day > 1:
            ax.plot([], [])  # Skip days with no sales data
        ax.plot(day, combined_sales[i], color='#78FAAE', marker='o', markerfacecolor='#0E3A2F')
        prev_day = day

    # Connect data points with lines
    plt.plot(combined_days, combined_sales, color='#78FAAE', linewidth=3)

    # Custom styling
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.set_xlabel('')
    ax.set_title("Aksesuar Satışı (BİN ₺)")

    # Set y-axis limits
    max_val = max(combined_sales)
    plt.ylim(0, max_val + 10000)

    for i, day in enumerate(combined_days):
        plt.text(day, combined_sales[i] + max_val/100, f"{combined_sales[i]:,.0f}", fontsize=9, weight='bold')

    plt.xticks(range(1, num_days + 1), [f"{day}-{ay}" for day in range(1, num_days + 1)], fontsize=9, rotation=90)
    plt.yticks(fontsize=9)

    # Add horizontal lines
    x = 0
    while x <= max_val + 10000:
        ax.axhline(x, color='#0E3A2F', linestyle='--', alpha=0.05)
        x = x + 10000

    fig.set_size_inches(12, 6)
    plt.tight_layout()

    plt.savefig(f"{png_name}.png")
    #plt.show()

def plot_circlu_(percan_1, perc_1, label2, label1, baslik, png_name):
    # Doing this if below so the graphic will not have any color if percentage is higher than 100%
    if perc_1 < 0:
        perc_1 = 0

    # Create data for the pie chart
    sizes = [abs(perc_1), abs(percan_1)]
    colors = ['#78FAAE', '#0E3A2F']
    labels = [label1, label2]

    # Create the pie chart
    fig, ax = plt.subplots()
        
    wedges, texts = ax.pie(sizes, colors=colors, startangle=90, wedgeprops={'edgecolor': 'white'})

    # Add labels and percentage values to the chart
    percentage_values = ['{}%'.format(int(round(s))) for s in sizes]
    labels_with_values = ['{} ({})'.format(label, percentage_values[i]) for i, label in enumerate(labels)]
    #ax.legend(wedges, labels_with_values, loc=(0.5, -0.1))  # changed loc parameter to move the legend below

    # Create an empty circle in the center of the pie chart
    centre_circle = plt.Circle((0, 0), 0.8, color='white', fc='white', linewidth=1.25)
    ax.add_artist(centre_circle)

    # Add the value of perc_1 to the center of the pie chart
    ax.text(0, 0, f'{percan_1}%', ha='center', va='center', fontsize=28, fontweight='bold')

    # Add a title
    ax.set_title(baslik, fontweight="bold", fontsize=22)

    # Set the font size for the labels and values
    for text in texts:
        text.set_fontsize(22)

    # Save the figure
    plt.savefig(png_name + '.png', dpi=300, bbox_inches='tight')
