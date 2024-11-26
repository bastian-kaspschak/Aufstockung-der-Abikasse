from taipy.gui import Gui
import taipy.gui.builder as tgb
import numpy as np

# Initial parameter values
p = kv1 = kv2 = 0.0 # Price and variable unit costs
thr = 750 # Amount threshold
fx = 0 # Fixed costs

# Constants
maxp = 1.50 # Max. price
maxx = 3000 # Max. amount
maxkf = 2000 # Max. fixed costs

# Image path
image_path = "images/durststiller.png"

# Layout
page_width = 800 # Page width (pixels)
plotrange = [-2000, 4000] # Fixed yrange for plot

# Economic Functions
def revenue_function(x, p):
    return p * x

def cost_function(x, kv1, kv2, thr, fx):
    return np.where(x <= thr, kv1 * x + fx, kv2 * x + (kv1 - kv2) * thr + fx)

def profit_function(x, p, kv1, kv2, thr, fx):
    return revenue_function(x, p) - cost_function(x, kv1, kv2, thr, fx)

# Generate initial data
x = np.linspace(0, maxx, 1000)
e = revenue_function(x, p)
k = cost_function(x, kv1, kv2, thr, fx)
g = profit_function(x, p, kv1, kv2, thr, fx)

data = {
    "Menge x in Stk.": x,
    "Erlös E(x) in €": e,
    "Kosten K(x) in €": k,
    "Gewinn G(x) in €": g
}

vertical_line = {
    "yaxis": {"range": plotrange},
    "shapes": [{
        "type": 'line',
        "x0": thr, "y0": plotrange[0], "x1": thr, "y1": plotrange[1],
        "line": {"color": 'rgb(0.5, 0.5, 0.5)', "dash": 'dot'}
    }]
}

# Update function for slider and number input callback
def update_plot(state):
    k = cost_function(x, state.kv1, state.kv2, state.thr, state.fx)
    e = revenue_function(x, state.p)
    g = profit_function(x, state.p, state.kv1, state.kv2, state.thr, state.fx)
    state.data = {
        "Menge x in Stk.": x,
        "Erlös E(x) in €": e,
        "Kosten K(x) in €": k,
        "Gewinn G(x) in €": g
    }
    state.vertical_line = {
        "yaxis": {"range": plotrange},
        "shapes": [{
            "type": 'line',
            "x0": state.thr, "y0": plotrange[0], "x1": state.thr, "y1": plotrange[1],
            "line": {"color": 'rgb(0.5, 0.5, 0.5)', "dash": 'dot'}
        }]
    }

# Pages
with tgb.Page() as root:
    with tgb.layout(columns="1 1 1"):
        tgb.part()
        with tgb.part(width=f"{page_width}px"):
            tgb.toggle(label="Modus", theme=True)
            tgb.navbar()
            tgb.text("# Mehr Geld für die Abikasse", mode="md")
        tgb.part()

with tgb.Page() as plotter:
    with tgb.layout(columns="1 1 1"):
        tgb.part()
        with tgb.part(width=f"{page_width}px"):
            with tgb.layout(columns="2fr 1fr", gap="30px"):
                with tgb.part():
                    tgb.text("## Plot", mode="md")
                    tgb.chart(
                        "{data}", mode="lines", x="Menge x in Stk.",
                        y__1="Erlös E(x) in €", y__2="Kosten K(x) in €",
                        y__3="Gewinn G(x) in €", layout="{vertical_line}", fixed_axis=True
                    )
                with tgb.part():
                    tgb.text("## Parameter", mode="md")
                    for label, var, max_val, step in [
                        ("Preis in €", "p", maxp, 0.01),
                        ("Var. Stückkosten kᵥ,₁ in €", "kv1", 1.0, 0.01),
                        ("Var. Stückkosten kᵥ,₂ in €", "kv2", 1.0, 0.01),
                        ("Rabattschwelle xₛ in Stück", "thr", maxx, max(1,int(maxx/100))),
                        ("Fixkosten K_f in €", "fx", maxkf, max(1,int(maxkf/100)))
                    ]:
                        with tgb.expandable(title=label):
                            tgb.number(f"{{{var}}}", min=0.0, max=max_val, step=step, on_change=update_plot)
                            tgb.slider(f"{{{var}}}", min=0.0, max=max_val, step=step, on_change=update_plot)
        tgb.part()

with tgb.Page() as start:
    with tgb.layout(columns="1 1 1"):
        tgb.part()
        with tgb.part(width=f"{page_width}px"):
            with tgb.layout(columns="1 1"):
                tgb.image(image_path)
                with tgb.part():
                    tgb.text("Bei vielen Schülerinnen und Schülern besteht eine sehr hohe Nachfrage nach Durststillern. Daher beschließt die 24HH1 für die nächsten Monate in den Pausen Durststiller verschiedener Geschmackssorten für je **1,20€** pro Stück zu verkaufen und so die Abikasse aufzustocken.", mode="md")
                    tgb.text("Für die gesamte Aktion fallen durch Transport, Lagerung, Miete und Werbung Fixkosten von **900€** an. Der Großhändler, von dem die Durststiller bezogen werden, verlangt **0,70€** je Stück. Allerdings gewährt er der 24HH1 einen Mengenrabatt: Nach dem **750**. Durststiller (Rabattschwelle) verlangt er nämlich nur noch **0,36€** je Stück.", mode="md")
                    tgb.text("Insgesamt reicht das Budget aus, um die Fixkosten zu tragen und maximal 3.000 Durststiller beim Großhändler einzukaufen.", mode="md")
                    tgb.text("**Wie viele Durststiller müssten mindestens verkauft werden, damit die 24HH1 keinen Verlust macht?**", mode="md")
                    tgb.text("**Wie hoch ist der Gewinn, wenn alle 3.000 Durststiller verkauft werden?**", mode="md")
            with tgb.part():
                tgb.text("## Arbeitsauftrag", mode="md")
                tgb.text("Ihnen steht im obigen Reiter ein Funktionsplotter zur Verfügung. Über Schieberegler und Eingabefelder können Sie den Preis, die Fixkosten, die Rabattschwelle und die variablen Stückkosten vor und nach der Rabattschwelle dynamisch anpassen.", mode="md")
                tgb.text("Übernehmen Sie die gegebenen Werte aus dem obigen Text und visualisieren Sie die Funktionsgraphen für die Erlös-, Kosten- und Gewinnfunktion. Bestimmen Sie außerdem graphisch die **Gewinnschwelle** und den **Gewinn bei 3.000 verkauften Durststillern**. Machen Sie anschließend einen Screenshot der drei Funktionsgraphen.", mode="md")
        tgb.part()

# Page routing
pages = {
    "/": root,
    "Start": start,
    "Funktionsplotter": plotter
}

# Launch the GUI
Gui(pages=pages).run(use_reloader=True, debug=True, dark_mode=False)
