import PySimpleGUI as sg
import csv
sg.theme('DarkBlue4')
sg.Popup("Добро пожаловать, дорогой друг!")
layout = [
    [sg.Text('Введите артиста или музыкальную группу'), sg.InputText(key='-IN-'), sg.Button('Run')],
    [sg.Cancel()]]
window = sg.Window('Results', layout)
while True:
    event, values = window.read()
    if event == 'Run':
        window.close()
        def sql_start():
                name = values['-IN-']
                import psycopg2
                from psycopg2 import sql
                conn = psycopg2.connect(dbname='musicbrainz', user='musicbrainz',
                                        password='musicbrainz', host='localhost', port="15432")

                cursor = conn.cursor()
                cursor.execute(
                    sql.SQL(" SELECT DISTINCT r.name AS album, t.name AS track,t.position AS album_position "
                            "FROM artist_credit_name ac "
                            "JOIN release r ON ac.artist_credit= r.artist_credit "
                            "JOIN medium m ON r.id=m.id "
                            "JOIN track t ON (r.artist_credit=t.artist_credit AND t.medium=m.id)"
                            " WHERE ac.name= %(name)s "
                            "ORDER BY t.position "
                            "LIMIT 50"), {"name": name})
                result = cursor.fetchall()
                with open("path\Res.csv", "w") as csv_file:
                    c = csv.writer(csv_file)
                    for x in result:
                        c.writerow(x)
                cursor.close()
                conn.close()
        sql_start()
        def table_example():
            try:
                with open("path\Res.csv", "r") as in_file:
                    reader = csv.reader(in_file)
                    data = list(reader)
                    header_list = ["Альбом", 'Трек', 'Номер трека в альбоме']
                    sg.set_options(element_padding=(0, 0))
                    layout = [[sg.Table(values=data,
                                        headings=header_list,
                                        max_col_width=100,
                                        auto_size_columns=True,
                                        justification='left',
                                        num_rows=min(len(data), 20))]]
                    window = sg.Window('Table', layout, grab_anywhere=False)
                    event, values = window.read()
            except KeyError:
                sg.Popup("Артист не найден,либо введен с ошибкой,запустите заново")
        table_example()
    if event in (None, 'Cancel'):
        break
window.close()


