import reflex as rx
from rxconfig import config

import json
import mi_crypto_lib as cripto

class State(rx.State):
    # CRR
    n_crr: str = ""
    crr_elements: list[int] = []
    crr_elements_str: str = ""
    crr_length: str = ""
    phi_theoretical: str = ""
    crr_verified: str = ""
    
    # RSA
    inicio_p: str = ""
    inicio_q: str = ""
    rsa_p: str = ""
    rsa_q: str = ""
    rsa_n: str = ""
    rsa_phi: str = ""

    # Inversos
    inv_a: str = ""
    inv_n: str = ""
    inv_res_euler: str = ""
    inv_res_ext: str = ""
    inv_verif: str = ""

    def set_n_crr(self, val: str):
        self.n_crr = val

    def set_inicio_p(self, val: str):
        self.inicio_p = val

    def set_inicio_q(self, val: str):
        self.inicio_q = val

    def set_inv_a(self, val: str):
        self.inv_a = val

    def set_inv_n(self, val: str):
        self.inv_n = val

    # Hill
    hill_plano: str = ""
    hill_cifrado: str = ""
    hill_n: str = ""
    hill_matriz_res: str = ""
    hill_verif: str = ""

    def set_hill_plano(self, val: str):
        self.hill_plano = val
        
    def set_hill_cifrado(self, val: str):
        self.hill_cifrado = val
        
    def set_hill_n(self, val: str):
        self.hill_n = val

    # Autoclave
    autoc_plano: str = ""
    autoc_clave: str = ""
    autoc_cifrado: str = ""
    autoc_descifrado: str = ""
    autoc_kasiski_res: str = ""

    def set_autoc_plano(self, val: str):
        self.autoc_plano = val
        
    def set_autoc_clave(self, val: str):
        self.autoc_clave = val

    def calculate_autoc(self):
        if not self.autoc_plano or not self.autoc_clave:
            self.autoc_cifrado = "Ingrese texto y clave"
            self.autoc_descifrado = ""
            self.autoc_kasiski_res = ""
            return
            
        try:
            # Cifrar y descifrar
            self.autoc_cifrado = cripto.cifrar_autoclave(self.autoc_plano, self.autoc_clave)
            self.autoc_descifrado = cripto.descifrar_autoclave(self.autoc_cifrado, self.autoc_clave)
            
            # Kasiski sobre el cifrado
            res_kasiski = cripto.kasiski(self.autoc_cifrado)
            self.autoc_kasiski_res = json.dumps(res_kasiski, indent=2, ensure_ascii=False)
        except Exception as e:
            self.autoc_cifrado = f"Error: {str(e)}"
            self.autoc_descifrado = ""
            self.autoc_kasiski_res = ""

    # n Genérico
    ngen_val: str = ""
    ngen_factores_str: str = ""
    ngen_phi_val: str = ""
    ngen_error: str = ""

    def set_ngen_val(self, val: str):
        self.ngen_val = val

    def calculate_ngen(self):
        try:
            n = int(self.ngen_val)
            if n <= 0:
                self.ngen_error = "Error: n debe ser un entero positivo"
                self.ngen_factores_str = ""
                self.ngen_phi_val = ""
                return
            
            factores = cripto.factorizar(n)
            if factores:
                self.ngen_factores_str = " × ".join([f"{p}^{e}" for p, e in factores.items()])
            else:
                self.ngen_factores_str = f"{n} es 1 (no tiene factores primos)"
                
            self.ngen_phi_val = str(cripto.euler_phi(n))
            self.ngen_error = ""
        except ValueError:
            self.ngen_error = "Error: Ingrese un número válido"
            self.ngen_factores_str = ""
            self.ngen_phi_val = ""

    def calculate_crr(self):
        try:
            n = int(self.n_crr)
            if n < 2:
                self.crr_verified = "Error: n debe ser mayor o igual a 2"
                return
            elements = cripto.calcular_crr(n)
            phi_val = cripto.phi(n)
            
            self.crr_elements = elements
            self.crr_elements_str = "{" + ", ".join(str(e) for e in elements) + "}"
            self.crr_length = str(len(elements))
            self.phi_theoretical = str(phi_val)
            self.crr_verified = " Coincide exactamente" if len(elements) == phi_val else "❌ No coincide"
        except ValueError:
            self.crr_verified = "Error: Ingrese un número válido."
            self.crr_elements = []
            self.crr_elements_str = ""
            self.crr_length = ""
            self.phi_theoretical = ""

    def calculate_rsa(self):
        try:
            ini_p = int(self.inicio_p)
            ini_q = int(self.inicio_q)
            
            p = cripto.generar_primo_seguro(ini_p)
            q = cripto.generar_primo_seguro(ini_q)
            
            # Asegurar que p y q no sean el mismo primo
            if p == q:
                q = cripto.generar_primo_seguro(p + 1)
                
            n = p * q
            phi_val = (p - 1) * (q - 1)
            
            self.rsa_p = str(p)
            self.rsa_q = str(q)
            self.rsa_n = str(n)
            self.rsa_phi = str(phi_val)
        except ValueError:
            self.rsa_p = "Error"
            self.rsa_q = "Error"
            self.rsa_n = ""
            self.rsa_phi = ""

    def calculate_inversos(self):
        try:
            a = int(self.inv_a)
            n = int(self.inv_n)
            
            res_euler = cripto.inverso_euler(a, n)
            res_ext = cripto.inverso_extendido(a, n)
            
            # Compatibilidad si las funciones devuelven directamente el entero
            if isinstance(res_euler, int) or isinstance(res_ext, int):
                self.inv_res_euler = str(res_euler)
                self.inv_res_ext = str(res_ext)
                self.inv_verif = " Calculado"
                return
            
            if isinstance(res_euler, dict) and "error" in res_euler:
                self.inv_res_euler = res_euler["error"]
                self.inv_res_ext = res_ext.get("error", "Error") if isinstance(res_ext, dict) else "Error"
                self.inv_verif = "❌ No existe inverso"
            else:
                self.inv_res_euler = str(res_euler.get("inverso", res_euler)) if isinstance(res_euler, dict) else str(res_euler)
                self.inv_res_ext = str(res_ext.get("inverso", res_ext)) if isinstance(res_ext, dict) else str(res_ext)
                self.inv_verif = " Verificado (a*i ≡ 1 mod n)"
        except ValueError:
            self.inv_res_euler = "Error"
            self.inv_res_ext = "Error"
            self.inv_verif = "Ingrese números válidos"

    def calculate_hill(self):
        try:
            n = int(self.hill_n)
            if n < 2:
                self.hill_verif = "Error: n debe ser mayor o igual a 2"
                return
            
            matriz_clave = cripto.CifradoMatriz.recuperar_clave(self.hill_plano, self.hill_cifrado, n)
            self.hill_matriz_res = matriz_clave.to_string()
            self.hill_verif = "Clave encontrada exitosamente"
        except Exception as e:
            self.hill_matriz_res = ""
            self.hill_verif = f"Error: {str(e)}"



# Componentes UI
def crr_card():
    return rx.card(
        rx.vstack(
            rx.heading("1. Conjunto Reducido de Residuos", size="5", color="var(--accent-9)"),
            rx.text("Ingrese el módulo n para calcular el CRR y verificar con la función de Euler φ(n).", size="2"),
            rx.hstack(
                rx.input(placeholder="Módulo n", value=State.n_crr, on_change=State.set_n_crr),
                rx.button("Calcular CRR", on_click=State.calculate_crr, variant="solid"),
                width="100%"
            ),
            rx.divider(),
            rx.hstack(
                rx.text("Elementos CRR(n): ", weight="bold"),
                rx.code(State.crr_elements_str)
            ),
            rx.hstack(
                rx.hstack(rx.text("Cantidad real: ", weight="bold"), rx.badge(State.crr_length, color_scheme="blue")),
                rx.hstack(rx.text("φ(n) teórico: ", weight="bold"), rx.badge(State.phi_theoretical, color_scheme="green")),
                spacing="4"
            ),
            rx.hstack(rx.text("Verificación: ", weight="bold"), rx.text(State.crr_verified)),
            align_items="start",
            spacing="3",
        ),
        variant="surface",
        padding="6",
        width="100%",
        border_radius="15px",
        background="rgba(255, 255, 255, 0.03)",
        backdrop_filter="blur(15px)",
        box_shadow="0 8px 32px 0 rgba(0, 0, 0, 0.37)",
        border="1px solid rgba(255, 255, 255, 0.08)"
    )

def rsa_card():
    return rx.card(
        rx.vstack(
            rx.heading("2. Base de RSA (Primos Seguros)", size="5", color="var(--accent-9)"),
            rx.text("Ingrese semillas numéricas para buscar primos seguros p y q, y calcular n y φ(n).", size="2"),
            rx.hstack(
                rx.input(placeholder="p", value=State.inicio_p, on_change=State.set_inicio_p),
                rx.input(placeholder="q", value=State.inicio_q, on_change=State.set_inicio_q),
                rx.button("Generar RSA", on_click=State.calculate_rsa, variant="solid"),
                width="100%"
            ),
            rx.divider(),
            rx.hstack(
                rx.hstack(rx.text("Primo Seguro p: ", weight="bold"), rx.badge(State.rsa_p, color_scheme="iris")),
                rx.hstack(rx.text("Primo Seguro q: ", weight="bold"), rx.badge(State.rsa_q, color_scheme="iris")),
                spacing="4"
            ),
            rx.hstack(rx.text("Módulo n (p*q): ", weight="bold"), rx.code(State.rsa_n, color="var(--accent-11)")),
            rx.hstack(rx.text("φ(n) rápida (p-1)*(q-1): ", weight="bold"), rx.code(State.rsa_phi, color="var(--accent-11)")),
            align_items="start",
            spacing="3",
        ),
        variant="surface",
        padding="6",
        width="100%",
        border_radius="15px",
        background="rgba(255, 255, 255, 0.03)",
        backdrop_filter="blur(15px)",
        box_shadow="0 8px 32px 0 rgba(0, 0, 0, 0.37)",
        border="1px solid rgba(255, 255, 255, 0.08)"
    )

def inversos_card():
    return rx.card(
        rx.vstack(
            rx.heading("4. Inversos Multiplicativos", size="5", color="var(--accent-9)"),
            rx.text("Calcule el inverso de 'a' módulo 'n' usando dos métodos diferentes.", size="2"),
            rx.hstack(
                rx.input(placeholder="Valor a", value=State.inv_a, on_change=State.set_inv_a),
                rx.input(placeholder="Módulo n", value=State.inv_n, on_change=State.set_inv_n),
                rx.button("Calcular", on_click=State.calculate_inversos, variant="solid"),
                width="100%"
            ),
            rx.divider(),
            rx.grid(
                rx.vstack(
                    rx.text("Método Euler", weight="bold", size="2"),
                    rx.badge(State.inv_res_euler, color_scheme="blue", size="3"),
                    align_items="center",
                ),
                rx.vstack(
                    rx.text("Euclides Extendido", weight="bold", size="2"),
                    rx.badge(State.inv_res_ext, color_scheme="green", size="3"),
                    align_items="center",
                ),
                columns="2",
                spacing="4",
                width="100%",
            ),
            rx.hstack(
                rx.text("Estado: ", weight="bold"),
                rx.text(State.inv_verif),
            ),
            align_items="start",
            spacing="3",
        ),
        variant="surface",
        padding="6",
        width="100%",
        border_radius="15px",
        background="rgba(255, 255, 255, 0.03)",
        backdrop_filter="blur(15px)",
        box_shadow="0 8px 32px 0 rgba(0, 0, 0, 0.37)",
        border="1px solid rgba(255, 255, 255, 0.08)"
    )

def ngen_card():
    return rx.card(
        rx.vstack(
            rx.heading("3. Algoritmo para n Genérico", size="5", color="var(--accent-9)"),
            rx.text("Ingrese un número n para factorizarlo y calcular su función φ(n) de Euler.", size="2"),
            rx.hstack(
                rx.input(placeholder="Valor de n", value=State.ngen_val, on_change=State.set_ngen_val),
                rx.button("Calcular", on_click=State.calculate_ngen, variant="solid"),
                width="100%"
            ),
            rx.divider(),
            rx.hstack(
                rx.text("Factorización: ", weight="bold"),
                rx.code(State.ngen_factores_str, color="var(--accent-11)"),
            ),
            rx.hstack(
                rx.text("φ(n): ", weight="bold"),
                rx.badge(State.ngen_phi_val, color_scheme="green", size="3"),
            ),
            rx.cond(
                State.ngen_error != "",
                rx.text(State.ngen_error, color="red")
            ),
            align_items="start",
            spacing="3",
        ),
        variant="surface",
        padding="6",
        width="100%",
        border_radius="15px",
        background="rgba(255, 255, 255, 0.03)",
        backdrop_filter="blur(15px)",
        box_shadow="0 8px 32px 0 rgba(0, 0, 0, 0.37)",
        border="1px solid rgba(255, 255, 255, 0.08)"
    )



def autoc_card():
    return rx.card(
        rx.vstack(
            rx.heading("5. Sistema de Cifra Autoclave", size="5", color="var(--accent-9)"),
            rx.text("Cifrado Vigenère de Clave Continua y análisis Kasiski.", size="2"),
            rx.hstack(
                rx.text_area(placeholder="Mensaje a cifrar", value=State.autoc_plano, on_change=State.set_autoc_plano, width="100%", height="100px"),
                rx.vstack(
                    rx.input(placeholder="Clave inicial", value=State.autoc_clave, on_change=State.set_autoc_clave),
                    rx.button("Ejecutar", on_click=State.calculate_autoc, variant="solid", width="100%"),
                    width="200px"
                ),
                width="100%",
                align_items="start"
            ),
            rx.divider(),
            rx.grid(
                rx.vstack(
                    rx.text("Texto Cifrado:", weight="bold"),
                    rx.text_area(value=State.autoc_cifrado, read_only=True, width="100%", height="100px"),
                    rx.text("Texto Descifrado:", weight="bold"),
                    rx.text_area(value=State.autoc_descifrado, read_only=True, width="100%", height="100px"),
                    width="100%",
                ),
                rx.vstack(
                    rx.text("Análisis Kasiski (Ineficaz por falta de periodo):", weight="bold"),
                    rx.text(
                        State.autoc_kasiski_res,
                        style={"white_space": "pre", "font_family": "monospace", "background": "rgba(0,0,0,0.2)", "padding": "10px", "border_radius": "5px", "width": "100%", "height": "230px", "overflow_y": "auto"}
                    ),
                    width="100%",
                ),
                columns="2",
                spacing="4",
                width="100%",
            ),
            align_items="start",
            spacing="3",
        ),
        variant="surface",
        padding="6",
        width="100%",
        border_radius="15px",
        background="rgba(255, 255, 255, 0.03)",
        backdrop_filter="blur(15px)",
        box_shadow="0 8px 32px 0 rgba(0, 0, 0, 0.37)",
        border="1px solid rgba(255, 255, 255, 0.08)"
    )

def gauss_card():
    return rx.card(
        rx.vstack(
            rx.heading("6. Ataque de Gauss-Jordan contra Hill", size="5", color="var(--accent-9)"),
            rx.text("Ataque de texto conocido para recuperar la matriz clave de Hill.", size="2"),
            rx.hstack(
                rx.input(placeholder="Texto Plano", value=State.hill_plano, on_change=State.set_hill_plano),
                rx.input(placeholder="Texto Cifrado", value=State.hill_cifrado, on_change=State.set_hill_cifrado),
                rx.input(placeholder="Dimensión n", value=State.hill_n, on_change=State.set_hill_n, width="120px"),
                rx.button("Ejecutar Ataque", on_click=State.calculate_hill, variant="solid"),
                width="100%"
            ),
            rx.divider(),
            rx.text("Matriz Clave Recuperada:", weight="bold"),
            rx.text(
                State.hill_matriz_res, 
                style={"white_space": "pre", "font_family": "monospace", "background": "rgba(0,0,0,0.2)", "padding": "10px", "border_radius": "5px"}
            ),
            rx.hstack(
                rx.text("Estado: ", weight="bold"),
                rx.text(State.hill_verif),
            ),
            align_items="start",
            spacing="3",
        ),
        variant="surface",
        padding="6",
        width="100%",
        border_radius="15px",
        background="rgba(255, 255, 255, 0.03)",
        backdrop_filter="blur(15px)",
        box_shadow="0 8px 32px 0 rgba(0, 0, 0, 0.37)",
        border="1px solid rgba(255, 255, 255, 0.08)"
    )

def tabs_layout():
    return rx.tabs.root(
        rx.tabs.list(
            rx.tabs.trigger("1. CRR", value="crr"),
            rx.tabs.trigger("2. RSA", value="rsa"),
            rx.tabs.trigger("3. n Genérico", value="ngen"),
            rx.tabs.trigger("4. Inversos", value="inv"),
            rx.tabs.trigger("5. Autoclave", value="autoc"),
            rx.tabs.trigger("6. Gauss-Jordan", value="gauss"),
            width="100%",
            margin_bottom="4"
        ),
        rx.tabs.content(crr_card(), value="crr"),
        rx.tabs.content(rsa_card(), value="rsa"),
        rx.tabs.content(ngen_card(), value="ngen"),
        rx.tabs.content(inversos_card(), value="inv"),
        rx.tabs.content(autoc_card(), value="autoc"),
        rx.tabs.content(gauss_card(), value="gauss"),
        default_value="crr",
        width="100%"
    )

def index() -> rx.Component:
    return rx.center(
        rx.vstack(
            rx.hstack(
                rx.icon("lock", size=40, color="var(--accent-9)"),
                rx.heading("Interfaz del proyecto de criptografía", size="8", margin_bottom="2"),
                align_items="center"
            ),
            rx.text("Proyecto 1 - Grupo G", size="4", color="gray", margin_bottom="6"),
            
            tabs_layout(),
            
            spacing="5",
            max_width="800px",
            width="100%",
            padding="2rem",
        ),
        width="100%",
        min_height="100vh",
        background="radial-gradient(circle at top, #1a1a2e, #16213e, #0f3460)",
    )

app = rx.App(
    theme=rx.theme(
        appearance="dark",
        has_background=True,
        radius="large",
        accent_color="cyan",
        gray_color="slate",
    )
)
app.add_page(index, title="Crypto Dashboard")
