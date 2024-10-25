# Import python packages
import streamlit as st
from snowflake.snowpark.context import get_active_session
from snowflake.snowpark.functions import col

# Write directly to the app
st.title("Customize Your Smoothie :cup_with_straw:")
st.write(
    """
    Choose the fruits you want in your customer Smoothie!
    """
)

name_on_order = st.text_input('Name on smoothie: ')
st.write('The name on your smoothie will be: ', name_on_order)

session = get_active_session()
my_dateframe = session.table('smoothies.public.fruit_options').select(col('FRUIT_NAME'))
# st.dataframe(data=my_dateframe, use_container_width=True)

ingredient_list = st.multiselect(
    'Choose up to 5 ingredients',
    my_dateframe,
    max_selections=5,
)

if ingredient_list:
    ingredient_string = ' '.join(ingredient_list)
    st.write(ingredient_string)
    time_to_insert = st.button('Submit Order')
    
    if time_to_insert:
        my_insert_stmt = f"""
            INSERT INTO smoothies.public.orders(ingredients, name_on_order)
            VALUES (?, ?)
        """
        session.sql(my_insert_stmt, params=[ingredient_string, name_on_order]).collect()
        st.success('Your Smoothie is ordered!', icon="✅")
