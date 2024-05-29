from flask import url_for, redirect
import openai
import cx_Oracle

# OpenAI API Key
openai.api_key = ''

table = """### Table Format: Table_Name(Column_Name: sample Column_Value, Column_Name: sample Column_Value)
           # 
           # CHATGPT_UNIT_MASTER(BUILDING: TOWER A / TOWER B, UNIT_CODE: MGT2-FL23-2301, UNIT_NUMBER: 2301, GROSS_AREA: 1000.56, BALCONY_AREA: 52.36, PRICE_VALUE: 2,000,000.00, UNIT_SPECS_NAME: 1 BHK / STUDIO / 2 BHK, UNIT_TYPE_NAME: TYPE 1 / TYPE A, UNIT_VIEW_NAME: Barsha South View, UNIT_OPEN_FOR_SALE: YES / NO)
           #
           """



def get_query(message, max_token):
    """
    Call the OpenAI API to generate a response to a given prompt.
    Parameters:
        - prompt (str): The message to generate a response for.
    Returns:
        - str: The generated response from the OpenAI API.
    """

    prompt = f"""### Oracle 11gR2 SQL tables, with their properties, data types and examples(if applicable):
                #
                {table}
                #
                ### Try to generate the sql query according to prompt. You can adjust the query as needed to include any additional criteria or to include other attributes from the table.
                ### prompt: {message} ->, completion: """

    response = openai.Completion.create(
        model="code-davinci-002",
        prompt=prompt,
        temperature=0,
        max_tokens=max_token,
        top_p=1.0,
        frequency_penalty=0.0,
        presence_penalty=0.0,
        stop=["#", ";"]
    )

    return response["choices"][0]["text"]

