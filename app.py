# استيراد المكتبات
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# تحميل البيانات 
df = pd.read_csv("sales_data_sample.csv", sep=',', encoding='ISO-8859-1')

# التأكد من تحميل البيانات
st.title('تطبيق تحليل بيانات المبيعات')
st.write('هذا التطبيق يعرض بيانات المبيعات للمدن المختلفة.')

# عرض البيانات الأصلية
if st.checkbox('إظهار البيانات الأصلية'):
    st.dataframe(df.head(8))

# تنظيف البيانات
df = df.dropna(how='all')
df['ORDERDATE'] = pd.to_datetime(df['ORDERDATE'])
df['QUANTITYORDERED'] = pd.to_numeric(df['QUANTITYORDERED'], errors='coerce')
df['PRICEEACH'] = pd.to_numeric(df['PRICEEACH'], errors='coerce')

# عرض ملخص عن البيانات
if st.checkbox('عرض ملخص البيانات'):
    st.write(df.describe())

# إنشاء عامود جديد لحساب الإيرادات الكلية
df['Total_Revenue'] = df['QUANTITYORDERED'] * df['PRICEEACH']

# حساب المقاييس لكل منتج
product_metrics = df.groupby('PRODUCTCODE').agg({
    'Total_Revenue': 'sum',
    'QUANTITYORDERED': 'sum',
    'PRICEEACH': 'mean',
    'ORDERNUMBER': 'nunique'
}).rename(columns={'ORDERNUMBER': 'ORDER_COUNT'}).reset_index()

# ترتيب المنتجات بناءً على الإيرادات
product_metrics.sort_values(by='Total_Revenue', ascending=False, inplace=True)

# عرض المقاييس لكل منتج
if st.checkbox('إظهار مقاييس المنتجات'):
    st.write(product_metrics)

# حساب المقاييس لكل شهر
monthly_metrics = df.groupby('MONTH_ID').agg({
    'Total_Revenue': 'sum',
    'QUANTITYORDERED': 'sum',
    'PRICEEACH': 'mean'
}).reset_index()

# عرض جدول المقاييس لكل شهر
st.subheader('جدول المقاييس لكل شهر')
st.dataframe(monthly_metrics)

# رسم الإيرادات الشهرية
st.subheader('الإيرادات الشهرية')
plt.figure(figsize=(10, 5))
sns.lineplot(x='MONTH_ID', y='Total_Revenue', data=monthly_metrics)
plt.title('Total Monthly Revenue')
plt.xlabel('MONTH_ID')
plt.ylabel('Total_Revenue')
st.pyplot(plt)

# حساب المبيعات لكل مدينة
city_metrics = df.groupby('CITY').agg({
    'Total_Revenue': 'sum'
}).reset_index()

# ترتيب المدن واختيار أعلى 5 مدن
top_cities = city_metrics.sort_values(by='Total_Revenue', ascending=False).head(5)

# عرض جدول ترتيب المدن
st.subheader('ترتيب أول 5 مدن حسب الإيرادات')
st.dataframe(top_cities)

# رسم المبيعات لأفضل 5 مدن
st.subheader('أعلى 5 مدن من حيث الإيرادات')
plt.figure(figsize=(10, 5))
sns.barplot(x='CITY', y='Total_Revenue', data=top_cities)
plt.title('Top 5 Cities by Total_Revenue')
plt.xlabel('CITY')
plt.ylabel('Total_Revenue')
st.pyplot(plt)
