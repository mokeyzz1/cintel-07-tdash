# Importing necessary libraries for data visualization, UI, and interactivity
import seaborn as sns
from faicons import icon_svg
from shiny import reactive
from shiny.express import input, render, ui
import palmerpenguins  # Loading the Penguins dataset

# Load the Palmer Penguins dataset into a DataFrame
df = palmerpenguins.load_penguins()

# Define overall page options
ui.page_opts(title="Penguins Dashboard", fillable=True)  # Set title for the app page

# Sidebar: Define filters and useful links
with ui.sidebar(title="Filter Penguins Data"):
    # Slider for filtering penguins by body mass
    ui.input_slider("mass", "Maximum Body Mass (grams)", 2000, 6000, 6000)
    
    # Checkbox group for filtering penguins by species
    ui.input_checkbox_group(
        "species",
        "Select Species to Display",
        ["Adelie", "Gentoo", "Chinstrap"],
        selected=["Adelie", "Gentoo", "Chinstrap"],
    )
    
    # Divider for visual clarity
    ui.hr()

    # Links section with resources for users
    ui.h6("Useful Resources")
    ui.a(
        "GitHub Repository: Source Code",
        href="https://github.com/denisecase/cintel-07-tdash",
        target="_blank",
    )
    ui.a(
        "Live App Deployment",
        href="https://denisecase.github.io/cintel-07-tdash/",
        target="_blank",
    )
    ui.a(
        "Report Issues",
        href="https://github.com/denisecase/cintel-07-tdash/issues",
        target="_blank",
    )
    ui.a("Learn PyShiny", href="https://shiny.posit.co/py/", target="_blank")
    ui.a(
        "Dashboard Template",
        href="https://shiny.posit.co/py/templates/dashboard/",
        target="_blank",
    )
    ui.a(
        "Penguins Dashboard Express Example",
        href="https://github.com/denisecase/pyshiny-penguins-dashboard-express",
        target="_blank",
    )

# Main layout: Display value boxes and visualizations
with ui.layout_column_wrap(fill=False):
    # Value box to display the number of penguins in the filtered dataset
    with ui.value_box(showcase=icon_svg("earlybirds")):
        "Total Number of Penguins"

        @render.text
        def count():
            return filtered_df().shape[0]

    # Value box for displaying the average bill length
    with ui.value_box(showcase=icon_svg("ruler-horizontal")):
        "Average Bill Length (mm)"

        @render.text
        def bill_length():
            return f"{filtered_df()['bill_length_mm'].mean():.1f} mm"

    # Value box for displaying the average bill depth
    with ui.value_box(showcase=icon_svg("ruler-vertical")):
        "Average Bill Depth (mm)"

        @render.text
        def bill_depth():
            return f"{filtered_df()['bill_depth_mm'].mean():.1f} mm"

# Layout for charts and data grid
with ui.layout_columns():
    # Card displaying scatterplot of bill length vs bill depth
    with ui.card(full_screen=True):
        ui.card_header("Bill Length vs. Bill Depth")

        @render.plot
        def length_depth():
            return sns.scatterplot(
                data=filtered_df(),
                x="bill_length_mm",
                y="bill_depth_mm",
                hue="species",
            )

    # Card displaying the filtered dataset in a DataGrid
    with ui.card(full_screen=True):
        ui.card_header("Penguins Dataset Overview")

        @render.data_frame
        def summary_statistics():
            # Columns to display in the DataGrid
            cols = [
                "species",
                "island",
                "bill_length_mm",
                "bill_depth_mm",
                "body_mass_g",
            ]
            # Enable filters for the DataGrid
            return render.DataGrid(filtered_df()[cols], filters=True)

# Uncomment to include a custom CSS file for styling (if needed)
# ui.include_css(app_dir / "styles.css")

# Reactive calculation for filtering the dataset based on user input
@reactive.calc
def filtered_df():
    """
    Filter the dataset based on:
    1. Selected species from the checkbox group.
    2. Body mass less than the value set by the slider.
    """
    filt_df = df[df["species"].isin(input.species())]
    filt_df = filt_df.loc[filt_df["body_mass_g"] < input.mass()]
    return filt_df
