# import libraries 
import streamlit as st
import pandas as pd 
import numpy as np 
import plotly.express as px
import plotly.graph_objects as go



# set up dashboard 
st.set_page_config(page_title= "Ebay Laptop Sales Dashboard", layout= "wide")
col1, col2 = st.columns([0.3,0.7], vertical_alignment="center")
with col1: 
    st.image("ebay_logo.png")
with col2:
    st.title("Laptop Sales Dashboard")
st.divider()

# load data 
df = pd.read_csv('EbayCleanedDataSample.csv')
# pre-process data
df['Condition'] = df['Condition'].str[:3]
# categorize condition as either Used, New, Seller Refurbished, Very Good Refurbished, Good Refurbished, Excellent Refurbished, Open Box, Certified Refurbished, For Parts or Not Working, or Open Box 
df['Condition'] = df['Condition'].str.strip()
df['Condition'] = df['Condition'].apply(lambda x: 'Used' if x == 'Use' else 'New' if x == 'New' else 'Seller Refurbished' if x == 'Sel' else 'Very Good - Refurbished' if x == 'Ver' else 'Good - Refurbished' if x == 'Goo' else 'Excellent - Refurbished' if x == 'Exc' else 'Open Box' if x == 'Ope' else 'Certified Refurbished' if x == 'Cer' else 'For Parts or Not Working' if x == 'For' else 'Not Specified')
# Replace Windows 11 Home S with Windows 11 Home 
df['OS'] = df['OS'].str.replace('Windows 11 Home S', 'Windows 11 Home')
df['OS'] = df['OS'].str.replace('\u200eWindows 11 Home', 'Windows 11 Home')
df['OS'] = df['OS'].str.replace('Windows 11 pros', 'Windows 11 Pro')
df['OS'] = df['OS'].str.replace('Windows 10 pros', 'Windows 10 Pro')
df['OS'] = df['OS'].str.replace('Windows 10 Pros', 'Windows 10 Pro')
df['OS'] = df['OS'].str.replace('Windows 10 Pro 64Bit', 'Windows 10 Pro')
df['OS'] = df['OS'].str.replace('Windows 7 Professional', 'Windows 7 Pro')
df['OS'] = df['OS'].str.replace('windows 11', 'Windows 11')
df['OS'] = df['OS'].str.replace('Win 10', 'Windows 10')
df['OS'] = df['OS'].str.replace('Windows 10 Pro 64', 'Windows 10 Pro')
df['OS'] = df['OS'].str.replace('Windows 10 Home 64', 'Windows 10 Home')
df['OS'] = df['OS'].str.replace('Windows 10 Professional', 'Windows 10 Pro')
df['OS'] = df['OS'].str.replace('Windows 11 S mode', 'Windows 11 S')
df['OS'] = df['OS'].str.replace('Windows 11 S Mode', 'Windows 11 S')
df['OS'] = df['OS'].str.replace('Microsoft Windows 10 Pro', 'Windows 10 Pro')
df['OS'] = df['OS'].str.replace('Mac Os', 'macOS')
df['OS'] = df['OS'].str.replace('Microsoft Windows 11', 'Windows 11')
df['OS'] = df['OS'].str.replace('Mac OS', 'macOS')

st.header("💻 eBay Laptop Sales Data")
st.write("The dataset contains information on **1,013** laptops sold on eBay") 
tab1, tab2 = st.tabs(["Full Data View", "Filtered Data View"])

with tab1:
 st.header("Full Data View")
 st.dataframe(df)
 price_fig = px.histogram(
    data_frame=df,
    x='Price',
    title='Distribution of Laptop Sale Prices',
    labels={'Price': 'Price ($)'},
    color_discrete_sequence=['green'] 
    )       
 price_fig.update_layout(
    xaxis_title='Price ($)',
    yaxis_title='Count of Laptop Sales',
    bargap=0.05  # Reduce gap between bars for a cleaner look
    )
 st.plotly_chart(price_fig)

with tab2: 
   # brand filter 
   selected_brands = st.multiselect(
      "Select Brand(s): ",
      options= df['Brand'].unique(), 
      default= df['Brand'].unique()
   )

   # CONDITION filter 
   selected_condition = st.multiselect(
      "Select Condition(s): ", 
      options= df['Condition'].unique(), 
      default= df['Condition'].unique()
   )

   # price filter 
   min_price = int(df['Price'].min())
   max_price = int(df['Price'].max())
   price_range = st.slider(
      "Select Price Range:", 
      min_value= min_price,
      max_value= max_price,
      value = (min_price, max_price)
   )

   # apply filters 
   filtered_data = df[
        (df['Brand'].isin(selected_brands)) &
        (df['Price'] >= price_range[0]) &
        (df['Price'] <= price_range[1]) &
        (df['Condition'].isin(selected_condition))
    ]
   
   # display filtered data 
   st.dataframe(filtered_data, use_container_width= True)
   # Convert data to CSV
   csv_data = filtered_data.to_csv(index=False)
   st.download_button(label="Download Data as CSV",
    data=csv_data,
    file_name="laptopsales_data.csv",
    mime="text/csv")
   
# Visualize Key Features 
st.header("Visualizations of Key Features")
st.write("eBay Laptop Sales by **Brand**, **Condition**, and **Operating System (OS)**")
st.subheader("Laptop Sale Counts")
tab3, tab4, tab5 = st.tabs(["Brand", "Condition", "OS"])
with tab3: 
   brands_multi = st.multiselect(
      "Select Brand(s): ",
      options= df['Brand'].unique(), 
      default= df['Brand'].unique(), 
      key= "brand"
   )
   brand_df = df[df['Brand'].isin(brands_multi)] 
   sales_by_brand = brand_df.groupby('Brand').size().reset_index(name='Number of Sales')
   sales_by_brand.set_index('Brand', inplace=True)
   st.write("### Count of Laptop Sales by Brand")
   st.bar_chart(sales_by_brand['Number of Sales'])
   st.caption("Dell, Lenovo, and HP dominate laptop sales on eBay, indicating their popularity and affordability. Lesser-known brands may have niche audiences or limited availability.")
 

   # show avg price by brand 
   avg_price_brand = brand_df.groupby('Brand')['Price'].mean().reset_index()
   avg_price_brand.columns = ['Brand', 'Average Price']
   brand_price_fig = px.bar(
    avg_price_brand,
    x='Brand',
    y='Average Price',
    title='Average Price by Brand',
    labels={'Brand': 'Brand', 'Average Price': 'Average Price ($)'},
    color='Average Price',
    color_continuous_scale='Greens'
   )
   st.plotly_chart(brand_price_fig)
   with st.expander("Detailed Business Analysis for Brand Insights"):
    st.markdown("""
    - **Count of Laptop Sales by Brand**:
      - Dell, Lenovo, and HP are the most frequently sold laptop brands, reflecting their popularity and affordability among eBay buyers.
      - Lesser sales for Apple indicate that high pricing may limit its market reach, while niche or lesser-known brands have minimal sales, likely due to limited demand or availability.
      - Sellers should prioritize listing popular brands like Dell and Lenovo to maximize sales. For brands with lower sales, targeted promotions and better pricing strategies could improve visibility.

    - **Average Price by Brand**:
      - Dell, Lenovo, and HP offer lower average prices, catering to eBay’s cost-conscious buyers and contributing to their higher sales volume.
    """)



with tab4: 
   condition_multi = st.multiselect(
      "Select Conditions(s): ",
      options= df['Condition'].unique(), 
      default= df['Condition'].unique(), 
      key= "condition"
   )
   condition_df = df[df['Condition'].isin(condition_multi)] 
   sales_by_condition = condition_df.groupby('Condition').size().reset_index(name='Number of Sales')
   sales_by_condition.set_index('Condition', inplace=True)
   st.write("### Count of Laptop Sales by Condition")
   st.bar_chart(sales_by_condition['Number of Sales'])
   st.caption("The majority of laptop sales are for 'Used' and 'Seller Refurbished' conditions, highlighting eBay's popularity as a platform for second-hand items. New and certified refurbished laptops have significantly lower sales volumes, indicating they cater to a smaller market of buyers seeking premium options.")


   
   # show avg price by condition 
   avg_price_conditon = condition_df.groupby('Condition')['Price'].median().reset_index()
   avg_price_conditon.columns = ['Condition', 'Average Price']
   condition_price_fig = px.bar(
    avg_price_conditon,
    x='Condition',
    y='Average Price',
    title='Average Price by Condition',
    labels={'Condition': 'Condition', 'Average Price': 'Average Price ($)'},
    color='Average Price',
    color_continuous_scale='Greens'
   )
   st.plotly_chart(condition_price_fig)
   st.caption("New laptops command the highest average prices, followed by certified refurbished laptops, reflecting their premium quality and reliability. In contrast, used laptops are priced significantly lower, appealing to budget-conscious buyers")
   with st.expander("Detailed Business Analysis for Condition Insights"): 
      st.write("""
               The popularity of 'Used' and 'Seller Refurbished' laptops suggests that eBay buyers prioritize affordability over brand-new products.
      - Sellers of new and certified refurbished laptops may need to emphasize quality, warranty, or exclusive features to attract more buyers.
      - Increasing promotions or offering bundled deals for new or certified refurbished laptops could help capture more price-sensitive customers in these categories.
      """)


with tab5: 
   os_multi = st.multiselect(
      "Select Operating System(s): ",
      options= df['OS'].unique(), 
      default= df['OS'].unique(), 
      key= "os"
   )
   os_df = df[df['OS'].isin(os_multi)] 
   sales_by_os = os_df.groupby('OS').size().reset_index(name='Number of Sales')
   sales_by_os.set_index('OS', inplace=True)
   st.write("### Count of Laptop Sales by OS")
   st.bar_chart(sales_by_os['Number of Sales'])

st.divider()

st.header("Laptop Specifications vs. Sale Prices: Insights by Condition and Brand")



# Screen Size 
# make screen size an integer 

# strip 'in' 
df['Screen Size'] = df['Screen Size'].str.strip('in')
df['Screen Size'] = df['Screen Size'].astype(float)

# RAM Size 
# make ram size a float variable
# strip 'GB' 
df['Ram Size'] = df['Ram Size'].str.strip('GB')
df['Ram Size'] = df['Ram Size'].astype(float)

condition_scatters = make_subplots(
   rows = 1, 
   cols = 2, 
   subplot_titles=("Screen Size vs. Price", "RAM Size vs. Price")
)

screen_size_scatter = px.scatter(
    df,
    x='Screen Size',
    y='Price',
    color='Condition',
    labels={
        'Screen Size': 'Screen Size (inches)',
        'Price': 'Price ($)',
        'Condition': 'Condition'
    },
).data  # Extract the scatterplot data to add manually
for trace in screen_size_scatter:
    condition_scatters.add_trace(trace, row=1, col=1)

ram_size_scatter = px.scatter(
    df,
    x='Ram Size',
    y='Price',
    color='Condition',
    labels={
        'Ram Size': 'RAM Size (GB)',
        'Price': 'Price ($)',
        'Condition': 'Condition'
    },
).data  # Extract the scatterplot data to add manually
for trace in ram_size_scatter:
    trace.showlegend = False
    condition_scatters.add_trace(trace, row=1, col=2)

condition_scatters.update_layout(title_text = "Screen Size & Ram Size vs. Price<br><sub><i>Grouped by Condition</i>", 
                                  xaxis_title="Screen Size (inches)",
    yaxis_title="Price ($)",
    xaxis2_title="RAM Size (GB)",
    legend=dict(title=dict(text="<b>Condition<b>")))


with st.container(border = True):
   st.plotly_chart(condition_scatters, use_container_width=True)


brand_scatters = make_subplots(
   rows = 1, 
   cols = 2, 
   subplot_titles=("Screen Size vs. Price", "RAM Size vs. Price")
)

screen_size_scatter_b = px.scatter(
    df,
    x='Screen Size',
    y='Price',
    color='Brand',
    labels={
        'Screen Size': 'Screen Size (inches)',
        'Price': 'Price ($)',
        'Brand': 'Brand'
    },
).data  # Extract the scatterplot data to add manually
for trace in screen_size_scatter_b:
    brand_scatters.add_trace(trace, row=1, col=1)


ram_size_scatter_b = px.scatter(
    df,
    x='Ram Size',
    y='Price',
    color='Brand',
    labels={
        'Ram Size': 'RAM Size (GB)',
        'Price': 'Price ($)',
        'Brand': 'Brand'
    },
).data  # Extract the scatterplot data to add manually
for trace in ram_size_scatter_b:
    trace.showlegend = False
    brand_scatters.add_trace(trace, row=1, col=2)

brand_scatters.update_layout(title_text = "Screen Size & Ram Size vs. Price<br><sub><i>Grouped by Brand</i>", 
                              xaxis_title="Screen Size (inches)",
    yaxis_title="Price ($)",
    xaxis2_title="RAM Size (GB)", 
    legend=dict(title=dict(text="<b>Brand<b>")))

with st.container(border = True):
   st.plotly_chart(brand_scatters, use_container_width=True)

with st.expander("Detailed Business Analysis for Screen Size vs. Price"):
    st.markdown("""
    - **Observation**:
      - Laptops with screen sizes between 14 and 16 inches have a higher price range, indicating their alignment with premium or performance-oriented devices.
      - Smaller screen sizes (<14 inches) are more affordable and dominate the lower price spectrum, appealing to buyers looking for lightweight and portable options.

    - **Business Analysis**:
      - The positive trend between screen size and price suggests that buyers associate larger screens with better usability for productivity or multimedia tasks.
      - Sellers of larger screen laptops should highlight features like high resolution, color accuracy, or productivity benefits to justify their pricing.
      - For smaller screen laptops, sellers can target students or travelers by emphasizing portability and affordability in their marketing.
    """)

with st.expander("Detailed Business Analysis for RAM Size vs. Price"):
    st.markdown("""
    - **Observation**:
      - Higher RAM capacities (16GB and above) correlate with significantly higher prices, appealing to users needing high performance for tasks like gaming or video editing.
      - Lower RAM sizes (4GB–8GB) dominate the lower price range, reflecting their affordability and use for everyday computing needs.

    - **Business Analysis**:
      - The clear pricing differentiation based on RAM size shows that buyers value memory capacity for performance-intensive use cases.
      - Sellers offering laptops with high RAM capacities should target professionals, gamers, or content creators and emphasize multitasking and speed in their marketing.
      - For lower RAM configurations, focusing on cost-effective solutions for students or casual users would align with their affordability appeal.
    """)

    






