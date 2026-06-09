import pandas as pd
import streamlit as st


@st.cache_data(show_spinner=False)
def load_temperature_data() -> pd.DataFrame:
    url = "https://storage.googleapis.com/berkeley-earth-temperature-hr/global/Global_TAVG_monthly.txt"
    columns = [
        "Year",
        "Month",
        "Monthly_Anomaly",
        "Monthly_Unc",
        "Annual_Anomaly",
        "Annual_Unc",
        "FiveYear_Anomaly",
        "FiveYear_Unc",
        "TenYear_Anomaly",
        "TenYear_Unc",
        "TwentyYear_Anomaly",
        "TwentyYear_Unc",
    ]
    df = pd.read_csv(
        url,
        sep=r"\s+",
        comment="%",
        header=None,
        names=columns,
        engine="python",
    )
    df["Date"] = pd.to_datetime(
        df["Year"].astype(str) + "-" + df["Month"].astype(str).str.zfill(2),
        format="%Y-%m",
    )
    return df


def main() -> None:
    st.set_page_config(page_title="Temperature Table", page_icon="🌍", layout="wide")
    st.title("🌍 Temperaturdaten aus Berkeley Earth")
    st.write("Diese Tabelle wird direkt aus der angegebenen Quelle geladen.")

    df = load_temperature_data()

    st.caption(f"{len(df):,} Zeilen geladen")

    year_min = int(df["Year"].min())
    year_max = int(df["Year"].max())
    selected_years = st.slider(
        "Jahre auswählen",
        min_value=year_min,
        max_value=year_max,
        value=(year_min, year_max),
    )

    filtered_df = df[
        (df["Year"] >= selected_years[0]) & (df["Year"] <= selected_years[1])
    ]

    display_df = filtered_df[["Date", "Year", "Month", "Monthly_Anomaly", "Monthly_Unc"]].copy()
    display_df = display_df.rename(
        columns={
            "Date": "Datum",
            "Year": "Jahr",
            "Month": "Monat",
            "Monthly_Anomaly": "Monatlicher Anstieg",
            "Monthly_Unc": "Unsicherheit",
        }
    )

    st.dataframe(display_df, use_container_width=True)


if __name__ == "__main__":
    main()
