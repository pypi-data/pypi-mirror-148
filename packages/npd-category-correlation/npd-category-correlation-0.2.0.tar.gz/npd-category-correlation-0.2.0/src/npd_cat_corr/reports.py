import datetime
import logging
import pandas as pd
import numpy as np
import os
import calendar

NON_SALES_COLS = ['Ticker','quarter_end','date', 'eps_estimate',
       'eps_reported', 'gaap_eps', 'quarter', 'reported_revenue',
       'revenue_estimate', 'symbol', "total_dollars", "eps","profit","revenue", "ann_date","q_datetime","calendar_type", "SALES_REV_TURN","GROSS_PROFIT","ARD_GROSS_PROFITS","IS_EPS", "IS_COMP_EPS_ADJUSTED", "IS_BASIC_EPS_CONT_OPS", "ARD_ADJUSTED_EPS","IS_ADJUSTED_EPS_AS_REPORTED", "BEST_SALES","BEST_EPS","IS_COMP_EPS_EXCL_STOCK_COMP"]

REVENUE_REPORT = "SALES_REV_TURN"
REVENUE_EST = "BEST_SALES"
PROFIT_REPORT = "GROSS_PROFIT"
PROFIT_EST = None
EPS_REPORT = "IS_COMP_EPS_EXCL_STOCK_COMP"
EPS_EST = "BEST_EPS"
NPD_TOTAL_DOLLARS = "total_dollars"
SHARE_PERC_MIN = 0.1

class ReportDataException(Exception):
    pass

def run_summary_cat_report(output_dir, df, retailer=False):

    df["quarter_end"] = pd.to_datetime(df["quarter_end"])
    df = df[df["valid_quarter"]]

    rev_corr_data = []
    profit_corr_data = []
    eps_corr_data = []

    for symbol in df["symbol"].unique():
        sdf = df[df["symbol"] == symbol]
        sdf = sdf.dropna(how="all", axis=1)
        share_percs = get_share_percs(sdf)
        sdf = sdf[[c for c in sdf.columns if c in ["quarter_end",REVENUE_REPORT,REVENUE_EST,PROFIT_REPORT,PROFIT_EST,EPS_REPORT,EPS_EST,NPD_TOTAL_DOLLARS]] + [c for c in sdf.columns if (c not in NON_SALES_COLS and share_percs[c] > SHARE_PERC_MIN) or (c not in NON_SALES_COLS and retailer)]]
        sdf_yy = get_yy_df(sdf)

        #revenue correlations
        best_rev_cat, rev_cat_corr, rev_total_corr, rev_est_corr = get_ticker_correlations(sdf_yy, REVENUE_REPORT, REVENUE_EST)
        if np.nan not in [best_rev_cat, rev_cat_corr]:
            rev_corr_data.append({"symbol":symbol, "category":best_rev_cat, "category_corr":rev_cat_corr, "total_dollars_corr":rev_total_corr, "share_of_total_dollars":share_percs[best_rev_cat], "estimate_corr":rev_est_corr})

        #profit correlations
        best_profit_cat, profit_cat_corr, profit_total_corr, profit_est_corr = get_ticker_correlations(sdf_yy, PROFIT_REPORT, PROFIT_EST)
        if np.nan not in [best_profit_cat, profit_cat_corr]:
            profit_corr_data.append({"symbol":symbol, "category":best_profit_cat, "category_corr":profit_cat_corr, "total_dollars_corr":profit_total_corr, "share_of_total_dollars":share_percs[best_profit_cat], "estimate_corr":profit_est_corr})

        #eps correlations
        best_eps_cat, eps_cat_corr, eps_total_corr, eps_est_corr = get_ticker_correlations(sdf_yy, EPS_REPORT, EPS_EST)
        if np.nan not in [best_eps_cat, eps_cat_corr]:
            eps_corr_data.append({"symbol":symbol, "category":best_eps_cat, "category_corr":eps_cat_corr, "total_dollars_corr":eps_total_corr, "share_of_total_dollars":share_percs[best_eps_cat], "estimate_corr":eps_est_corr})
    
    rev_corr_df = pd.DataFrame(rev_corr_data).sort_values("category_corr", ascending=False)
    profit_corr_df = pd.DataFrame(profit_corr_data).sort_values("category_corr", ascending=False)
    if PROFIT_EST == None:
        profit_corr_df = profit_corr_df.drop(columns=["estimate_corr"])
    eps_corr_df = pd.DataFrame(eps_corr_data).sort_values("category_corr", ascending=False)

    writer = pd.ExcelWriter(output_dir + "YYcorr.xlsx")
    rev_corr_df[["symbol","category","category_corr","total_dollars_corr","share_of_total_dollars","estimate_corr"]].to_excel(writer, sheet_name="Rev YY", index=False)
    profit_corr_df[["symbol","category","category_corr","total_dollars_corr","share_of_total_dollars"]].to_excel(writer, sheet_name="Profit YY", index=False)
    eps_corr_df[["symbol","category","category_corr","total_dollars_corr","share_of_total_dollars","estimate_corr"]].to_excel(writer, sheet_name="EPS YY", index=False)
    workbook = writer.book
    rev_sheet = writer.sheets["Rev YY"]
    profit_sheet = writer.sheets["Profit YY"]
    eps_sheet = writer.sheets["EPS YY"] 

    beat_consensus_format = workbook.add_format({"bg_color":"#6ADF41"})
    beat_total_dollars_format = workbook.add_format({"bg_color":"#5897FE"})
    percent_format = workbook.add_format({'num_format': '0.0%'})

    rev_sheet.conditional_format(1, 2, len(rev_corr_df), 2, {"type":"formula","criteria":"=AND($C2>$F2,NOT(ISBLANK($F2)),NOT(ISBLANK($C2)))", "format":beat_consensus_format})
    rev_sheet.conditional_format(1, 2, len(rev_corr_df), 2, {"type":"formula","criteria":"=AND($C2>$D2,NOT(ISBLANK($D2)),NOT(ISBLANK($C2)))", "format":beat_total_dollars_format})
    rev_sheet.set_column(4, 4, cell_format=percent_format)

    if PROFIT_EST != None:
        profit_sheet.conditional_format(1, 2, len(profit_corr_df), 2, {"type":"formula","criteria":"=AND($C2>$F2,NOT(ISBLANK($F2)),NOT(ISBLANK($C2)))", "format":beat_consensus_format})
    profit_sheet.conditional_format(1, 2, len(profit_corr_df), 2, {"type":"formula","criteria":"=AND($C2>$D2,NOT(ISBLANK($D2)),NOT(ISBLANK($C2)))", "format":beat_total_dollars_format})
    profit_sheet.set_column(4, 4, cell_format=percent_format)

    eps_sheet.conditional_format(1, 2, len(eps_corr_df), 2, {"type":"formula","criteria":"=AND($C2>$F2,NOT(ISBLANK($F2)),NOT(ISBLANK($C2)))", "format":beat_consensus_format})
    eps_sheet.conditional_format(1, 2, len(eps_corr_df), 2, {"type":"formula","criteria":"=AND($C2>$D2,NOT(ISBLANK($D2)),NOT(ISBLANK($C2)))", "format":beat_total_dollars_format})
    eps_sheet.set_column(4, 4, cell_format=percent_format)

    writer.save()
    writer.close()


def get_yy_df(sdf):

    sdf_yy = sdf.copy()
    sdf_yy = sdf_yy.set_index("quarter_end")
    for x in sdf_yy.columns:
        if x not in NON_SALES_COLS or x in ["total_dollars",REVENUE_REPORT,REVENUE_EST,PROFIT_REPORT,EPS_REPORT,EPS_EST]:
            sdf_yy[x] = sdf_yy[x].pct_change(freq=pd.DateOffset(years=1))
    sdf_yy = sdf_yy.reset_index()
    scols = [x for x in sdf_yy.columns if x != "quarter_end"]
    sdf_yy = sdf_yy.dropna(how="all", axis=0, subset=scols)
    return sdf_yy

def get_share_percs(sdf):

    share_sdf = sdf.copy()
    share_percs = {}
    for sales_col in [c for c in share_sdf.columns if c not in NON_SALES_COLS]:
        share_sdf[sales_col] = share_sdf[sales_col].apply(lambda x: 0 if pd.isnull(x) else x)
        share_percs[sales_col] = (share_sdf[sales_col] / share_sdf["total_dollars"]).mean()
    return share_percs

def get_ticker_correlations(sdf, measure, measure_est, min_periods=4):
    print(sdf)
    if measure not in sdf.columns or (measure_est != None and measure_est not in sdf.columns):
        return np.nan, np.nan, np.nan, np.nan
    corr_df = sdf.corr(min_periods=min_periods)
    total_dollars_corr = corr_df.loc[NPD_TOTAL_DOLLARS, measure]
    if measure_est:
        est_corr = corr_df.loc[measure_est, measure]
    else:
        est_corr = None
    corr_df = corr_df.reset_index()
    corr_df = corr_df[~corr_df["index"].isin(NON_SALES_COLS)].set_index("index")
    best_cat = corr_df[measure].idxmax()
    best_cat_corr = corr_df[measure].max()
    return best_cat, best_cat_corr, total_dollars_corr, est_corr


def run_cat_report(output_dir, ticker, df, retailer=False):

    df["quarter_end"] = pd.to_datetime(df["quarter_end"])
    df = df[df["valid_quarter"]]

    if ticker not in df["symbol"].unique():
        raise ReportDataException("Ticker not in data")
    
    sdf = df[df["symbol"] == ticker]
    sdf = sdf.dropna(how="all", axis=1)
    share_percs = get_share_percs(sdf)
    sdf = sdf[[c for c in sdf.columns if c in ["quarter_end",REVENUE_REPORT,REVENUE_EST,PROFIT_REPORT,PROFIT_EST,EPS_REPORT,EPS_EST,NPD_TOTAL_DOLLARS]] + [c for c in sdf.columns if (c not in NON_SALES_COLS and share_percs[c] > SHARE_PERC_MIN) or (c not in NON_SALES_COLS and retailer)]]
    sdf_yy = get_yy_df(sdf)

    sdf = sdf.set_index("quarter_end").reset_index().sort_values("quarter_end")
    sdf_yy = sdf_yy.set_index("quarter_end").reset_index().sort_values("quarter_end")

    sdf["quarter_end"] = sdf["quarter_end"].apply(lambda x: x.strftime("%Y-%m-%d"))
    sdf_yy["quarter_end"] = sdf_yy["quarter_end"].apply(lambda x: x.strftime("%Y-%m-%d"))

    yy_best_rev_cat, yy_rev_cat_corr, yy_rev_total_corr, yy_rev_est_corr = get_ticker_correlations(sdf_yy, REVENUE_REPORT, REVENUE_EST)
    yy_best_profit_cat, yy_profit_cat_corr, yy_profit_total_corr, yy_profit_est_corr = get_ticker_correlations(sdf_yy, PROFIT_REPORT, PROFIT_EST)
    yy_best_eps_cat, yy_eps_cat_corr, yy_eps_total_corr, yy_eps_est_corr = get_ticker_correlations(sdf_yy, EPS_REPORT, EPS_EST)

    use_rev = np.nan not in [yy_best_rev_cat, yy_rev_cat_corr]
    use_profit = np.nan not in [yy_best_profit_cat, yy_profit_cat_corr]
    use_eps = np.nan not in [yy_best_eps_cat, yy_eps_cat_corr]

    if True not in [use_rev, use_profit, use_eps]:
        raise ReportDataException("Not enough data for report")

    writer = pd.ExcelWriter( output_dir + ticker + "_category_correlation.xlsx")
    
    workbook = writer.book
    yy_visuals_sheet = workbook.add_worksheet(ticker + " YY")
    #raw_visuals_sheet = workbook.add_worksheet(ticker + " Raw")
    sdf_yy.to_excel(writer, index=False, sheet_name="YY Data")
    sdf.to_excel(writer, index=False, sheet_name="Raw Data")
    yy_sheet = writer.sheets["YY Data"]
    raw_sheet = writer.sheets["Raw Data"]

    percent_format = workbook.add_format({'num_format': '0.0%'})    
    border_format = workbook.add_format({"border":2})
    rounded_format = workbook.add_format({'num_format': '0.###'})
    rounded_border_format = workbook.add_format({'num_format': '0.###', 'border':2})
    percent_border_format = workbook.add_format({"num_format": "0.0%","border":2})
    beat_consensus_format = workbook.add_format({"num_format": "0.###","border":2})
    beat_consensus_format.set_bg_color("#6ADF41")
    beat_total_dollars_format = workbook.add_format({"num_format": "0.###","border":2})
    beat_total_dollars_format.set_bg_color("#5897FE")

    yy_cols = list(sdf_yy.columns)
    for col in [yy_cols.index(x) for x in sdf_yy.columns if x != "quarter_end"]:
        yy_sheet.set_column(col, col, cell_format=percent_format)

    #ticker and category table
    yy_visuals_sheet.write("A1", "Data", border_format)
    yy_visuals_sheet.write("B1", ticker + " Dollars %YY", border_format)
    yy_visuals_sheet.write("A2", "Best Category (Revenue)", border_format)
    if use_rev:
        yy_visuals_sheet.write("B2", yy_best_rev_cat, border_format)
    else:
        yy_visuals_sheet.write("B2", "Unavailable", border_format)
    yy_visuals_sheet.write("A3", "Best Category (Profit)", border_format)
    if use_profit:
        yy_visuals_sheet.write("B3", yy_best_profit_cat, border_format)
    else:
        yy_visuals_sheet.write("B3", "Unavailable", border_format)
    yy_visuals_sheet.write("A4", "Best Category (EPS)", border_format)
    if use_eps:
        yy_visuals_sheet.write("B4", yy_best_eps_cat, border_format)
    else:
        yy_visuals_sheet.write("B4", "Unavailable", border_format)

    #correlations table
    yy_visuals_sheet.write("E1","Category Corr.", border_format)
    yy_visuals_sheet.write("F1","Total NPD Corr.", border_format)
    yy_visuals_sheet.write("G1", "Consensus Corr.", border_format)
    yy_visuals_sheet.write("H1", "Share of Total NPD $", border_format)
    yy_visuals_sheet.write("D2","Revenue", border_format)
    yy_visuals_sheet.write("D3","Profit", border_format)
    yy_visuals_sheet.write("D4","EPS", border_format)

    if use_rev:
        if yy_rev_cat_corr > yy_rev_est_corr:
            yy_visuals_sheet.write("E2",yy_rev_cat_corr, beat_consensus_format)
        elif yy_rev_cat_corr > yy_rev_total_corr:
            yy_visuals_sheet.write("E2",yy_rev_cat_corr, beat_total_dollars_format)
        else:
            yy_visuals_sheet.write("E2",yy_rev_cat_corr, rounded_border_format)
        yy_visuals_sheet.write("F2", yy_rev_total_corr, rounded_border_format)
        yy_visuals_sheet.write("G2",yy_rev_est_corr, rounded_border_format)
        yy_visuals_sheet.write("H2", share_percs[yy_best_rev_cat], percent_border_format)
    else:
        yy_visuals_sheet.write("E2", "Unavailable", border_format)
        yy_visuals_sheet.write("F2", "Unavailable", border_format)
        yy_visuals_sheet.write("G2", "Unavailable", border_format)
        yy_visuals_sheet.write("H2", "Unavailable", border_format)
    
    if use_profit:
        if yy_profit_cat_corr > yy_profit_total_corr:
            yy_visuals_sheet.write("E3",yy_profit_cat_corr, beat_total_dollars_format)
        else:
            yy_visuals_sheet.write("E3",yy_profit_cat_corr, rounded_border_format)
        yy_visuals_sheet.write("F3", yy_profit_total_corr, rounded_border_format)
        yy_visuals_sheet.write("H3", share_percs[yy_best_profit_cat], percent_border_format)
    else:
        yy_visuals_sheet.write("E3", "Unavailable", border_format)
        yy_visuals_sheet.write("F3", "Unavailable", border_format)
        yy_visuals_sheet.write("H3", "Unavailable", border_format)
    yy_visuals_sheet.write("G3", "N/A", border_format)
    
    if use_eps:
        if yy_eps_cat_corr > yy_eps_est_corr:
            yy_visuals_sheet.write("E4", yy_eps_cat_corr, beat_consensus_format)
        elif yy_eps_cat_corr > yy_eps_total_corr:
            yy_visuals_sheet.write("E4", yy_eps_cat_corr, beat_total_dollars_format)
        else:
            yy_visuals_sheet.write("E4", yy_eps_cat_corr, rounded_border_format)
        yy_visuals_sheet.write("F4", yy_eps_total_corr, rounded_border_format)
        yy_visuals_sheet.write("G4", yy_eps_est_corr, rounded_border_format)
        yy_visuals_sheet.write("H4", share_percs[yy_best_eps_cat], percent_border_format)
    else:
        yy_visuals_sheet.write("E4", "Unavailable", border_format)
        yy_visuals_sheet.write("F4", "Unavailable", border_format)
        yy_visuals_sheet.write("G4", "Unavailable", border_format)
        yy_visuals_sheet.write("H4", "Unavailable", border_format)


    for col, size in {0:22, 1:29, 4:14, 5:18, 6:15, 7:18}.items():
        yy_visuals_sheet.set_column(col, col, size)

    yy_x_axis = ["YY Data",1, yy_cols.index("quarter_end"), len(sdf_yy), yy_cols.index("quarter_end")]

    if use_rev:
        yy_rev_cat_chart = create_chart(workbook, "YY Data", list(sdf_yy.columns), yy_best_rev_cat, REVENUE_REPORT, "Reported Revenue", yy_x_axis, len(sdf_yy), yy_rev_cat_corr)
        yy_rev_total_chart = create_chart(workbook, "YY Data", list(sdf_yy.columns), "total_dollars", REVENUE_REPORT, "Reported Revenue", yy_x_axis, len(sdf_yy), yy_rev_total_corr)
        yy_rev_consenesus_chart = create_chart(workbook, "YY Data", list(sdf_yy.columns), "BEST_SALES", REVENUE_REPORT, "Reported Revenue", yy_x_axis, len(sdf_yy), yy_rev_est_corr)
    if use_profit:
        yy_profit_cat_chart = create_chart(workbook, "YY Data", list(sdf_yy.columns), yy_best_profit_cat, PROFIT_REPORT, "Reported Profit", yy_x_axis, len(sdf_yy), yy_profit_cat_corr)
        yy_profit_total_chart = create_chart(workbook, "YY Data", list(sdf_yy.columns), "total_dollars", PROFIT_REPORT, "Reported Profit", yy_x_axis, len(sdf_yy), yy_profit_total_corr)
    if use_eps:
        yy_eps_cat_chart = create_chart(workbook, "YY Data", list(sdf_yy.columns), yy_best_eps_cat, EPS_REPORT, "Reported EPS", yy_x_axis, len(sdf_yy), yy_eps_cat_corr)
        yy_eps_total_chart = create_chart(workbook, "YY Data", list(sdf_yy.columns), "total_dollars", EPS_REPORT, "Reported EPS", yy_x_axis, len(sdf_yy), yy_eps_total_corr)
        yy_eps_consenesus_chart = create_chart(workbook, "YY Data", list(sdf_yy.columns), "BEST_EPS", EPS_REPORT, "Reported EPS", yy_x_axis, len(sdf_yy), yy_eps_est_corr)

    if use_rev:
        yy_visuals_sheet.insert_chart("A6", yy_rev_cat_chart)
        yy_visuals_sheet.insert_chart("E6", yy_rev_total_chart)
        yy_visuals_sheet.insert_chart("J6", yy_rev_consenesus_chart, {'x_offset': -44})
    if use_profit:
        yy_visuals_sheet.insert_chart("A21", yy_profit_cat_chart)
        yy_visuals_sheet.insert_chart("E21", yy_profit_total_chart)
    if use_eps:
        yy_visuals_sheet.insert_chart("A36", yy_eps_cat_chart)
        yy_visuals_sheet.insert_chart("E36", yy_eps_total_chart)
        yy_visuals_sheet.insert_chart("J36", yy_eps_consenesus_chart, {'x_offset': -44})

    writer.save()
    writer.close()
        

def create_chart(workbook, sheet_name, sheet_cols, npd_col, measure, measure_label, x_axis, num_rows, r):

    npd_col_name = "Total NPD" if npd_col == "total_dollars" else npd_col
    chart = workbook.add_chart({"type":"line"})
    chart.add_series({"name":npd_col_name,"categories":x_axis, "values":[sheet_name, 1, sheet_cols.index(npd_col), num_rows, sheet_cols.index(npd_col)], "line":{"color":"#0078BE"}})
    chart.add_series({"name":measure_label,"categories":x_axis, "values":[sheet_name, 1, sheet_cols.index(measure), num_rows, sheet_cols.index(measure)], "line":{"color":"red"}})
    chart.set_y_axis({"crossing":"min"})
    chart.set_x_axis({"name":"For Quarter Ending", "position_axis":"on_tick"})
    if npd_col == "total_dollars":
        chart.set_title({"name":"YY Total NPD {measure} Correlation\nr = {r}".format(measure=measure_label.replace("Reported ", ""), r=round(r, 3))})
    elif npd_col in ["BEST_SALES","BEST_EPS"]:
        chart.set_title({"name":"YY Consensus {measure} Correlation\nr = {r}".format(measure=measure_label.replace("Reported ", ""), r=round(r, 3))})
    else:
        chart.set_title({"name":"YY Category {measure} Correlation\nr = {r}".format(measure=measure_label.replace("Reported ", ""), r=round(r, 3))})
    chart.set_legend({"position":"bottom"})
    chart.set_plotarea({"layout":{"x":0.16,"y":0.23,"width":0.84, "height":0.38}})
    return chart