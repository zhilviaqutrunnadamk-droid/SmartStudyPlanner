import tkinter as tk
from tkinter import ttk, messagebox
class SmartStudyPlanner:
    def __init__(self, root):
        self.root = root
        self.root.title("Smart Study Planner")
        self.root.geometry("950x650")

        self.courses = []
        self.slots = []

        self.create_ui()

    def create_ui(self):
        title = tk.Label(
            self.root,
            text="SMART STUDY PLANNER",
            font=("Arial", 20, "bold"),
            bg="#243b53",
            fg="white",
            pady=15
        )
        title.pack(fill="x")

        main = tk.Frame(self.root, padx=15, pady=15)
        main.pack(fill="both", expand=True)

        left = tk.Frame(main)
        left.pack(side="left", fill="y", padx=10)

        right = tk.Frame(main)
        right.pack(side="right", fill="both", expand=True)

        # Input mata kuliah
        tk.Label(left, text="Nama Mata Kuliah").pack(anchor="w")
        self.course_entry = tk.Entry(left, width=30)
        self.course_entry.pack(pady=5)

        tk.Label(left, text="Prioritas").pack(anchor="w")
        self.priority = ttk.Combobox(
            left,
            values=["3 - Tinggi", "2 - Sedang", "1 - Rendah"],
            state="readonly"
        )
        self.priority.current(1)
        self.priority.pack(pady=5)

        tk.Label(left, text="Target Sesi Belajar").pack(anchor="w")
        self.target = tk.Entry(left, width=30)
        self.target.insert(0, "2")
        self.target.pack(pady=5)

        tk.Button(
            left,
            text="Tambah Mata Kuliah",
            command=self.add_course
        ).pack(fill="x", pady=5)

        self.course_list = tk.Listbox(left, width=35, height=8)
        self.course_list.pack(pady=5)

        tk.Button(
            left,
            text="Hapus Mata Kuliah",
            command=self.delete_course
        ).pack(fill="x", pady=5)

        # Input waktu luang
        tk.Label(left, text="Hari").pack(anchor="w", pady=(10, 0))
        self.day = ttk.Combobox(
            left,
            values=[
                "Senin", "Selasa", "Rabu", "Kamis",
                "Jumat", "Sabtu", "Minggu"
            ],
            state="readonly"
        )
        self.day.current(0)
        self.day.pack(pady=5)

        tk.Label(left, text="Waktu Mulai (HH:MM)").pack(anchor="w")
        self.start_time = tk.Entry(left)
        self.start_time.insert(0, "08:00")
        self.start_time.pack(pady=5)

        tk.Label(left, text="Waktu Selesai (HH:MM)").pack(anchor="w")
        self.end_time = tk.Entry(left)
        self.end_time.insert(0, "12:00")
        self.end_time.pack(pady=5)

        tk.Button(
            left,
            text="Tambah Waktu Luang",
            command=self.add_slot
        ).pack(fill="x", pady=5)

        self.slot_list = tk.Listbox(left, width=35, height=6)
        self.slot_list.pack(pady=5)

        tk.Button(
            left,
            text="Hapus Waktu Luang",
            command=self.delete_slot
        ).pack(fill="x", pady=5)

        # Hasil jadwal
        tk.Label(
            right,
            text="HASIL JADWAL BELAJAR",
            font=("Arial", 14, "bold")
        ).pack(pady=10)

        tk.Button(
            right,
            text="BUAT JADWAL OTOMATIS",
            bg="#243b53",
            fg="white",
            command=self.generate_schedule
        ).pack(fill="x", pady=5)

        tk.Button(
            right,
            text="RESET SEMUA DATA",
            command=self.reset
        ).pack(fill="x", pady=5)

        self.result = tk.Text(
            right,
            font=("Consolas", 11),
            wrap="word"
        )
        self.result.pack(fill="both", expand=True, pady=10)

    def add_course(self):
        name = self.course_entry.get().strip()

        try:
            target = int(self.target.get())
            if target < 1:
                raise ValueError
        except ValueError:
            messagebox.showerror(
                "Kesalahan",
                "Target sesi harus berupa angka minimal 1."
            )
            return

        if not name:
            messagebox.showwarning(
                "Peringatan",
                "Masukkan nama mata kuliah."
            )
            return

        if any(c["name"].lower() == name.lower()
               for c in self.courses):
            messagebox.showwarning(
                "Peringatan",
                "Mata kuliah sudah ditambahkan."
            )
            return

        priority = int(self.priority.get()[0])

        self.courses.append({
            "name": name,
            "priority": priority,
            "target": target
        })

        self.refresh_courses()
        self.course_entry.delete(0, tk.END)

    def refresh_courses(self):
        self.course_list.delete(0, tk.END)

        for c in self.courses:
            self.course_list.insert(
                tk.END,
                f'{c["name"]} | Prioritas {c["priority"]} | '
                f'{c["target"]} sesi'
            )

    def delete_course(self):
        selected = self.course_list.curselection()

        if not selected:
            messagebox.showwarning(
                "Peringatan",
                "Pilih mata kuliah yang ingin dihapus."
            )
            return

        del self.courses[selected[0]]
        self.refresh_courses()

    def add_slot(self):
        day = self.day.get()

        try:
            start = self.convert_time(self.start_time.get())
            end = self.convert_time(self.end_time.get())
        except ValueError:
            messagebox.showerror(
                "Kesalahan",
                "Gunakan format waktu HH:MM, misalnya 08:00."
            )
            return

        if end <= start:
            messagebox.showerror(
                "Kesalahan",
                "Waktu selesai harus setelah waktu mulai."
            )
            return

        for slot in self.slots:
            if slot["day"] == day:
                if start < slot["end"] and end > slot["start"]:
                    messagebox.showwarning(
                        "Peringatan",
                        "Waktu tersebut bertumpuk dengan jadwal lain."
                    )
                    return

        self.slots.append({
            "day": day,
            "start": start,
            "end": end
        })

        urutan_hari = [
            "Senin", "Selasa", "Rabu", "Kamis",
            "Jumat", "Sabtu", "Minggu"
        ]

        self.slots.sort(
            key=lambda s: (
                urutan_hari.index(s["day"]),
                s["start"]
            )
        )

        self.refresh_slots()

    def refresh_slots(self):
        self.slot_list.delete(0, tk.END)

        for slot in self.slots:
            self.slot_list.insert(
                tk.END,
                f'{slot["day"]}: '
                f'{self.format_time(slot["start"])} - '
                f'{self.format_time(slot["end"])}'
            )

    def delete_slot(self):
        selected = self.slot_list.curselection()

        if not selected:
            messagebox.showwarning(
                "Peringatan",
                "Pilih waktu luang yang ingin dihapus."
            )
            return

        del self.slots[selected[0]]
        self.refresh_slots()

    def convert_time(self, value):
        hour, minute = map(int, value.split(":"))

        if not (0 <= hour < 24 and 0 <= minute < 60):
            raise ValueError

        return hour * 60 + minute

    def format_time(self, minutes):
        return f"{minutes // 60:02d}:{minutes % 60:02d}"

    def generate_schedule(self):
        if not self.courses:
            messagebox.showwarning(
                "Peringatan",
                "Tambahkan mata kuliah terlebih dahulu."
            )
            return

        if not self.slots:
            messagebox.showwarning(
                "Peringatan",
                "Tambahkan waktu luang terlebih dahulu."
            )
            return

        available = []

        # Membagi waktu luang menjadi sesi 60 menit
        for slot in self.slots:
            current = slot["start"]

            while current + 60 <= slot["end"]:
                available.append({
                    "day": slot["day"],
                    "start": current,
                    "end": current + 60
                })
                current += 60

        # Mengurutkan berdasarkan prioritas tertinggi
        ordered_courses = sorted(
            self.courses,
            key=lambda c: -c["priority"]
        )

        schedule = []
        index = 0

        total_target = sum(
            c["target"] for c in self.courses
        )

        # Proses Planning
        for course in ordered_courses:
            for _ in range(course["target"]):
                if index >= len(available):
                    break

                schedule.append({
                    "course": course["name"],
                    "priority": course["priority"],
                    **available[index]
                })

                index += 1

        # Menampilkan hasil
        self.result.delete("1.0", tk.END)

        self.result.insert(
            tk.END,
            "JADWAL BELAJAR OTOMATIS\n"
            "====================================\n\n"
        )

        self.result.insert(
            tk.END,
            f"Total target sesi : {total_target}\n"
            f"Sesi terjadwal    : {len(schedule)}\n"
            f"Belum terjadwal   : {total_target - len(schedule)}\n\n"
        )

        days = [
            "Senin", "Selasa", "Rabu", "Kamis",
            "Jumat", "Sabtu", "Minggu"
        ]

        for day in days:
            daily = [
                item for item in schedule
                if item["day"] == day
            ]

            if daily:
                self.result.insert(
                    tk.END,
                    f"{day.upper()}\n"
                )

                for item in daily:
                    priority_name = {
                        3: "Tinggi",
                        2: "Sedang",
                        1: "Rendah"
                    }[item["priority"]]

                    self.result.insert(
                        tk.END,
                        f'{self.format_time(item["start"])} - '
                        f'{self.format_time(item["end"])} | '
                        f'{item["course"]} '
                        f'(Prioritas {priority_name})\n'
                    )

                self.result.insert(tk.END, "\n")

        if len(schedule) < total_target:
            self.result.insert(
                tk.END,
                "Catatan: Tambahkan waktu luang atau "
                "kurangi target sesi agar semua jadwal terpenuhi."
            )
        else:
            self.result.insert(
                tk.END,
                "Semua target belajar berhasil dijadwalkan!"
            )

    def reset(self):
        if messagebox.askyesno(
            "Konfirmasi",
            "Yakin ingin menghapus semua data?"
        ):
            self.courses.clear()
            self.slots.clear()
            self.refresh_courses()
            self.refresh_slots()
            self.result.delete("1.0", tk.END)


if __name__ == "__main__":
    root = tk.Tk()
    app = SmartStudyPlanner(root)
    root.mainloop()
