import pandas as pd
import streamlit as st
import re

st.title("Registro de Empleados")

# Paso 1: Ingreso del nombre de la compañía
if "nombre_compania" not in st.session_state:
    st.session_state["nombre_compania"] = ""
    st.session_state["paso"] = 1
    st.session_state["empleados"] = []
    st.session_state["cantidad_empleados"] = 0
    st.session_state["empleados_ingresados"] = 0

if st.session_state["paso"] == 1:
    st.header("Paso 1: Ingrese el nombre de la compañía")
    nombre_compania_input = st.text_input("Nombre de la Compañía")
    if st.button("Continuar"):
        if nombre_compania_input.strip():
            st.session_state["nombre_compania"] = nombre_compania_input.strip()
            st.session_state["paso"] = 2
            st.rerun()
        else:
            st.error("Por favor, ingrese el nombre de la compañía.")

# Paso 2: Ingreso de la cantidad de empleados activos y terminados este año
if st.session_state["paso"] == 2:
    st.header("Paso 2: Ingrese la cantidad de empleados activos y terminados este año")
    cantidad_empleados_w2 = st.number_input("Cantidad de Empleados Directos (W2)", min_value=0, step=1)
    cantidad_contratistas_480 = st.number_input("Cantidad de Contratistas (480)", min_value=0, step=1)

    total_empleados = cantidad_empleados_w2 + cantidad_contratistas_480
    if st.button("Continuar al formulario de empleados"):
        if total_empleados > 0:
            st.session_state["cantidad_empleados"] = total_empleados
            st.session_state["cantidad_empleados_w2"] = cantidad_empleados_w2
            st.session_state["cantidad_contratistas_480"] = cantidad_contratistas_480
            st.session_state["paso"] = 3
            st.rerun()
        else:
            st.error("Por favor, ingrese una cantidad válida de empleados.")

# Paso 3: Formulario de empleados
if st.session_state["paso"] == 3:
    if st.button("⬅️ Volver atrás"):
        st.session_state["paso"] = 2
        st.rerun()
    st.header(f"Paso 3: Ingrese la información de los empleados ({st.session_state['empleados_ingresados']} de {st.session_state['cantidad_empleados']})")
    
    with st.form("form_empleado"):
        tipo_empleado = st.selectbox("Tipo de Empleado", ["Empleado (W2)", "Contratista (480)"])
        ssn = st.text_input("Número de Seguro Social (sin guiones, solo números)")
        ssn = re.sub(r'[^0-9]', '', ssn)  # Elimina cualquier carácter que no sea número
        if len(ssn) == 9:
            ssn = f"{ssn[:3]}-{ssn[3:5]}-{ssn[5:]}"
        apellido_paterno = st.text_input("Apellido Paterno")
        apellido_materno = st.text_input("Apellido Materno (Opcional)")
        nombre = st.text_input("Nombre")
        inicial = st.text_input("Inicial (Opcional)")
        direccion = st.text_input("Dirección")
        pueblo = st.text_input("Pueblo")
        pais = st.text_input("País")
        zip_code = st.text_input("Zip Code")
        fecha_reclutamiento = st.text_input("Fecha de Reclutamiento (MM/DD/YYYY)")
        fecha_nacimiento = st.text_input("Fecha de Nacimiento (MM/DD/YYYY)")
        estatus_marital = st.selectbox("Estatus Marital", ["Soltero", "Casado"])
        genero = st.selectbox("Género", ["Masculino", "Femenino", "No responder"])
        status_empleado = st.selectbox("Status de Empleado", ["Activo", "Terminado"])
        posicion = st.text_input("Posición")
        email_personal = st.text_input("Email Personal")
        email_trabajo = st.text_input("Email del Trabajo (Opcional)")
        balance_enfermedad = st.number_input("Balance de horas por enfermedad (Opcional)", min_value=0, step=1)
        balance_vacaciones = st.number_input("Balance de horas de vacaciones (Opcional)", min_value=0, step=1)
        tipo_paga = st.selectbox("Tipo de Paga", ["Salario", "Hora"])
        cantidad_paga = st.number_input("Cantidad de Paga por Período ($)", min_value=0.0, format="%.2f", step=0.01)
        tipo_cuenta = st.selectbox("Tipo de Cuenta Bancaria", ["Cheque", "Ahorro"])
        numero_ruta = st.text_input("Número de Ruta")
        numero_cuenta = st.text_input("Número de Cuenta del Banco")
        
        if tipo_empleado == "Empleado (W2)":
            dependientes = st.selectbox("Dependientes", ["Selecciona una opción"] + list(range(0, 101)))
            cantidad_retencion = st.selectbox("Retención de Hacienda", ["Selecciona una opción", "25 - Soltero mínima retención", "29 - Casado mitad de retención", "58 - Casado mínima retención", "00 - Casado o Soltero máxima retención"], index=0)
        else:
            dependientes = None
            cantidad_retencion = None
        
        submit = st.form_submit_button("Agregar Empleado")
        
        if submit:
            st.session_state["empleados"].append({
                "Tipo de Empleado": tipo_empleado,
                "Número de Seguro Social": ssn,
                "Apellido Paterno": apellido_paterno,
                "Apellido Materno": apellido_materno,
                "Nombre": nombre,
                "Inicial": inicial,
                "Dirección": direccion,
                "Pueblo": pueblo,
                "País": pais,
                "Zip Code": zip_code,
                "Fecha de Reclutamiento": fecha_reclutamiento,
                "Fecha de Nacimiento": fecha_nacimiento,
                "Estatus Marital": estatus_marital,
                "Dependientes": dependientes,
                "Retención de Hacienda": cantidad_retencion,
                "Género": genero,
                "Status de Empleado": status_empleado,
                "Posición": posicion,
                "Email Personal": email_personal,
                "Email del Trabajo": email_trabajo,
                "Balance de Horas por Enfermedad": balance_enfermedad,
                "Balance de Horas de Vacaciones": balance_vacaciones,
                "Tipo de Paga": tipo_paga,
                "Cantidad de Paga por Período": cantidad_paga,
                "Tipo de Cuenta Bancaria": tipo_cuenta,
                "Número de Ruta": numero_ruta,
                "Número de Cuenta del Banco": numero_cuenta
            })
            st.session_state["empleados_ingresados"] += 1
            if st.session_state["empleados_ingresados"] >= st.session_state["cantidad_empleados"]:
                st.session_state["paso"] = 4
            st.rerun()

# Paso 4: Descargar Excel y reiniciar
if st.session_state["paso"] == 4:
    st.header("Paso 4: Descargar Archivo Excel")
    df = pd.DataFrame(st.session_state["empleados"])
    excel_file = f"{st.session_state['nombre_compania']} Master File.xlsx"
    df.to_excel(excel_file, index=False, engine='openpyxl')
    with open(excel_file, "rb") as f:
        st.download_button("Descargar Archivo Excel", f, file_name=excel_file, mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
    
    if st.button("Comenzar de Nuevo"):
        for key in list(st.session_state.keys()):
            del st.session_state[key]
        st.rerun()
