import xml.etree.ElementTree as ET
import os
import tkinter as tk
from tkinter import filedialog

TO_EXPORT = 'export_xml'

def dodaj_atrybuty_wymiarow(offer):
    wymiary_element = offer.find(".//property[@name='wymiary']")

    szerokosc, glebokosc, wysokosc, srednica = None, None, None, None

    if wymiary_element is not None:
        wymiary = wymiary_element.text

        if wymiary.startswith('o'):
            wymiary = wymiary[1:]
            wymiary_czesci = wymiary.split('x')

            srednica = wymiary_czesci[0].strip() if len(wymiary_czesci) >= 1 else ''
            wysokosc = wymiary_czesci[1].strip() if len(wymiary_czesci) >= 2 else ''

        elif wymiary.startswith('śr. '):
            wymiary = wymiary[4:]
            wymiary_czesci = wymiary.split('x')

            srednica = wymiary_czesci[0].strip() if len(wymiary_czesci) >= 1 else ''
            wysokosc = wymiary_czesci[1].strip() if len(wymiary_czesci) >= 2 else ''

        elif wymiary.startswith('śr.'):
            wymiary = wymiary[3:]
            wymiary_czesci = wymiary.split('x')

            srednica = wymiary_czesci[0].strip() if len(wymiary_czesci) >= 1 else ''
            wysokosc = wymiary_czesci[1].strip() if len(wymiary_czesci) >= 2 else ''

        elif wymiary.startswith('(L)'):
            wymiary = wymiary[3:]
            dlugosc = wymiary

        else:
            wymiary_czesci = wymiary.split('x')

            szerokosc = wymiary_czesci[0].strip() if len(wymiary_czesci) >= 1 else ''
            glebokosc = wymiary_czesci[1].strip() if len(wymiary_czesci) >= 2 else ''
            wysokosc = wymiary_czesci[2].strip() if len(wymiary_czesci) >= 3 else ''

        if wysokosc.startswith('(H)'):
            wysokosc = wysokosc[3:]

        if wysokosc.endswith('mm'):
            wysokosc = wysokosc[:-2]

    if srednica and wysokosc:
        check_srednica = offer.find(".//property[@name='szerokość']")
        check_wysokosc = offer.find(".//property[@name='wysokość']")
        if check_srednica is None and check_wysokosc is None:
            atrybut_srednica = ET.Element("property", {"name": "średnica"})
            atrybut_srednica.text = srednica

            atrybut_wysokosc = ET.Element("property", {"name": "wysokość"})
            atrybut_wysokosc.text = wysokosc

            index = list(offer).index(wymiary_element)
            offer.insert(index + 1, atrybut_srednica)
            offer.insert(index + 2, atrybut_wysokosc)

    elif szerokosc and glebokosc and wysokosc:
        check_szerokosc = offer.find(".//property[@name='szerokość']")
        check_glebokosc = offer.find(".//property[@name='głębokość']")
        check_dlugosc = offer.find(".//property[@name='długość']")
        check_wysokosc = offer.find(".//property[@name='wysokość']")

        if check_szerokosc is None and check_glebokosc is None and check_dlugosc is None and check_wysokosc is None:
            print('dodaje atrybuty')
            atrybut_szerokosc = ET.Element("property", {"name": "szerokość"})
            atrybut_szerokosc.text = szerokosc

            atrybut_glebokosc = ET.Element("property", {"name": "głębokość"})
            atrybut_glebokosc.text = glebokosc

            atrybut_wysokosc = ET.Element("property", {"name": "wysokość"})
            atrybut_wysokosc.text = wysokosc

            index = list(offer).index(wymiary_element)
            offer.insert(index + 1, atrybut_szerokosc)
            offer.insert(index + 2, atrybut_glebokosc)
            offer.insert(index + 3, atrybut_wysokosc)

    elif dlugosc:
        check_dlugosc = offer.find(".//property[@name='długość']")
        if check_dlugosc is None:
            atrybut_dlugosc = ET.Element("property", {"name": "długość"})
            atrybut_dlugosc.text = dlugosc

            index = list(offer).index(wymiary_element)
            offer.insert(index + 1, atrybut_dlugosc)


def dodaj_atrybuty_mocy_napiecia(offer):
    moc_napiecie_element = offer.find(".//property[@name='moc/napięcie (W/V)']")

    if moc_napiecie_element is not None:
        moc_napiecie = moc_napiecie_element.text
        moc, napiecie = moc_napiecie.split('/') if '/' in moc_napiecie else ('', '')
    else:
        moc, napiecie = '', ''

    if moc:
        atrybut_moc = ET.Element("property", {"name": "moc elektryczna"})
        atrybut_moc.text = moc
        index = list(offer).index(moc_napiecie_element)
        offer.insert(index + 1, atrybut_moc)

    if napiecie:
        atrybut_napiecie = ET.Element("property", {"name": "napięcie"})
        atrybut_napiecie.text = napiecie
        index = list(offer).index(moc_napiecie_element)
        offer.insert(index + 2, atrybut_napiecie)

def init_tkinter():
    root = tk.Tk()
    root.withdraw()
    root.silence_deprecation = True
    return root

def select_files():
    root = init_tkinter()
    files = filedialog.askopenfilenames(filetypes=[("XML files", "*.xml")])
    return files

def select_export_folder():
    root = init_tkinter()
    folder = filedialog.askdirectory()
    return folder

def indent(elem, level=0):
    i = "\n" + level*"  "
    if len(elem):
        if not elem.text or not elem.text.strip():
            elem.text = i + "  "
        if not elem.tail or not elem.tail.strip():
            elem.tail = i
        for elem in elem:
            indent(elem, level+1)
        if not elem.tail or not elem.tail.strip():
            elem.tail = i
    else:
        if level and (not elem.tail or not elem.tail.strip()):
            elem.tail = i

def main():
    files = select_files()
    if not files:
        messagebox.showinfo("Error", "No files selected")
        return

    export_folder = select_export_folder()
    if not export_folder:
        messagebox.showinfo("Error", "No export folder selected")
        return

    if not os.path.exists(export_folder):
        os.makedirs(export_folder)

    for file in files:
        tree = ET.parse(file)
        root = tree.getroot()

        for offer in root.findall('.//offer'):
            dodaj_atrybuty_wymiarow(offer)
            dodaj_atrybuty_mocy_napiecia(offer)

        indent(root)

        file_name = os.path.basename(file)
        export_path = os.path.join(export_folder, file_name)
        tree.write(export_path, encoding='utf-8', xml_declaration=True)

    messagebox.showinfo("Success", "Conversion completed")

if __name__ == '__main__':
    main()