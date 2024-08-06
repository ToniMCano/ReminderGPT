



'''
answer_prompt = PromptTemplate.from_template(
    """Given the following user question, corresponding SQL query, and SQL result, answer the user question.

Question: {question}
SQL Query: {query}
SQL Result: {result}
Answer: """
)

answer = answer_prompt | llm | StrOutputParser()
chain = (
    RunnablePassthrough.assign(query=write_query).assign(
        result=itemgetter("query") | execute_query
    )
    | answer
)



db.run(response)    
'''

import sqlite3
from datetime import datetime

def query():
    connection = sqlite3.connect('C:\\Users\\34615\\Documents\\Python\\ReminderGPT\\reminder_gpt\\ecommerce.db')
    
    cursor = connection.cursor()
    
    
    query = cursor.execute("SELECT fecha_factura FROM ventas").fetchall()
    
    
    for date in query:
        
        old_date = date[0]
        to_change = datetime.strptime(date , "%m-%d-%Y %H:%M") 
        changed = to_change.strftime("%Y-%m-%d %H:%M")
        
        changed = to_change.strftime("%Y-%m-%d %H:%M")

        print(changed)

        cursor.execute("UPDATE ventas SET fecha_factura = ? WHERE fecha_factura = ?", (changed, old_date))
    
    connection.commit()
    connection.close
    
        
    
    '''original_format = "%d/%m/%Y %H:%M"
    # Formato ISO 8601
    iso_format = "%Y-%m-%d %H:%M:%S"
    # Convertir la fecha
    datetime_obj = datetime.strptime(date_str, original_format)
    iso_date_str = datetime_obj.strftime(iso_format)
    
    cursor.execute("UPDATE ventas SET fecha_factura = ? WHERE id = ?", (iso_date_str, record_id))
'''
    
    

'''from datetime import datetime


to_change = datetime.strptime("" , "%m-%d-%Y %H:%M")
 
changed = to_change.strftime("%Y-%m-%d %H:%M")

print(changed)
 '''
    
    

        


