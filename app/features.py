import pandas as pd
import numpy as np
from app.data import (
    get_driver_standings,
    get_constructor_standings,
    get_qualifying_results,
    get_race_results,
    # get_practice_telemetry,
)

FEATURE_COLS = [
    'qualiPosition',
    'driver_points',
    'driver_champ_pos',
    'driver_wins',
    'constructor_points',
    'constructor_pos',
]


def build_features(year: int, round_num: int, include_result: bool = True) -> pd.DataFrame:
    quali = get_qualifying_results(year, round_num)
    if quali.empty:
        return pd.DataFrame()

    driver_st = get_driver_standings(year, round_num)
    constr_st = get_constructor_standings(year, round_num)

    df = quali.copy()

    if not driver_st.empty:
        df = df.merge(driver_st, on='code', how='left')
    else:
        df['driver_points'] = 0.0
        df['driver_champ_pos'] = range(1, len(df) + 1)
        df['driver_wins'] = 0

    if not constr_st.empty:
        df = df.merge(constr_st, on='constructorId', how='left')
    else:
        df['constructor_points'] = 0.0
        df['constructor_pos'] = 10

    for col in FEATURE_COLS:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors='coerce')
            median = df[col].median()
            df[col] = df[col].fillna(median if pd.notna(median) else 0)

    df['year'] = year
    df['round'] = round_num

    if include_result:
        results = get_race_results(year, round_num)
        if not results.empty:
            df = df.merge(results, on='code', how='left')

    return df
