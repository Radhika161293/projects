import pandas as pd
from sqlalchemy import create_engine, text

df = pd.read_csv('agri.csv')

df.columns = df.columns.str.strip().str.replace(' ', '_').str.replace('(', '').str.replace(')', '').str.replace('/', '_').str.lower()

df['year'] = pd.to_numeric(df['year'], errors='coerce')

db_url = "mysql+pymysql://3p4fdyCt9Bzwfkh.root:w38mCpM1dvOB8CGL@gateway01.eu-central-1.prod.aws.tidbcloud.com:4000/PROJECT?ssl_verify_cert=false"

engine = create_engine(db_url)

table_name = "agri_data"


print(f"✅ Data successfully uploaded to TiDB in table '{table_name}'!")

with engine.connect() as connection:
    print("✅ Connected to TiDB successfully!")


    query1 = """
    SELECT
        year,
        state_name,
        SUM(rice_production_1000_tons) AS total_rice_production
    FROM
        agri_data
    GROUP BY
        year, state_name
    ORDER BY
        year ASC, total_rice_production DESC
    LIMIT 3;
    """
    result1 = connection.execute(text(query1))
    print("📊 Year-wise Trend of Rice Production Across States (Top 3):")
    for row in result1.fetchall():
        print(row)

    query2 = """
    SELECT
        a.dist_name,
        a.year,
        (a.wheat_yield_kg_per_ha - b.wheat_yield_kg_per_ha) AS yield_increase
    FROM
        agri_data a
    JOIN
        agri_data b
    ON
        a.dist_name = b.dist_name
        AND a.year = b.year + 5
    WHERE
        b.wheat_yield_kg_per_ha > 0
    ORDER BY
        yield_increase DESC
    LIMIT 5;
    """
    result2 = connection.execute(text(query2))
    print("\n📊 Top 5 Districts by Wheat Yield Increase Over the Last 5 Years:")
    for row in result2.fetchall():
        print(row)

    query3 = """
    SELECT
        a.state_name,
        ((a.oilseeds_production_1000_tons - b.oilseeds_production_1000_tons) / b.oilseeds_production_1000_tons) * 100 AS growth_rate
    FROM
        agri_data a
    JOIN
        agri_data b
    ON
        a.state_name = b.state_name
        AND a.year = b.year + 5
    WHERE
        b.oilseeds_production_1000_tons > 0
    ORDER BY
        growth_rate DESC
    LIMIT 5;
    """
    result3 = connection.execute(text(query3))
    print("\n📊 States with the Highest Growth in Oilseed Production (5-Year Growth Rate):")
    for row in result3.fetchall():
        print(row)

    query_corr = """
    SELECT
        dist_name,
        rice_area_1000_ha,
        rice_production_1000_tons,
        wheat_area_1000_ha,
        wheat_production_1000_tons,
        maize_area_1000_ha,
        maize_production_1000_tons
    FROM
        agri_data;
    """

    df_corr = pd.read_sql(query_corr, engine)

    corr_matrix = df_corr[['rice_area_1000_ha', 'rice_production_1000_tons',
                        'wheat_area_1000_ha', 'wheat_production_1000_tons',
                        'maize_area_1000_ha', 'maize_production_1000_tons']].corr()

    print("\n📊 Correlation Matrix for Major Crops:")
    print(corr_matrix)


    query5 = """
    SELECT
        state_name,
        year,
        SUM(cotton_production_1000_tons) AS total_cotton_production
    FROM
        agri_data
    GROUP BY
        state_name, year
    ORDER BY
        total_cotton_production DESC
    LIMIT 5;
    """
    result5 = connection.execute(text(query5))
    print("\n📊 Yearly Production Growth of Cotton in Top 5 Cotton Producing States:")
    for row in result5.fetchall():
        print(row)

    query6 = """
    SELECT
        dist_name,
        SUM(groundnut_production_1000_tons) AS total_groundnut_production
    FROM
        agri_data
    WHERE
        year = 2020
    GROUP BY
        dist_name
    ORDER BY
        total_groundnut_production DESC
    LIMIT 5;
    """
    result6 = connection.execute(text(query6))
    print("\n📊 Districts with the Highest Groundnut Production in 2020:")
    for row in result6.fetchall():
        print(row)

    query7 = """
    SELECT
        year,
        AVG(maize_yield_kg_per_ha) AS avg_maize_yield
    FROM
        agri_data
    GROUP BY
        year
    ORDER BY
        year ASC;
    """
    result7 = connection.execute(text(query7))
    print("\n📊 Annual Average Maize Yield Across All States:")
    for row in result7.fetchall():
        print(row)

    query8 = """
    SELECT
        state_name,
        SUM(oilseeds_area_1000_ha) AS total_oilseed_area
    FROM
        agri_data
    GROUP BY
        state_name
    ORDER BY
        total_oilseed_area DESC;
    """
    result8 = connection.execute(text(query8))
    print("\n📊 Total Area Cultivated for Oilseeds in Each State:")
    for row in result8.fetchall():
        print(row)

    query9 = """
    SELECT
        dist_name,
        MAX(rice_yield_kg_per_ha) AS highest_rice_yield
    FROM
        agri_data
    GROUP BY
        dist_name
    ORDER BY
        highest_rice_yield DESC
    LIMIT 5;
    """
    result9 = connection.execute(text(query9))
    print("\n📊 Districts with the Highest Rice Yield:")
    for row in result9.fetchall():
        print(row)

    query10 = """
    WITH top_states AS (
        SELECT
            state_name,
            SUM(rice_production_1000_tons + wheat_production_1000_tons) AS total_production
        FROM
            agri_data
        GROUP BY
            state_name
        ORDER BY
            total_production DESC
        LIMIT 5
    )
    SELECT
        year,
        state_name,
        SUM(rice_production_1000_tons) AS total_rice_production,
        SUM(wheat_production_1000_tons) AS total_wheat_production
    FROM
        agri_data
    WHERE
        state_name IN (SELECT state_name FROM top_states)
        AND year BETWEEN (SELECT MAX(year) - 10 FROM agri_data) AND (SELECT MAX(year) FROM agri_data)
    GROUP BY
        year, state_name
    ORDER BY
        year ASC;
    """
    result10 = connection.execute(text(query10))
    print("\n📊 Compare the Production of Wheat and Rice for the Top 5 States Over 10 Years:")
    for row in result10.fetchall():
        print(row)
