import flet as ft
import json
import os

def main(page: ft.Page):
    # --- AYARLAR ---
    page.title = "Emergency Ezber"
    page.theme_mode = "dark"
    page.bgcolor = "#1a1a1a"
    page.window_width = 450
    page.window_height = 800
    page.scroll = "adaptive" # Liste uzun olduğu için kaydırma özelliği açıldı

    # --- DOSYA SİSTEMİ ---
    # Dosya adını değiştirdim ki eski boş listenle karışmasın.
    DOSYA_ADI = "emergency_listesi.json"

    # --- SENİN GÖNDERDİĞİN LİSTE ---
    baslangic_listesi = [
        {"name": "2. -100M ÜZERİNDE", "done": False},
        {"name": "3. -100M ALTINDA", "done": False},
        {"name": "4. -12.000KG GW'İN ALTINDA", "done": False},
        {"name": "5. -12.000KG GW'İN ÜZERİNDE", "done": False},
        {"name": "6. -80KM/H'İN ALTINDA", "done": False},
        {"name": "8. -3M'YE KADAR", "done": False},
        {"name": "9. -3-5M ARASINDA", "done": False},
        {"name": "10. -5-10M ARASINDA", "done": False},
        {"name": "11. -110M VE ÜZERİNDE", "done": False},
        {"name": "12. KALKIŞTA TEK MOTOR ARIZASI", "done": False},
        {"name": "13. İRTİFA 10M ALTINDA VE SÜRAT 60KM ALTINDA", "done": False},
        {"name": "14. İRTİFA 10M ÜZERİNDE VE SÜRAT 60KM ÜZERİNDE", "done": False},
        {"name": "16. İRTİFA 100M ÜZERİNDE VE SÜRAT 80KM ÜZERİNDE", "done": False},
        {"name": "17. İRTİFA 100M ALTINDA VE SÜRAT 120KM ÜZERİNDE", "done": False},
        {"name": "18. İRTİFA 100M ALTINDA VE SÜRAT 80KM ALTINDA", "done": False},
        {"name": "19. YANGIN", "done": False},
        {"name": "20. DİŞLİ KUTULARINDA ARIZA", "done": False},
        {"name": "21. MOTOR OTOMATİK KONTROL SİSTEMİ ARIZASI", "done": False},
        {"name": "22. EEG FREE TURB ARIZASI", "done": False},
        {"name": "23. ELEKTRONİK REGÜLATÖR ARIZASI", "done": False},
        {"name": "24. MOTORLARDA ANORMAL TİTREŞİM", "done": False},
        {"name": "25. DÜŞÜK MOTOR YAĞ BASINCI", "done": False},
        {"name": "26. MOTOR YAĞ BASINCI 2 KgF/CM²'YE DÜŞERSE", "done": False},
        {"name": "27. MOTOR YAĞ BASINCI 2 KgF/CM²'NİN ALTINA DÜŞERSE", "done": False},
        {"name": "28. MOTOR CHIP DEDEKTÖR İKAZ IŞIĞININ YANMASI", "done": False},
        {"name": "29. MOTORUN DÜZENSİZ ÇALIŞMASI", "done": False},
        {"name": "30. TIT KONTROLÜ ARIZASI", "done": False},
        {"name": "31. YAKIT BOOSTER POMPASININ ARIZALANMASI", "done": False},
        {"name": "32. YAKIT TRANSFER POMPALARI ARIZASI", "done": False},
        {"name": "33. 270 LT FUEL RSV IŞIĞININ YANMASI", "done": False},
        {"name": "34. YAKIT FİLTRESİNİN TIKANMASI", "done": False},
        {"name": "35. HİDROLİK SİSTEMİN ARIZALANMASI", "done": False},
        {"name": "36. UÇUŞ ESNASINDA DÜŞÜK FREKANSLI TİTREŞİM", "done": False},
        {"name": "37. BİR AC JENERATÖR ARIZASI", "done": False},
        {"name": "38. ÇİFT AC JENERATÖR ARIZASI", "done": False},
        {"name": "39. TEK RECTIFIER ARIZASI", "done": False},
        {"name": "40. İKİ RECTIFIER ARIZASI", "done": False},
        {"name": "41. DMR 200 RÖLE ARIZASI", "done": False},
        {"name": "42. BASINÇ ALTİMETRESİNİN ARIZALANMASI", "done": False},
        {"name": "43. SOL SÜRAT SAATİNİN ARIZALANMASI", "done": False},
        {"name": "44. T/R PITCH LİMİT SİSTEMİ ARIZASI", "done": False}
    ]

    def verileri_yukle():
        if os.path.exists(DOSYA_ADI):
            try:
                with open(DOSYA_ADI, "r", encoding="utf-8") as f:
                    return json.load(f)
            except:
                return baslangic_listesi 
        else:
            return baslangic_listesi

    def verileri_kaydet(data):
        with open(DOSYA_ADI, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False)

    tasks_data = verileri_yukle()

    # --- ARAYÜZ ELEMANLARI ---
    tasks_view = ft.Column()
    new_task = ft.TextField(hint_text="Yeni ekle...", expand=True)

    # --- FONKSİYONLAR ---
    def load_tasks():
        tasks_view.controls.clear()
        
        # Kalan Sayısı Hesaplama
        kalan_sayisi = len([x for x in tasks_data if not x["done"]])
        progress_text.value = f"Kalan Emergency: {kalan_sayisi}"
        
        for item in tasks_data:
            if not item["done"]: 
                tasks_view.controls.append(
                    ft.Container(
                        content=ft.Checkbox(
                            label=item["name"], 
                            value=False,
                            on_change=lambda e, n=item["name"]: checkbox_changed(e, n)
                        ),
                        padding=10,
                        bgcolor="#333333", 
                        border_radius=10,
                        margin=2
                    )
                )
        page.update()

    def checkbox_changed(e, task_name):
        for item in tasks_data:
            if item["name"] == task_name:
                item["done"] = True 
        
        verileri_kaydet(tasks_data)
        load_tasks()
        page.update()

    def add_clicked(e):
        if new_task.value:
            tasks_data.append({"name": new_task.value, "done": False})
            verileri_kaydet(tasks_data)
            new_task.value = ""
            load_tasks()
            page.update()

    def reset_clicked(e):
        # Listeyi sıfırlama (Tekrar modu)
        for item in tasks_data:
            item["done"] = False
        verileri_kaydet(tasks_data)
        load_tasks()
        page.update()

    # --- SAYFA DÜZENİ ---
    
    # İstatistik Yazısı
    progress_text = ft.Text("Kalan:", size=18, color="orange")
    
    # Ekle Butonu
    add_btn = ft.ElevatedButton(content=ft.Text("EKLE"), on_click=add_clicked)
    
    # Sıfırla Butonu (En alta koyacağız)
    reset_btn = ft.ElevatedButton(content=ft.Text("HEPSİNİ TEKRARLA"), on_click=reset_clicked, bgcolor="red", color="white")

    page.add(
        ft.Text("Mi-17 Emergency", size=25, weight="bold"),
        progress_text,
        ft.Divider(),
        ft.Row([new_task, add_btn]),
        tasks_view,
        ft.Divider(),
        reset_btn
    )

    load_tasks()

ft.app(target=main)