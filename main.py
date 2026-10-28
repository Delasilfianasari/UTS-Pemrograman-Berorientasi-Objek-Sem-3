import json
from abc import ABC, abstractmethod
from pathlib import Path


# ============================================================
# BAGIAN 1: DATA KARYAWAN (EMPLOYEE)
# Aturan bonus:
# PERF2026  = bonus 10% dari gaji pokok
# SENIOR10  = bonus 10% dari gaji pokok
# LEAD2026  = bonus 15% dari gaji pokok
# Karyawan nonpermanen tidak mendapat bonus.
# Karyawan permanen tanpa kode bonus tidak mendapat bonus.
# ============================================================

class Employee(ABC):
    """Kelas induk/abstrak untuk seluruh jenis karyawan."""

    def __init__(self, emp_id, name, base_salary, is_permanent, bonus_code):
        self.emp_id = emp_id
        self.name = name
        self.base_salary = float(base_salary)
        self.is_permanent = bool(is_permanent)
        self.bonus_code = bonus_code

    def calculate_bonus(self):
        """Rule bonus diterapkan berdasarkan kode bonus."""
        if not self.is_permanent or not self.bonus_code:
            return 0.0

        bonus_rules = {
            "PERF2026": 0.10,
            "SENIOR10": 0.10,
            "LEAD2026": 0.15,
        }
        rate = bonus_rules.get(self.bonus_code, 0.0)
        return self.base_salary * rate

    @abstractmethod
    def employee_type(self):
        """Wajib diimplementasikan oleh kelas turunan."""
        pass

    def total_salary(self):
        return self.base_salary + self.calculate_bonus()

    def display(self):
        return (
            f"{self.emp_id:<9} | {self.name:<20} | "
            f"{self.employee_type():<14} | "
            f"Rp{self.base_salary:>12,.0f} | "
            f"Rp{self.calculate_bonus():>10,.0f} | "
            f"Rp{self.total_salary():>12,.0f}"
        )


class PermanentEmployee(Employee):
    """Kelas turunan untuk karyawan permanen."""

    def employee_type(self):
        return "Permanen"

    # Override: format laporan khusus karyawan permanen.
    def display(self):
        return "[TETAP] " + super().display()


class ContractEmployee(Employee):
    """Kelas turunan untuk karyawan nonpermanen/kontrak."""

    def calculate_bonus(self):
        # Override: karyawan kontrak tidak memperoleh bonus.
        return 0.0

    def employee_type(self):
        return "Nonpermanen"

    # Override: format laporan khusus karyawan kontrak.
    def display(self):
        return "[KONTRAK] " + super().display()


class EmployeeManager:
    def __init__(self, file_path):
        self.file_path = Path(file_path)
        self.employees = []

    def load_data(self):
        with self.file_path.open("r", encoding="utf-8") as file:
            data = json.load(file)

        self.employees = []
        for item in data.get("employees", []):
            if item.get("is_permanent", False):
                employee = PermanentEmployee(**item)
            else:
                employee = ContractEmployee(**item)
            self.employees.append(employee)

    def show_report(self):
        print("\\n" + "=" * 112)
        print("LAPORAN GAJI KARYAWAN")
        print("=" * 112)
        print("ID        | Nama                 | Status         | Gaji Pokok   | Bonus      | Total Gaji")
        print("-" * 112)
        for employee in self.employees:
            # Polymorphism: metode display() menyesuaikan jenis objek.
            print(employee.display())
        print("-" * 112)
        print(f"Jumlah karyawan : {len(self.employees)}")
        print(f"Total gaji pokok: Rp{sum(e.base_salary for e in self.employees):,.0f}")
        print(f"Total bonus     : Rp{sum(e.calculate_bonus() for e in self.employees):,.0f}")
        print(f"Total penggajian: Rp{sum(e.total_salary() for e in self.employees):,.0f}")


# ============================================================
# BAGIAN 2: PEMANTAUAN SENSOR (SENSOR LOGS)
# Rule status berdasarkan suhu:
# NORMAL  : suhu < 60 derajat
# WARNING : 60 <= suhu < 85 derajat
# DANGER  : suhu >= 85 derajat
# Status dari JSON tetap ditampilkan dan dibandingkan dengan
# status hasil rule suhu untuk pemeriksaan konsistensi.
# ============================================================

class Sensor(ABC):
    def __init__(self, sensor_id, location, temperature, status, operator_id):
        self.sensor_id = sensor_id
        self.location = location
        self.temperature = float(temperature)
        self.status = status
        self.operator_id = operator_id

    def determine_status(self):
        if self.temperature >= 85:
            return "DANGER"
        elif self.temperature >= 60:
            return "WARNING"
        return "NORMAL"

    @abstractmethod
    def sensor_type(self):
        pass

    def operator_label(self):
        return str(self.operator_id) if self.operator_id is not None else "Belum ditugaskan"

    def display(self):
        calculated = self.determine_status()
        consistency = "Sesuai" if calculated == self.status else "Periksa"
        return (
            f"{self.sensor_id:<9} | {self.location:<15} | "
            f"{self.temperature:>7.1f} °C | {self.status:<7} | "
            f"{calculated:<7} | {self.operator_label():<18} | "
            f"{consistency:<7} | {self.sensor_type()}"
        )


class DangerSensor(Sensor):
    def sensor_type(self):
        return "Sensor Bahaya"

    # Override: tampilkan peringatan khusus saat suhu berbahaya.
    def display(self):
        return "!!! " + super().display()


class NormalSensor(Sensor):
    def sensor_type(self):
        return "Sensor Normal"


class WarningSensor(Sensor):
    def sensor_type(self):
        return "Sensor Peringatan"

    # Override: penanda khusus untuk sensor berstatus WARNING.
    def display(self):
        return "!!  " + super().display()


class SensorManager:
    def __init__(self, file_path):
        self.file_path = Path(file_path)
        self.sensors = []

    def load_data(self):
        with self.file_path.open("r", encoding="utf-8") as file:
            data = json.load(file)

        self.sensors = []
        for item in data.get("readings", []):
            # Pemilihan subclass berdasarkan status yang ada di JSON.
            status = item.get("status", "NORMAL")
            if status == "DANGER":
                sensor = DangerSensor(**item)
            elif status == "WARNING":
                sensor = WarningSensor(**item)
            else:
                sensor = NormalSensor(**item)
            self.sensors.append(sensor)

    def show_report(self):
        print("\\n" + "=" * 125)
        print("LAPORAN PEMANTAUAN SENSOR")
        print("=" * 125)
        print("ID        | Lokasi          | Suhu       | Status JSON | Rule    | Operator           | Validasi | Jenis")
        print("-" * 125)
        for sensor in self.sensors:
            # Polymorphism: display() dipanggil dengan implementasi subclass.
            print(sensor.display())
        print("-" * 125)

        counts = {"NORMAL": 0, "WARNING": 0, "DANGER": 0}
        for sensor in self.sensors:
            counts[sensor.status] = counts.get(sensor.status, 0) + 1

        missing_operator = sum(1 for s in self.sensors if s.operator_id is None)
        mismatches = sum(1 for s in self.sensors if s.determine_status() != s.status)

        print(f"Jumlah sensor             : {len(self.sensors)}")
        print(f"Status NORMAL              : {counts['NORMAL']}")
        print(f"Status WARNING             : {counts['WARNING']}")
        print(f"Status DANGER              : {counts['DANGER']}")
        print(f"Belum memiliki operator   : {missing_operator}")
        print(f"Status perlu diperiksa     : {mismatches}")


def main():
    # File JSON harus berada di folder yang sama dengan main.py.
    folder = Path(__file__).resolve().parent

    try:
        employee_manager = EmployeeManager(folder / "employee.json")
        employee_manager.load_data()
        employee_manager.show_report()

        sensor_manager = SensorManager(folder / "sensor_logs.json")
        sensor_manager.load_data()
        sensor_manager.show_report()

    except FileNotFoundError as error:
        print(f"File tidak ditemukan: {error.filename}")
        print("Pastikan employee.json dan sensor_logs.json satu folder dengan main.py.")
    except json.JSONDecodeError as error:
        print(f"Format JSON tidak valid: {error}")


if __name__ == "__main__":
    main()
