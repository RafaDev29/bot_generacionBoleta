from fpdf import FPDF
import datetime

class BoletaPDF(FPDF):
    def titulo_boleta(self, mes, anio):
        # Título de la boleta
        self.set_font("Arial", 'B', 14)
        self.cell(0, 10, f"BOLETA DE PAGO - {mes} {anio}", ln=True, align='C')
        self.ln(10)
        
        
    def header(self):
        # Encabezado con el nombre de la empresa, RUC y dirección
        self.set_font("Arial", 'B', 12)
        self.cell(0, 10, "ABC", ln=True, align='C')
        self.set_font("Arial", size=10)
        self.cell(0, 10, "RUC: 20547896532", ln=True, align='C')
        self.cell(0, 10, "Dirección: AV LOS FRUTALES", ln=True, align='C')
        self.ln(10)

    

    def cuerpo_boleta(self, empleado, boleta):
        # Datos del empleado
        self.set_font("Arial", 'B', 10)
        self.cell(0, 10, "Datos del Trabajador", ln=True)
        self.set_font("Arial", size=10)
        self.cell(50, 10, f"Código: {empleado['codigo']}", border=1)
        self.cell(0, 10, f"Nombre: {empleado['nombres']} {empleado['apellidos']}", border=1, ln=True)
        self.cell(50, 10, f"DNI: {empleado['dni']}", border=1)
        self.cell(0, 10, f"Sueldo Básico: S/. {boleta['sueldo_basico']:.2f}", border=1, ln=True)
        self.cell(50, 10, f"Sistema de Pensión: {empleado['sistema_pension']}", border=1, ln=True)
        self.ln(10)

        # Tabla de ingresos y descuentos
        self.set_font("Arial", 'B', 10)
        self.cell(0, 10, "Ingresos y Descuentos", ln=True)
        self.set_font("Arial", size=10)
        self.cell(90, 10, "Concepto", border=1, align='C')
        self.cell(50, 10, "Monto Ingreso (S/.)", border=1, align='C')
        self.cell(50, 10, "Monto Descuento (S/.)", border=1, align='C')
        self.ln()

        # Ingresos
        self.cell(90, 10, "Sueldo Básico", border=1)
        self.cell(50, 10, f"{boleta['sueldo_basico']:.2f}", border=1)
        self.cell(50, 10, "", border=1)
        self.ln()
        self.cell(90, 10, "Bonificación", border=1)
        self.cell(50, 10, f"{boleta['bonificacion']:.2f}", border=1)
        self.cell(50, 10, "", border=1)
        self.ln()

        # Descuentos
        self.cell(90, 10, "Descuento Pensión", border=1)
        self.cell(50, 10, "", border=1)
        self.cell(50, 10, f"{boleta['descuento_pension']:.2f}", border=1)
        self.ln()

        # Totales
        self.set_font("Arial", 'B', 10)
        self.cell(90, 10, "Total Ingresos", border=1)
        self.cell(50, 10, f"{boleta['sueldo_basico'] + boleta['bonificacion']:.2f}", border=1)
        self.cell(50, 10, "", border=1)
        self.ln()
        self.cell(90, 10, "Total Descuentos", border=1)
        self.cell(50, 10, "", border=1)
        self.cell(50, 10, f"{boleta['descuento_pension']:.2f}", border=1)
        self.ln()
        self.cell(90, 10, "Total Neto", border=1)
        self.cell(50, 10, f"{boleta['sueldo_neto']:.2f}", border=1)
        self.cell(50, 10, "", border=1)
        self.ln(20)

    def firmas(self):
        # Campos para firmas del gerente y del empleado
        self.cell(90, 10, "_________________________", ln=0, align='C')
        self.cell(90, 10, "_________________________", ln=1, align='C')
        self.cell(90, 10, "Firma del Gerente", ln=0, align='C')
        self.cell(90, 10, "Firma del Empleado", ln=1, align='C')

# Función para generar el PDF de la boleta
def generar_pdf_boleta(empleado, boleta):
    pdf = BoletaPDF()
    pdf.add_page()

    # Mes y año actual
    mes = datetime.datetime.now().strftime("%B")
    anio = datetime.datetime.now().year

    # Añadir título y cuerpo de la boleta
    pdf.titulo_boleta(mes, anio)
    pdf.cuerpo_boleta(empleado, boleta)
    pdf.firmas()

    # Guardar el PDF con el nombre del empleado
    pdf_filename = f"boleta_{empleado['codigo']}.pdf"
    pdf.output(pdf_filename)
    print(f"Boleta generada: {pdf_filename}")

# Función para solicitar la información del empleado
def solicitar_datos_empleado():
    codigo = input("Ingrese el código del empleado: ")
    apellidos = input("Ingrese los apellidos del empleado: ")
    nombres = input("Ingrese los nombres del empleado: ")
    dni = input("Ingrese el DNI del empleado: ")
    sueldo_basico = float(input("Ingrese el sueldo básico del empleado: "))
    sistema_pension = input("Ingrese el sistema de pensión (AFP/ONP): ").upper()
    return {
        'codigo': codigo,
        'apellidos': apellidos,
        'nombres': nombres,
        'dni': dni,
        'sueldo_basico': sueldo_basico,
        'sistema_pension': sistema_pension,
    }

# Función para calcular los descuentos y bonificaciones
def calcular_boleta(empleado):
    sueldo_basico = empleado['sueldo_basico']
    
    # Calculando descuentos de pensión (ejemplo 10% AFP, 13% ONP)
    if empleado['sistema_pension'] == 'AFP':
        descuento_pension = sueldo_basico * 0.10
    elif empleado['sistema_pension'] == 'ONP':
        descuento_pension = sueldo_basico * 0.13
    else:
        descuento_pension = 0

    # Calculando bonificación (si es julio o diciembre)
    mes_actual = datetime.datetime.now().month
    bonificacion = sueldo_basico if mes_actual in [7, 12] else 0

    # Sueldo neto
    sueldo_neto = sueldo_basico - descuento_pension + bonificacion

    return {
        'sueldo_basico': sueldo_basico,
        'descuento_pension': descuento_pension,
        'bonificacion': bonificacion,
        'sueldo_neto': sueldo_neto
    }
# Clase para el PDF del reporte estadístico
class ReporteEstadisticoPDF(FPDF):
    def header(self):
        # Encabezado del reporte
        self.set_font("Arial", 'B', 12)
        self.cell(0, 10, "INKAFARMA - Reporte Estadístico", ln=True, align='C')
        self.set_font("Arial", size=10)
        self.cell(0, 10, "RUC: 20547896532", ln=True, align='C')
        self.cell(0, 10, "Dirección: AV LOS PENDEJOS", ln=True, align='C')
        self.ln(10)

    def cuerpo_reporte(self, total_sueldo_neto, promedio_sueldo_neto, max_sueldo_neto, min_sueldo_neto):
        # Cuerpo del reporte estadístico
        self.set_font("Arial", 'B', 10)
        self.cell(0, 10, "Resumen Estadístico de Boletas de Pago", ln=True)
        self.ln(5)

        self.set_font("Arial", size=10)
        self.cell(90, 10, "Total Sueldo Neto", border=1)
        self.cell(0, 10, f"S/. {total_sueldo_neto:.2f}", border=1, ln=True)

        self.cell(90, 10, "Promedio Sueldo Neto", border=1)
        self.cell(0, 10, f"S/. {promedio_sueldo_neto:.2f}", border=1, ln=True)

        self.cell(90, 10, "Sueldo Neto Máximo", border=1)
        self.cell(0, 10, f"S/. {max_sueldo_neto:.2f}", border=1, ln=True)

        self.cell(90, 10, "Sueldo Neto Mínimo", border=1)
        self.cell(0, 10, f"S/. {min_sueldo_neto:.2f}", border=1, ln=True)

# Función para generar el PDF del reporte estadístico
def generar_pdf_reporte_estadistico(boletas):
    total_sueldo_neto = sum(boleta['sueldo_neto'] for boleta in boletas)
    promedio_sueldo_neto = total_sueldo_neto / len(boletas)
    max_sueldo_neto = max(boleta['sueldo_neto'] for boleta in boletas)
    min_sueldo_neto = min(boleta['sueldo_neto'] for boleta in boletas)

    pdf = ReporteEstadisticoPDF()
    pdf.add_page()
    pdf.cuerpo_reporte(total_sueldo_neto, promedio_sueldo_neto, max_sueldo_neto, min_sueldo_neto)

    # Guardar el PDF del reporte estadístico
    pdf_filename = "reporte_estadistico.pdf"
    pdf.output(pdf_filename)
    print(f"Reporte estadístico generado: {pdf_filename}")

# Función principal
def main():
    num_boletas = int(input("Ingrese el número de boletas a generar (entre 3 y 8): "))
    while num_boletas < 3 or num_boletas > 8:
        print("El número de boletas debe estar entre 3 y 8.")
        num_boletas = int(input("Ingrese el número de boletas a generar (entre 3 y 8): "))

    boletas = []

    # Solicitar datos y calcular boletas
    for _ in range(num_boletas):
        empleado = solicitar_datos_empleado()
        boleta = calcular_boleta(empleado)
        generar_pdf_boleta(empleado, boleta)
        boletas.append(boleta)

if __name__ == "__main__":
    main()
