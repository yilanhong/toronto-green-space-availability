# Builds the two comparison charts from the summary tables.
# Run from the repository root: python scripts/make_charts.py

import pandas as pd, matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
plt.rcParams['font.family']='DejaVu Sans'

g=pd.read_csv('data/summary_tables/Results_Demographic_Comparison.csv').set_index('Variable')
c=pd.read_csv('data/summary_tables/Results_CaseStudy_Comparison.csv').set_index('Variable')

def fmt(v,kind):
    if kind=='$': return f"${v/1000:.0f}k"
    if kind=='int': return f"{v:,.0f}"
    if kind=='m2': return f"{v:.1f}"
    return f"{v:.1f}%"

def panel(ax,labels,vals,colors,title,kind,hatch=None):
    bars=ax.bar(range(len(vals)),vals,color=colors,edgecolor='#333',linewidth=0.6)
    if hatch is not None:
        for b,h in zip(bars,hatch):
            if h: b.set_hatch(h); b.set_facecolor('white')
    top=max(vals)
    for b,v in zip(bars,vals):
        ax.text(b.get_x()+b.get_width()/2,v+top*0.02,fmt(v,kind),ha='center',va='bottom',fontsize=8.5)
    ax.set_title(title,fontsize=10.5,fontweight='bold',pad=8)
    ax.set_xticks(range(len(vals))); ax.set_xticklabels(labels,fontsize=8.5)
    ax.set_ylim(0,top*1.18)
    ax.spines[['top','right','left']].set_visible(False); ax.set_yticks([])

# ---------- Chart 1: groups ----------
groups=['Underserved','Moderate','Well-served','Citywide']
cols=['#E8743B','#C9C9C9','#2E7D32','white']
hat=[None,None,None,'///']
vars1=[('Population density (people per km2)','Population density\n(people per km²)','int'),
       ('Apartments in buildings 5+ storeys (%)','Apartments in\nbuildings 5+ storeys','%'),
       ('Renter households (%)','Renter households','%'),
       ('Median household income, 2020 ($) - median of tracts','Median household\nincome (2020)','$'),
       ('Visible minority population (%)','Visible minority\npopulation','%'),
       ('Immigrant population (%)','Immigrant\npopulation','%'),
       ('Population aged 0-14 (%)','Children\n(aged 0–14)','%'),
       ('Low income prevalence, LIM-AT (%)','Low income\n(LIM-AT)','%')]
fig,axes=plt.subplots(2,4,figsize=(14,7.6))
for ax,(k,t,kind) in zip(axes.flat,vars1):
    panel(ax,['Under-\nserved','Moderate','Well-\nserved','City-\nwide'],[g.loc[k,x] for x in groups],cols,t,kind,hat)
fig.suptitle('Demographic Profile of Census Tracts by Green Space Availability, City of Toronto',fontsize=15,fontweight='bold',y=0.985)
fig.text(0.5,0.925,'Groups based on green space per resident: Underserved = bottom 25% (under 3.3 m²), Moderate = middle 50%, Well-served = top 25% (over 33.4 m²)',ha='center',fontsize=10,color='#444')
fig.text(0.01,0.015,'Values are averages across census tracts in each group (144 underserved, 288 moderate, 145 well-served, 577 citywide). Income shows the median of tract median household incomes.\n'
         'Data: City of Toronto Open Data (Green Spaces, Neighbourhoods); Statistics Canada, 2021 Census of Population. Chart by Yilan Hong, 2026.',fontsize=7.8,color='#555',va='bottom')
fig.tight_layout(rect=[0,0.06,1,0.91],h_pad=2.5)
fig.savefig('charts/Chart_01_Demographics_by_Availability_Group.png',dpi=300,facecolor='white'); plt.close()

# ---------- Chart 2: case studies ----------
areas=['Downtown Yonge East','Rustic','Black Creek']
acols=['#E8743B','#C9C9C9','#2E7D32']
vars2=[('Green space per resident (m2)','Green space per resident\n(m²)','m2'),
       ('Population density (people per km2)','Population density\n(people per km²)','int'),
       ('Apartments in buildings 5+ storeys (%)','Apartments in\nbuildings 5+ storeys','%'),
       ('Population aged 0-14 (%)','Children\n(aged 0–14)','%'),
       ('Visible minority population (%)','Visible minority\npopulation','%'),
       ('Immigrant population (%)','Immigrant\npopulation','%'),
       ('Unemployment rate, pop-weighted avg (%)','Unemployment\nrate','%'),
       ('Low income prevalence, LIM-AT (%)','Low income\n(LIM-AT)','%')]
fig,axes=plt.subplots(2,4,figsize=(14,7.6))
for ax,(k,t,kind) in zip(axes.flat,vars2):
    panel(ax,['Downtown\nYonge East','Rustic','Black\nCreek'],[float(c.loc[k,a]) for a in areas],acols,t,kind)
fig.suptitle('Case Study Comparison: Downtown Yonge East, Rustic, and Black Creek',fontsize=15,fontweight='bold',y=0.985)
fig.text(0.5,0.925,'Lowest to highest green space per resident among the three case study neighbourhoods',ha='center',fontsize=10,color='#444')
fig.text(0.01,0.015,'Neighbourhood values combine census tracts whose centroids fall within each neighbourhood (3, 2, and 5 tracts). Percentages are recalculated from summed counts;\n'
         'unemployment and low income are population-weighted averages of tract rates. Data: City of Toronto Open Data; Statistics Canada, 2021 Census of Population. Chart by Yilan Hong, 2026.',fontsize=7.8,color='#555',va='bottom')
fig.tight_layout(rect=[0,0.06,1,0.91],h_pad=2.5)
fig.savefig('charts/Chart_02_Case_Study_Comparison.png',dpi=300,facecolor='white'); plt.close()
print('done')
