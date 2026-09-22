#!/usr/bin/env python3
"""Build MUS_Risk_Aligned_Allocation_Calculator.xlsx (openpyxl, formulas only)."""
from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.worksheet.datavalidation import DataValidation
from openpyxl.comments import Comment
import math

wb = Workbook()
ws = wb.active; ws.title = "Calculator"
F = "Arial"
bold = Font(name=F, bold=True); norm = Font(name=F); blue = Font(name=F, color="0000FF"); title = Font(name=F, bold=True, size=14)
green = Font(name=F, color="008000")
yellow = PatternFill("solid", fgColor="FFFF00"); grey = PatternFill("solid", fgColor="EEEEEE"); head = PatternFill("solid", fgColor="D9E1F2")
thin = Side(style="thin", color="999999"); box = Border(left=thin, right=thin, top=thin, bottom=thin)
wrap = Alignment(wrap_text=True, vertical="center", horizontal="center")

ws["A1"] = "MUS Risk-Aligned Allocation Calculator"; ws["A1"].font = title
ws["A2"] = ("Allocation aid: distributes a probabilistic sample size you have already chosen across amount bands, after certainty items are removed. "
            "It does not determine sample size. Blue cells on yellow are inputs; everything else is a formula."); ws["A2"].font = norm
ws.merge_cells("A2:S2"); ws["A2"].alignment = Alignment(wrap_text=True, vertical="top"); ws.row_dimensions[2].height = 32

ws["A4"] = "Mode (Basic or Advanced)"; ws["B4"] = "Advanced"
ws["C4"] = "Basic: dollar share and occurrence only (severity assumed equal across bands, cost equal). Advanced: adds severity and optional cost."
ws["A5"] = "Total planned probabilistic sample size (transactions)"; ws["B5"] = 400
ws["C5"] = "Chosen by the auditor from the engagement's own sample-size method; this workbook only allocates it."
ws["A6"] = "Reference band (1-4) for 'occurrence that would justify MUS'"; ws["B6"] = 2
ws["C6"] = "Column Q shows, for each band, the occurrence rate at which p*s/c would equal the reference band's, i.e. the condition for MUS to be risk-aligned."
ws["A7"] = "Check: dollar shares sum to 100%"; ws["B7"] = '=IF(ABS(D14-1)<0.0005,"OK","Dollar shares must sum to 100%")'
for r in (4, 5, 6): ws[f"B{r}"].font = blue; ws[f"B{r}"].fill = yellow; ws[f"B{r}"].border = box
for r in (4, 5, 6, 7): ws[f"A{r}"].font = bold; ws[f"C{r}"].font = Font(name=F, italic=True, size=9)
ws["B7"].font = bold
dv = DataValidation(type="list", formula1='"Basic,Advanced"', allow_blank=False); ws.add_data_validation(dv); dv.add("B4")
dv2 = DataValidation(type="whole", operator="between", formula1="1", formula2="4"); ws.add_data_validation(dv2); dv2.add("B6")

headers = ["Band", "Label / amount range", "Number of transactions", "% of remaining dollars (D_h)",
           "Expected error occurrence % (p_h)", "Expected RMS % error when erroneous (sqrt of s_h)",
           "Expected review cost per item (optional)", "Severity used (s_h)", "Cost used (c_h)",
           "Risk multiplier sqrt(p*s/c), relative to reference band", "Unnormalized allocation weight D_h x multiplier",
           "MUS share (dollar-proportional)", "Suggested sample % (risk-aligned)", "MUS sample count",
           "Suggested sample count", "Difference (suggested minus MUS)", "Occurrence % that would justify MUS",
           "Suggested coverage (% of band's transactions)", "MUS coverage (% of band's transactions)"]
cols = "ABCDEFGHIJKLMNOPQRS"
for c, h in zip(cols, headers):
    cell = ws[f"{c}9"]; cell.value = h; cell.font = bold; cell.fill = head; cell.alignment = wrap; cell.border = box
ws.row_dimensions[9].height = 78

# example inputs (hypothetical planning assumptions; match manuscript Table 7)
example = [
    (1, "Below $1,000", 6000, 0.10, 0.010, math.sqrt(0.30), 1),
    (2, "$1,000 to $9,999", 2500, 0.30, 0.015, math.sqrt(0.15), 1),
    (3, "$10,000 to $99,999", 800, 0.40, 0.020, math.sqrt(0.06), 1),
    (4, "$100,000 to certainty threshold", 120, 0.20, 0.025, math.sqrt(0.02), 1),
]
for i, (b, lab, n, d, p, rms, cost) in enumerate(example):
    r = 10 + i
    ws[f"A{r}"] = b; ws[f"B{r}"] = lab; ws[f"C{r}"] = n; ws[f"D{r}"] = d; ws[f"E{r}"] = p; ws[f"F{r}"] = rms; ws[f"G{r}"] = cost
    for c in "BCDEFG":
        ws[f"{c}{r}"].font = blue; ws[f"{c}{r}"].fill = yellow
    ws[f"H{r}"] = f'=IF(AND($B$4="Advanced",F{r}>0),F{r}^2,1)'
    ws[f"I{r}"] = f'=IF(AND($B$4="Advanced",G{r}>0),G{r},1)'
    ws[f"J{r}"] = (f'=IF(OR(D{r}=0,E{r}=0),0,SQRT(E{r}*H{r}/I{r})/SQRT(INDEX($E$10:$E$13,$B$6)*INDEX($H$10:$H$13,$B$6)/INDEX($I$10:$I$13,$B$6)))')
    ws[f"K{r}"] = f'=D{r}*J{r}'
    ws[f"L{r}"] = f'=IF($D$14=0,0,D{r}/$D$14)'
    ws[f"M{r}"] = f'=IF($K$14=0,0,K{r}/$K$14)'
    ws[f"N{r}"] = f'=ROUND(L{r}*$B$5,0)'
    ws[f"O{r}"] = f'=ROUND(M{r}*$B$5,0)'
    ws[f"P{r}"] = f'=O{r}-N{r}'
    ws[f"Q{r}"] = f'=IF(H{r}=0,"",INDEX($E$10:$E$13,$B$6)*INDEX($H$10:$H$13,$B$6)/INDEX($I$10:$I$13,$B$6)*I{r}/H{r})'
    ws[f"R{r}"] = f'=IF(C{r}=0,"",O{r}/C{r})'
    ws[f"S{r}"] = f'=IF(C{r}=0,"",N{r}/C{r})'
    for c in cols: ws[f"{c}{r}"].border = box
    for c in "ADELMQRS": ws[f"{c}{r}"].number_format = "0.00%" if c != "A" else "0"
    ws[f"F{r}"].number_format = "0.0%"; ws[f"C{r}"].number_format = "#,##0"; ws[f"G{r}"].number_format = "0.00"
    ws[f"H{r}"].number_format = "0.0000"; ws[f"I{r}"].number_format = "0.00"; ws[f"J{r}"].number_format = "0.000"; ws[f"K{r}"].number_format = "0.00000"
    for c in "NOP": ws[f"{c}{r}"].number_format = "0;(0);-"
ws["A14"] = "Total"; ws["A14"].font = bold
for c in "CDKLMNOP":
    ws[f"{c}14"] = f"=SUM({c}10:{c}13)"; ws[f"{c}14"].font = bold; ws[f"{c}14"].fill = grey; ws[f"{c}14"].border = box
ws["C14"].number_format = "#,##0"; ws["D14"].number_format = "0.00%"; ws["K14"].number_format = "0.00000"
ws["L14"].number_format = "0.00%"; ws["M14"].number_format = "0.00%"
for c in "NOP": ws[f"{c}14"].number_format = "0;(0);-"
ws["Q14"] = '=IF(N14<>B5,"Rounded counts; compare total with B5","")'; ws["Q14"].font = Font(name=F, italic=True, size=9)

ws["A16"] = "What MUS assumes"; ws["A16"].font = bold
ws["A17"] = ("MUS is the special case of this allocation in which p_h x s_h / c_h is the same in every band. Column Q shows the occurrence rate each band would need, "
             "given its severity and cost, for that to hold relative to the reference band. If you believe those rates, the MUS counts (column N) are risk-aligned; if not, the suggested counts (column O) are.")
ws.merge_cells("A17:S17"); ws["A17"].alignment = Alignment(wrap_text=True, vertical="top"); ws.row_dimensions[17].height = 40
ws["A19"] = "Formulas"; ws["A19"].font = bold
ws["A20"] = "Suggested share_h = D_h x sqrt(p_h x s_h / c_h) / sum over bands of the same quantity. MUS share_h = D_h. Basic mode sets s_h = 1 and c_h = 1 for every band (equal severity and cost assumed)."
ws["A21"] = "s_h is entered as the RMS percentage error among erroneous transactions and squared inside the workbook. p_h, s_h and c_h are planning inputs unless taken from prior, pilot or reference evidence; label their source in the Notes sheet."
ws["A22"] = "Source: Equation (11) and Supplemental Section S1.6 of 'Assumed, Not Measured'. Example values are hypothetical planning assumptions and match Table 7 of the manuscript."
for r in (20, 21, 22):
    ws.merge_cells(f"A{r}:S{r}"); ws[f"A{r}"].alignment = Alignment(wrap_text=True, vertical="top"); ws.row_dimensions[r].height = 30; ws[f"A{r}"].font = Font(name=F, size=9)
ws["A24"] = "Legend"; ws["A24"].font = bold
ws["A25"] = "Blue text on yellow fill = input you edit. Black = formula (do not overwrite). Row 10 to 13 example values are illustrative, not measured data."
ws.merge_cells("A25:S25"); ws["A25"].font = Font(name=F, size=9)
ws["D10"].comment = Comment("Share of the remaining recorded dollars in the band after certainty items are removed. Shares must sum to 100%.", "Calculator")
ws["E10"].comment = Comment("Anticipated probability that a transaction in this band contains an error. Planning judgment unless measured; see Notes.", "Calculator")
ws["F10"].comment = Comment("Anticipated root-mean-square percentage misstatement among erroneous transactions in the band (e.g. 0.30 means 30%). Squared inside the workbook to give s_h = E[taint^2 | error]. Used only in Advanced mode.", "Calculator")
ws["G10"].comment = Comment("Optional. Relative review cost per transaction. Leave 1 (or blank) if costs are equal. Used only in Advanced mode.", "Calculator")
widths = {"A": 8, "B": 26, "C": 13, "D": 13, "E": 13, "F": 15, "G": 13, "H": 11, "I": 9, "J": 14, "K": 14, "L": 12, "M": 13, "N": 10, "O": 10, "P": 12, "Q": 14, "R": 13, "S": 13}
for c, w in widths.items(): ws.column_dimensions[c].width = w
ws.freeze_panes = "A10"

# ---------------- Sensitivity sheet ----------------
sv = wb.create_sheet("Sensitivity")
sv["A1"] = "Sensitivity: one band's occurrence rate"; sv["A1"].font = title
sv["A2"] = ("Vary the occurrence rate of one band while holding the other bands at their Calculator values. Multipliers apply to that band's p_h only; "
            "scaling every band by the same factor would leave the shares unchanged."); sv.merge_cells("A2:H2"); sv["A2"].alignment = Alignment(wrap_text=True, vertical="top"); sv.row_dimensions[2].height = 32
sv["A4"] = "Band to vary (1-4)"; sv["B4"] = 4; sv["B4"].font = blue; sv["B4"].fill = yellow; sv["B4"].border = box; sv["A4"].font = bold
dv3 = DataValidation(type="whole", operator="between", formula1="1", formula2="4"); sv.add_data_validation(dv3); dv3.add("B4")
sv["A5"] = "Base occurrence of that band"; sv["B5"] = "=INDEX(Calculator!$E$10:$E$13,$B$4)"; sv["B5"].number_format = "0.00%"; sv["A5"].font = bold; sv["B5"].font = green
sv["A6"] = "Base unnormalized weight of that band"; sv["B6"] = "=INDEX(Calculator!$K$10:$K$13,$B$4)"; sv["B6"].number_format = "0.00000"; sv["A6"].font = bold; sv["B6"].font = green
sv["A7"] = "Sum of other bands' weights"; sv["B7"] = "=Calculator!$K$14-$B$6"; sv["B7"].number_format = "0.00000"; sv["A7"].font = bold; sv["B7"].font = green
hdr = ["Multiplier on p_h", "Occurrence used", "Share: band 1", "Share: band 2", "Share: band 3", "Share: band 4", "Count: varied band", "MUS count: varied band"]
for c, h in zip("ABCDEFGH", hdr):
    cell = sv[f"{c}9"]; cell.value = h; cell.font = bold; cell.fill = head; cell.alignment = wrap; cell.border = box
sv.row_dimensions[9].height = 36
mults = [0.25, 0.5, 0.75, 1.0, 1.5, 2.0, 3.0, 5.0]
for i, mlt in enumerate(mults):
    r = 10 + i
    sv[f"A{r}"] = mlt; sv[f"A{r}"].font = blue; sv[f"A{r}"].fill = yellow; sv[f"A{r}"].number_format = "0.00"
    sv[f"B{r}"] = f"=$B$5*A{r}"; sv[f"B{r}"].number_format = "0.00%"
    # varied band's new weight = base weight * sqrt(multiplier); denominator = others + new weight
    for j, c in enumerate("CDEF", start=1):
        sv[f"{c}{r}"] = (f"=IF($B$7+$B$6*SQRT(A{r})=0,0,IF($B$4={j},$B$6*SQRT(A{r}),INDEX(Calculator!$K$10:$K$13,{j}))/($B$7+$B$6*SQRT(A{r})))")
        sv[f"{c}{r}"].number_format = "0.0%"
    sv[f"G{r}"] = f"=ROUND(INDEX(C{r}:F{r},$B$4)*Calculator!$B$5,0)"; sv[f"G{r}"].number_format = "0"
    sv[f"H{r}"] = "=INDEX(Calculator!$N$10:$N$13,$B$4)"; sv[f"H{r}"].number_format = "0"
    for c in "ABCDEFGH": sv[f"{c}{r}"].border = box
sv["A19"] = "Reading: the row with multiplier 1.00 reproduces the Calculator sheet. Rows above and below show how much the varied band's share and count move if its occurrence rate is lower or higher than assumed."
sv.merge_cells("A19:H19"); sv["A19"].alignment = Alignment(wrap_text=True, vertical="top"); sv.row_dimensions[19].height = 30; sv["A19"].font = Font(name=F, size=9)
for c, w in zip("ABCDEFGH", (16, 14, 13, 13, 13, 13, 16, 18)): sv.column_dimensions[c].width = w

# ---------------- Notes sheet ----------------
nt = wb.create_sheet("Notes")
notes = [
    ("Purpose", "Allocates a chosen probabilistic sample across 3 or 4 amount bands in proportion to the residual misstatement risk the auditor anticipates in each band. Companion to 'Assumed, Not Measured: What Monetary-Unit Sampling Assumes About Where Error Lives'."),
    ("Not a sample-size tool", "The planned sample size (Calculator!B5) comes from the engagement's own sample-size determination. This workbook only distributes it across bands."),
    ("Certainty items", "Remove individually material, high-consequence and policy-required items before using the workbook. The dollar shares D_h refer to the remaining population."),
    ("Formula", "Suggested share_h = D_h x sqrt(p_h x s_h / c_h), normalized to sum to one. D_h = share of remaining dollars; p_h = probability a transaction in the band is erroneous; s_h = expected squared percentage misstatement among erroneous transactions (entered as its square root, the RMS percentage error); c_h = relative review cost per transaction."),
    ("Basic mode", "Sets s_h = 1 and c_h = 1 for every band, so share_h is proportional to D_h x sqrt(p_h). This assumes equal percentage severity and equal review cost across bands; state that assumption when you use it."),
    ("Advanced mode", "Uses the entered RMS percentage error (squared) as s_h and the entered cost as c_h. Blank or zero severity falls back to 1; blank or zero cost falls back to 1."),
    ("MUS as the special case", "If p_h x s_h / c_h is the same in every band, the multiplier cancels and the suggested share equals the MUS share D_h. Column Q reports the occurrence rate that would make each band's product equal the reference band's: the assumption MUS makes, in the planner's own units."),
    ("Where the inputs come from", "Prior audits of the same population, pilot or reference samples, re-performance, adjudicated historical results, or explicit planning assumptions. Inputs that are judgments rather than measurements should be labeled as such and varied in the Sensitivity sheet."),
    ("Within-band selection", "The rule assumes dollar-proportional selection within each band (the usual MUS mechanics) and changes only how the sample is divided between bands."),
    ("Rounding", "Suggested counts are rounded to whole transactions; the rounded total may differ from the planned size by one or two. Adjust by hand if needed."),
    ("Example values", "The example bands (rows 10-13) are hypothetical planning inputs and match Table 7 of the manuscript. They are not measured data."),
    ("Verification", "The companion Python script check_calculator.py reproduces the example allocation independently and compares it with the workbook's recalculated values."),
]
nt["A1"] = "Notes and assumptions"; nt["A1"].font = title
for i, (k, v) in enumerate(notes):
    r = 3 + i
    nt[f"A{r}"] = k; nt[f"A{r}"].font = bold; nt[f"A{r}"].alignment = Alignment(vertical="top")
    nt[f"B{r}"] = v; nt[f"B{r}"].font = norm; nt[f"B{r}"].alignment = Alignment(wrap_text=True, vertical="top")
    nt.row_dimensions[r].height = 48
nt.column_dimensions["A"].width = 26; nt.column_dimensions["B"].width = 110

wb.calculation.fullCalcOnLoad = True
wb.save("MUS_Risk_Aligned_Allocation_Calculator.xlsx")
print("saved")
