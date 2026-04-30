import reflex as rx
from rxconfig import config

from mi_crypto_lib.teoria_numeros.crr import crr
from mi_crypto_lib.teoria_numeros.phi import phi
from mi_crypto_lib.teoria_numeros.ejercicio_rsa_base import generar_primo_seguro

class State(rx.State):
    """The app state."""
    # CRR
    n_crr: str = ""
    crr_elements: list[int] = []
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

    def set_n_crr(self, val: str):
        self.n_crr = val

    def set_inicio_p(self, val: str):
        self.inicio_p = val

    def set_inicio_q(self, val: str):
        self.inicio_q = val

    def calculate_crr(self):
        try:
            n = int(self.n_crr)
            if n < 2:
                self.crr_verified = "Error: n debe ser mayor o igual a 2"
                return
            elements = crr(n)
            phi_val = phi(n)
            
            self.crr_elements = elements
            self.crr_length = str(len(elements))
            self.phi_theoretical = str(phi_val)
            self.crr_verified = " Coincide exactamente" if len(elements) == phi_val else "❌ No coincide"
        except ValueError:
            self.crr_verified = "Error: Ingrese un número válido."
            self.crr_elements = []
            self.crr_length = ""
            self.phi_theoretical = ""

    def calculate_rsa(self):
        try:
            ini_p = int(self.inicio_p)
            ini_q = int(self.inicio_q)
            
            p = generar_primo_seguro(ini_p)
            q = generar_primo_seguro(ini_q)
            
            # Asegurar que p y q no sean el mismo primo
            if p == q:
                q = generar_primo_seguro(p + 1)
                
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
                rx.code(State.crr_elements.to(str))
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
                rx.input(placeholder="Semilla para p", value=State.inicio_p, on_change=State.set_inicio_p),
                rx.input(placeholder="Semilla para q", value=State.inicio_q, on_change=State.set_inicio_q),
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

def placeholder_card(titulo: str):
    return rx.card(
        rx.vstack(
            rx.heading(titulo, size="5", color="gray"),
            rx.icon("wrench", size=40, color="gray"),
            rx.text("Módulo en desarrollo...", color="gray"),
            align_items="center",
            spacing="4",
            padding="10",
        ),
        variant="surface",
        width="100%",
        border_radius="15px",
        background="rgba(255, 255, 255, 0.03)",
        backdrop_filter="blur(15px)",
        box_shadow="0 8px 32px 0 rgba(0, 0, 0, 0.37)",
        border="1px solid rgba(255, 255, 255, 0.08)",
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
        rx.tabs.content(placeholder_card("3. Algoritmo para n Genérico"), value="ngen"),
        rx.tabs.content(placeholder_card("4. Relación con Inversos Multiplicativos"), value="inv"),
        rx.tabs.content(placeholder_card("5. Sistema de Cifra Autoclave"), value="autoc"),
        rx.tabs.content(placeholder_card("6. Ataque de Gauss-Jordan contra Hill"), value="gauss"),
        default_value="crr",
        width="100%"
    )

def index() -> rx.Component:
    return rx.center(
        rx.vstack(
            rx.hstack(
                rx.icon("lock", size=40, color="var(--accent-9)"),
                rx.heading("Explorador Criptográfico", size="8", margin_bottom="2"),
                align_items="center"
            ),
            rx.text("Proyecto 1 - Grupo 4", size="4", color="gray", margin_bottom="6"),
            
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
