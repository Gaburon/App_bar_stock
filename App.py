import tkinter as tk
from tkinter import *
from tkinter import messagebox
from tkinter import ttk
from PIL import Image, ImageTk
import json
import locale
from tkinter.simpledialog import askfloat

class InventarioBarApp:

    def __init__(self, root): 
        self.root = root
        self.root.title("Inventario Bar App")
        self.root.geometry('1200x900')
        self.my_tree = ttk.Treeview(root)

        # Cargar la imagen del logo
        ruta_logo = "img/Imagen_logo.png"
        img = Image.open(ruta_logo)
        nuevo_ancho = 250  # Ajusta el ancho deseado
        nuevo_alto = 250  # Ajusta el alto deseado
        img = img.resize((nuevo_ancho, nuevo_alto), Image.BICUBIC)
        self.fondo_image = ImageTk.PhotoImage(img)

        # Crear un label para mostrar la imagen
        self.logo_label = tk.Label(self.root, image=self.fondo_image)
        self.logo_label.place(relx=0.5, rely=0.5, anchor=tk.CENTER)
        # Configurar formato de moneda colombiana (COP)
        locale.setlocale(locale.LC_ALL, 'es_CO.UTF-8')

        # Cargar inventario desde el archivo
        self.inventario = self.cargar_inventario()

        # Cargar ganancias del mes desde el archivo
        self.ganancias_mes_actual = self.cargar_ganancias_mes()
        self.ingresos_totales = self.cargar_ingresos_totales()
        

        # Varibla contador de ganancias
        self.ganancias_venta = 0
        self.ganancias_dia = 0
        self.ganancias_mes = 0

        # Restablecer la posición de los elementos después de agregar la imagen de fondo
        self.configurar_interfaz()

        self.actualizar_ingresos_totales()

        # Interfaz de usuario
    def configurar_interfaz(self):
        # Interfaz de usuario
        self.lbl_header = tk.Label(self.root, text="Manejo Inventario", font=("Arial", 14, "bold"), fg="red")
        self.lbl_header.place(relx=0.17, rely=0.05, anchor=tk.CENTER)

        # Manejo de inventario
        self.lbl_producto = tk.Label(self.root, text="Producto:")
        self.lbl_producto.place(relx=0.1, rely=0.15)

        self.producto_var = tk.StringVar()
        self.cmb_producto = ttk.Combobox(self.root, textvariable=self.producto_var, values=list(self.inventario.keys()))
        self.cmb_producto.place(relx=0.19, rely=0.15)
        self.cmb_producto.bind("<<ComboboxSelected>>", self.actualizar_precios)

        self.lbl_precio_compra = tk.Label(self.root, text="Precio de Compra:")
        self.lbl_precio_compra.place(relx=0.1, rely=0.20)

        self.precio_compra_var = tk.StringVar()
        self.entry_precio_compra = tk.Entry(self.root, textvariable=self.precio_compra_var)
        self.entry_precio_compra.place(relx=0.2, rely=0.20)

        self.lbl_precio_venta = tk.Label(self.root, text="Precio de Venta:")
        self.lbl_precio_venta.place(relx=0.1, rely=0.25)

        self.precio_venta_var = tk.StringVar()
        self.entry_precio_venta = tk.Entry(self.root, textvariable=self.precio_venta_var)
        self.entry_precio_venta.place(relx=0.2, rely=0.25)

        # Actualizar inventario
        self.btn_update_inventario = tk.Button(self.root, text="Actualizar inventario", command=self.actualizar_inventario)
        self.btn_update_inventario.place(relx=0.15, rely=0.4, anchor=tk.CENTER)

        # Borrar item inventario
        self.btn_borrar_item = tk.Button(self.root, text="Borrar Objeto del inventario", command=self.borrar_item)
        self.btn_borrar_item.place(relx=0.27, rely=0.4, anchor=tk.CENTER)

        # Nuevos campos para cantidad de stock
        self.lbl_cantidad_stock = tk.Label(self.root, text="Cantidad de Stock:")
        self.lbl_cantidad_stock.place(relx=0.1, rely=0.30)

        self.cantidad_stock_var = tk.StringVar()
        self.entry_cantidad_stock = tk.Entry(self.root, textvariable=self.cantidad_stock_var)
        self.entry_cantidad_stock.place(relx=0.2, rely=0.30)

        self.btn_agregar_stock = tk.Button(self.root, text="Agregar Stock", command=self.agregar_stock)
        self.btn_agregar_stock.place(relx=0.24, rely=0.5, anchor=tk.CENTER)

        self.btn_agregar_producto = tk.Button(self.root, text="Agregar Producto", command=self.agregar_producto)
        self.btn_agregar_producto.place(relx=0.15, rely=0.5, anchor=tk.CENTER)

        # GANANCIAS MESSSSSSS
        self.lbl_ganancias_mes_actual = tk.Label(self.root, text=f"Ganancias: {locale.currency(int(self.ganancias_mes_actual), grouping=True, symbol=False)}")
        self.lbl_ganancias_mes_actual.place(relx=0.2, rely=0.8, anchor=tk.CENTER)

        # Etiqueta para mostrar ingresos totales
        self.lbl_ingresos_totales = tk.Label(self.root, text=f"Ingresos totales: {locale.currency(int(self.ingresos_totales), grouping=True, symbol=False)}")
        self.lbl_ingresos_totales.place(relx=0.2, rely=0.75, anchor=tk.CENTER)

        self.btn_limpiar_registro_mes = tk.Button(self.root, text="Limpiar Registro", command=self.limpiar_registro_mes)
        self.btn_limpiar_registro_mes.place(relx=0.2, rely=0.85, anchor=tk.CENTER)

        # Interfaz de ventas
        self.lbl_header_ventas = tk.Label(self.root, text="Ventas", font=("Arial", 14, "bold"), fg="red")
        self.lbl_header_ventas.place(relx=0.8, rely=0.05, anchor=tk.CENTER)

        #1
        self.lbl_producto_venta1 = tk.Label(self.root, text="Producto de venta 1:")
        self.lbl_producto_venta1.place(relx=0.48, rely=0.15)

        self.producto_venta1_var = tk.StringVar()
        self.cmb_producto_venta1 = ttk.Combobox(self.root, textvariable=self.producto_venta1_var, values=list(self.inventario.keys()))
        self.cmb_producto_venta1.place(relx=0.58, rely=0.15)
        self.cmb_producto_venta1.bind("<<ComboboxSelected>>", self.actualizar_precios)

        self.lbl_cantidad_venta1 = tk.Label(self.root, text="Cantidad:")
        self.lbl_cantidad_venta1.place(relx=0.7, rely=0.15)

        self.cantidad_venta1_var = tk.StringVar()
        self.entry_cantidad_venta1 = tk.Entry(self.root, textvariable=self.cantidad_venta1_var)
        self.entry_cantidad_venta1.place(relx=0.75, rely=0.15)

        # 2
        self.lbl_producto_venta2 = tk.Label(self.root, text="Producto de venta 2:")
        self.lbl_producto_venta2.place(relx=0.48, rely=0.20)

        self.producto_venta2_var = tk.StringVar()
        self.cmb_producto_venta2 = ttk.Combobox(self.root, textvariable=self.producto_venta2_var, values=list(self.inventario.keys()))
        self.cmb_producto_venta2.place(relx=0.58, rely=0.20)
        self.cmb_producto_venta2.bind("<<ComboboxSelected>>", self.actualizar_precios)

        self.lbl_cantidad_venta2 = tk.Label(self.root, text="Cantidad:")
        self.lbl_cantidad_venta2.place(relx=0.7, rely=0.20)

        self.cantidad_venta2_var = tk.StringVar()
        self.entry_cantidad_venta2 = tk.Entry(self.root, textvariable=self.cantidad_venta2_var)
        self.entry_cantidad_venta2.place(relx=0.75, rely=0.20)
        # 3
        self.lbl_producto_venta3 = tk.Label(self.root, text="Producto de venta 3:")
        self.lbl_producto_venta3.place(relx=0.48, rely=0.25)

        self.producto_venta3_var = tk.StringVar()
        self.cmb_producto_venta3 = ttk.Combobox(self.root, textvariable=self.producto_venta3_var, values=list(self.inventario.keys()))
        self.cmb_producto_venta3.place(relx=0.58, rely=0.25)
        self.cmb_producto_venta3.bind("<<ComboboxSelected>>", self.actualizar_precios)

        self.lbl_cantidad_venta3 = tk.Label(self.root, text="Cantidad:")
        self.lbl_cantidad_venta3.place(relx=0.7, rely=0.25)

        self.cantidad_venta3_var = tk.StringVar()
        self.entry_cantidad_venta3 = tk.Entry(self.root, textvariable=self.cantidad_venta3_var)
        self.entry_cantidad_venta3.place(relx=0.75, rely=0.25)

        # 4
        self.lbl_producto_venta4 = tk.Label(self.root, text="Producto de venta 4:")
        self.lbl_producto_venta4.place(relx=0.48, rely=0.30)

        self.producto_venta4_var = tk.StringVar()
        self.cmb_producto_venta4 = ttk.Combobox(self.root, textvariable=self.producto_venta4_var, values=list(self.inventario.keys()))
        self.cmb_producto_venta4.place(relx=0.58, rely=0.30)
        self.cmb_producto_venta4.bind("<<ComboboxSelected>>", self.actualizar_precios)

        self.lbl_cantidad_venta4 = tk.Label(self.root, text="Cantidad:")
        self.lbl_cantidad_venta4.place(relx=0.7, rely=0.30)

        self.cantidad_venta4_var = tk.StringVar()
        self.entry_cantidad_venta4 = tk.Entry(self.root, textvariable=self.cantidad_venta4_var)
        self.entry_cantidad_venta4.place(relx=0.75, rely=0.30)

        self.btn_registrar_venta = tk.Button(self.root, text="Registrar Venta", command=self.registrar_venta)
        self.btn_registrar_venta.place(relx=0.8, rely=0.45)

        # Mostrar inventario
        style = ttk.Style()

        style.configure("Treeview.Heading", font=('Arial bold', 15))
        style.configure("Vertical.TScrollbar", width=40)

        self.my_tree['columns'] = ("Nombre", "Precio", "Cantidad")
        self.my_tree.column("#0", width=0, stretch=tk.NO)
        self.my_tree.column("Nombre", anchor=tk.W, width=200)
        self.my_tree.column("Precio", anchor=tk.W, width=150)
        self.my_tree.column("Cantidad", anchor=tk.W, width=150)

        self.my_tree.heading("Nombre", text="Nombre", anchor=tk.W)
        self.my_tree.heading("Precio", text="Precio", anchor=tk.W)
        self.my_tree.heading("Cantidad", text="Cantidad", anchor=tk.W)
        scrollbar = ttk.Scrollbar(self.root, orient="vertical", command=self.my_tree.yview, style="Vertical.TScrollbar")
        scrollbar.place(relx=0.90, rely=0.8, anchor=tk.CENTER)

        self.mostrar_inventario()
        self.my_tree.tag_configure('orow', background="#EEEEEE", font=('Arial bold', 15))
        self.my_tree.place(relx=0.7, rely=0.8, anchor=tk.CENTER)

        self.my_tree.heading("Nombre", text="Nombre", anchor=tk.W, command=lambda:
                             self.organizar_nombres(self.my_tree, "Nombre", False))

        # Guardar inventario y ganancias del mes al cerrar la aplicación
        root.protocol("WM_DELETE_WINDOW", self.guardar_inventario_y_ganancias_mes_al_cerrar)

    def borrar_item(self):
        producto = self.producto_var.get()

        if producto not in self.inventario:
            messagebox.showerror("Error", "verifica que el producto este en el inventario.")
        else:
            del self.inventario[producto]

        self.mostrar_inventario()
        self.cargar_inventario()

    def actualizar_inventario(self):
        producto = self.producto_var.get()

        precio_venta = self.precio_venta_var.get()
        precio_compra = self.precio_compra_var.get()

        try:
            stock = int(self.cantidad_stock_var.get())
        except ValueError:
            stock = self.inventario[producto]["stock"]

        if producto not in self.inventario:
            messagebox.showerror("Error", "verifica que el producto este en el inventario.")
        else:
            self.inventario[producto]["stock"] = stock
            self.inventario[producto]["precio_venta"] = precio_venta
            self.inventario[producto]["precio_compra"] = precio_compra
            
        self.mostrar_inventario()

    def organizar_nombres(self, tv, col, reverse):
        l = [(tv.set(k, col), k) for k in tv.get_children('')]
        l.sort(reverse = reverse)

        for index, (val, k) in enumerate(l):
            tv.move(k, '', index)
        
        tv.heading(col, command = lambda: self.organizar_nombres(tv, col, not reverse))
        
    def limpiar_registro_mes(self):
        self.ganancias_mes_actual = 0
        self.ingresos_totales = 0

        # Actualizar las etiquetas correspondientes
        self.lbl_ganancias_mes_actual.config(text=f"Ganancias: {locale.currency(int(self.ganancias_mes_actual), grouping=True, symbol=False)}")
        self.lbl_ingresos_totales.config(text=f"Ingresos totales: {locale.currency(int(self.ingresos_totales), grouping=True, symbol=False)}")

        # Guardar las actualizaciones
        self.guardar_ganancias_mes()
        self.guardar_ingresos_totales()

    def cargar_ganancias_mes(self):
        try:
            with open("ganancias_mes.json", "r") as file:
                ganancias_mes = json.load(file)
            return ganancias_mes.get("ganancias_mes_actual", 0)
        except FileNotFoundError:
            return 0
        except json.JSONDecodeError:
            messagebox.showerror("Error", "Error al cargar las ganancias del mes desde el archivo.")
            return 0

    def cargar_ingresos_totales(self):
        try:
            with open("ingresos_totales.json", "r") as file:
                ingresos_totales = json.load(file)
            return ingresos_totales.get("ingresos_totales", 0)
        except FileNotFoundError:
            return 0
        except json.JSONDecodeError:
            messagebox.showerror("Error", "Error al cargar los ingresos totales desde el archivo.")
            return 0
    def guardar_ingresos_totales(self):
        try:
            with open("ingresos_totales.json", "w") as file:
                json.dump({"ingresos_totales": self.ingresos_totales}, file)
        except Exception as e:
            messagebox.showerror("Error", f"Error al guardar los ingresos totales: {str(e)}")

    def actualizar_ingresos_totales(self):
        self.lbl_ingresos_totales.config(text=f"Ingresos totales: {locale.currency(int(self.ingresos_totales), grouping=True, symbol=False)}")
        self.guardar_ingresos_totales()

    def guardar_ganancias_mes(self):
        try:
            with open("ganancias_mes.json", "w") as file:
                json.dump({"ganancias_mes_actual": self.ganancias_mes_actual}, file)
        except Exception as e:
            messagebox.showerror("Error", f"Error al guardar las ganancias del mes: {str(e)}")

    def actualizar_precios(self, event):
        producto_seleccionado = self.producto_var.get()
        if producto_seleccionado in self.inventario:
            precio_compra = self.inventario[producto_seleccionado]["precio_compra"]
            precio_venta = self.inventario[producto_seleccionado]["precio_venta"]

            self.precio_compra_var.set(str(precio_compra))
            self.precio_venta_var.set(str(precio_venta))

        self.mostrar_inventario()
            
    def registrar_venta(self):
        producto1 = self.producto_venta1_var.get()
        producto2 = self.producto_venta2_var.get()
        producto3 = self.producto_venta3_var.get()
        producto4 = self.producto_venta4_var.get()
        total_valor_producto1 = total_compra_producto1 = 0
        total_valor_producto2 = total_compra_producto2 = 0
        total_valor_producto3 = total_compra_producto3 = 0
        total_valor_producto4 = total_compra_producto4 = 0

        try:
            venta1 = int(self.entry_cantidad_venta1.get())

        except ValueError:
            venta1 = 0
        
        try:
            venta2 = int(self.entry_cantidad_venta2.get())

        except ValueError:
            venta2 = 0
        
        try:
            venta3 = int(self.entry_cantidad_venta3.get())

        except ValueError:
            venta3 = 0
        
        try:
            venta4 = int(self.entry_cantidad_venta4.get())

        except ValueError:
            venta4 = 0
        
        if producto1 not in self.inventario:
            producto1 = ""
            stock1 = -100
        else:
            stock1 = self.inventario[producto1]["stock"]


        if producto2 not in self.inventario:
            producto2 = ""
            stock2 = -100
        else:
            stock2 = self.inventario[producto2]["stock"]

        if producto3 not in self.inventario:
            producto3 = ""
            stock3 = -100
        else:
            stock3 = self.inventario[producto3]["stock"]
        
        if producto4 not in self.inventario:
            producto4 = ""
            stock4 = -100
        else: 
            stock4 = self.inventario[producto4]["stock"]

        # Verificación y ajuste del stock para venta1
        if venta1 > stock1 and stock1 != -100:
            messagebox.showerror("Error", f"No hay suficientes unidades de {producto1} en el inventario.")
            return

        if stock1 != -100:
            valor_producto1 = float(self.inventario[producto1]["precio_venta"])
            compra_producto1 = float(self.inventario[producto1]["precio_compra"])
            total_compra_producto1 = compra_producto1 * venta1
            total_valor_producto1 = valor_producto1 * venta1

        # Verificación y ajuste del stock para venta2
        if venta2 > stock2 and stock2 != -100:
            messagebox.showerror("Error", f"No hay suficientes unidades de {producto2} en el inventario.")
            return

        if stock2 != -100:
            valor_producto2 = float(self.inventario[producto2]["precio_venta"])
            compra_producto2 = float(self.inventario[producto2]["precio_compra"])
            total_compra_producto2 = compra_producto2 * venta2
            total_valor_producto2 = valor_producto2 * venta2

        # Verificación y ajuste del stock para venta3
        if venta3 > stock3 and stock3 != -100:
            messagebox.showerror("Error", f"No hay suficientes unidades de {producto3} en el inventario.")
            return

        if stock3 != -100:
            valor_producto3 = float(self.inventario[producto3]["precio_venta"])
            compra_producto3 = float(self.inventario[producto3]["precio_compra"])
            total_compra_producto3 = compra_producto3 * venta3
            total_valor_producto3 = valor_producto3 * venta3

        # Verificación y ajuste del stock para venta4
        if venta4 > stock4 and stock4 != -100:
            messagebox.showerror("Error", f"No hay suficientes unidades de {producto4} en el inventario.")
            return

        if stock4 != -100:
            valor_producto4 = float(self.inventario[producto4]["precio_venta"])
            compra_producto4 = float(self.inventario[producto4]["precio_compra"])
            total_compra_producto4 = compra_producto4 * venta4
            total_valor_producto4 = valor_producto4 * venta4

        ingresos_totales_total = total_valor_producto1 + total_valor_producto2 + total_valor_producto3 + total_valor_producto4
        costos_total = total_compra_producto1 +  total_compra_producto2 +  total_compra_producto3 +  total_compra_producto4

        ganancia_total = ingresos_totales_total - costos_total

        ganancias_venta = ganancia_total

        self.ganancias_mes_actual += ganancias_venta

        self.ingresos_totales += ingresos_totales_total
        # Obtener el monto con el que se va a pagar
        monto_pagado = askfloat("Pago", "Ingrese el monto con el que se va a pagar:")
        
        if monto_pagado is None or monto_pagado < ingresos_totales_total:
            # Mostrar mensaje de pago insuficiente y no realizar la venta
            messagebox.showerror("Pago Insuficiente", "El monto pagado no es suficiente. No se registrará la venta.")
            return

        # Calcular el cambio
        cambio = monto_pagado - ingresos_totales_total

        # Modificar el inventario después de verificar el pago
        for producto, cantidad_vendida in zip([producto1, producto2, producto3, producto4], [venta1, venta2, venta3, venta4]):
            if producto != "" and producto in self.inventario:
                self.inventario[producto]["stock"] -= cantidad_vendida
        # Restablecer los campos de cantidad
        self.cantidad_venta1_var.set("")  
        self.cantidad_venta2_var.set("")  
        self.cantidad_venta3_var.set("")  
        self.cantidad_venta4_var.set("")  

        # Actualizar etiqueta de ganancias del mes actual con formato de moneda colombiana
        self.actualizar_ingresos_totales()
        self.lbl_ganancias_mes_actual.config(text=f"Ganancias: {locale.currency(int(self.ganancias_mes_actual), grouping=True, symbol=False)}")
        
        # Mostrar mensaje de venta registrada
        messagebox.showinfo("Venta Registrada", f"Cobrar : {locale.currency(int(ingresos_totales_total), grouping=True, symbol=False)}\n"
        f"Cambio : {locale.currency(int(cambio), grouping=True, symbol=False)}\n"
        f"Ganancia : {locale.currency(int(ganancia_total), grouping=True, symbol=False)}")

        self.mostrar_inventario()

    def agregar_stock(self):
        producto = self.producto_var.get()
        cantidad_stock = self.cantidad_stock_var.get()

        try:
            cantidad_stock = int(cantidad_stock)
            if cantidad_stock <= 0:
                raise ValueError("La cantidad de stock debe ser un número positivo.")
        except ValueError as e:
            messagebox.showerror("Error", f"Error en la cantidad de stock: {str(e)}")
            return

        if producto in self.inventario:
            self.inventario[producto]["stock"] += cantidad_stock
            messagebox.showinfo("Stock Actualizado", f"Se agregaron {cantidad_stock} unidades de {producto} al stock.")
        else:
            messagebox.showerror("Error", "Producto no encontrado en el inventario.")
        
        self.mostrar_inventario()

    def agregar_producto(self):
        producto = self.producto_var.get()
        if producto not in self.inventario:
            try:
                precio_compra = float(self.precio_compra_var.get().replace('$', '').replace(',', ''))
                precio_venta = float(self.precio_venta_var.get().replace('$', '').replace(',', ''))
                if precio_compra < 0 or precio_venta < 0:
                    raise ValueError("Los precios deben ser números no negativos.")
            except ValueError as e:
                messagebox.showerror("Error", f"Error en los precios: {str(e)}")
                return

            self.inventario[producto] = {"precio_compra": precio_compra, "precio_venta": precio_venta, "stock": 0}
            messagebox.showinfo("Producto Agregado", f"Se ha agregado el producto: {producto}")
            self.cmb_producto['values'] = list(self.inventario.keys())  # Actualizar las opciones del Combobox
        else:
            messagebox.showerror("Error", "El producto ya existe en el inventario.")
        
        self.mostrar_inventario()

    def cargar_inventario(self):
        try:
            with open("inventario.json", "r") as file:
                inventario = json.load(file)
            print("Loaded Inventory:")
            for producto, detalles in inventario.items():
                print(f"Producto: {producto}, Detalles: {detalles}")
            return inventario
        except FileNotFoundError:
            print("FileNotFoundError: 'inventario.json' not found.")
            return {}
        except json.JSONDecodeError:
            print("JSONDecodeError: Error decoding 'inventario.json'.")
            messagebox.showerror("Error", "Error al cargar el inventario desde el archivo.")
            return {}

    def guardar_inventario(self):
        with open("inventario.json", "w") as file:
            json.dump(self.inventario, file)
        self.mostrar_inventario()

    def guardar_inventario_y_ganancias_mes_al_cerrar(self):
        self.guardar_inventario()
        self.guardar_ganancias_mes()
        self.guardar_ingresos_totales()
        self.root.destroy()

    def mostrar_inventario(self):
        for item in self.my_tree.get_children():
            self.my_tree.delete(item)

        print("Current Inventory:", self.inventario)

        for producto_seleccionado, values in self.inventario.items():
            precio_venta = values["precio_venta"]
            stock = values["stock"]

            precio_venta_int = int(''.join(filter(str.isdigit, str(precio_venta))))

            self.my_tree.insert("", "end", values=(producto_seleccionado, int(precio_venta), stock), tags=('orow'))
    
if __name__ == "__main__":
    try:
        root = tk.Tk()
        app = InventarioBarApp(root)
        root.mainloop()
    except Exception as e:
        messagebox.showerror("Error", f"Error inesperado: {str(e)}")